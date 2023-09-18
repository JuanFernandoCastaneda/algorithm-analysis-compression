import math
import json

def letter_probabilities(text) -> dict:
    # Wont respect uppercases.
    letter_ocurrences = {}
    for letter in text:
        letter_ocurrences[letter] = letter_ocurrences[letter]+1 \
            if letter in letter_ocurrences else 1
    letters = list(letter_ocurrences.keys())
    letters.sort(key=(lambda letter: letter_ocurrences[letter]), reverse=True)
    total_ocurrences = sum(letter_ocurrences.values())
    ordered_letter_probabilities = {letter: round(letter_ocurrences[letter]/total_ocurrences, 3) \
                                    for letter in letters}
    # Returns them ordered
    print(f"Entropía en el peor de los casos es {round(math.log(len(letters), 2), 3)}")
    return ordered_letter_probabilities

# Generates to which code will each word translate.
def generate_codes(text, save_file_name) -> dict:
    ordered_letter_probabilities = letter_probabilities(text)
    # The sizes that the letter encodings should have according to Shannon-Fano.
    shannon_sizes = {key: math.ceil(-math.log(value, 2)) \
                     for (key, value) in ordered_letter_probabilities.items()}
    # Array containing the actual codes.
    letter_codes = {}
    previous_letter = None
    for (letter, size) in shannon_sizes.items():
        # First encoding is full of zeros.
        if previous_letter == None:
            letter_codes[letter] = ["0"]*size
        else:
            # Sum one to the last encoding and then multiply it 
            # by 1 or 0 depending on if the size has changed.
            letter_codes[letter] = \
                binary_times_pow_2(
                    # This is the last plus one.
                    binary_sum_one(letter_codes[previous_letter]),
                    # And this is whether or not the size has changed.
                    shannon_sizes[letter] - shannon_sizes[previous_letter]
                )
        previous_letter = letter
    # Up until this moments the codes are in terms are lists, so we
    # concatenate them.
    concatenated_codes = {letter: "".join(code_list) \
            for (letter, code_list) in letter_codes.items()}
    # Before returning, we save them to a file.
    with open(f"{save_file_name}_reverse_codes.json", "w") as outfile:
        # What we save, though, is the reverse, for easyness of decompression.
        json.dump(
            {"".join(code_list): letter \
                for (letter, code_list) in letter_codes.items()}
            , outfile)
    expected_bits = round(expected_number_of_bits(ordered_letter_probabilities, 
                                                  shannon_sizes), 3)
    print(f"El número de bits esperados es {expected_bits}")
    return concatenated_codes

# Our binary encoding will be a list of strings. NOT IN PLACE.
def binary_sum_one(binary_encoding: list):
    carry = True
    response = binary_encoding.copy()
    # Loop from last to first. 
    for (index, bit) in reversed(list(enumerate(response))):
        # This flips zero to one and one to zero. XOR.
        response[index] = str(1^int(bit))
        # If the bit was a zero before the update, we stop. 
        if response[index] == "1":
            carry = False
            break
    # If we still have a carry after all the procedure insert a new one
    # in the beginning of the list. JUST FOR COMPLETENESS, WON'T BE NEEDED.
    if carry:
        response.insert(0, "1")
    return response

# This does binary_encoding * 2^pow. NOT IN PLACE
def binary_times_pow_2(binary_encoding: list, pow: int):
    result = binary_encoding.copy()
    for _ in range(pow):
        result.append("0")
    return result

def expected_number_of_bits(letter_probabilities, shannon_sizes):
    result = 0
    for letter in letter_probabilities.keys():
        result += letter_probabilities[letter]*shannon_sizes[letter]
    return result


def encode(text: str, save_file_name):
    codes = generate_codes(text, save_file_name)
    response = ""
    # Have to specify lower because otherwise it won't find in codes.
    for letter in text:
        response += codes[letter]
    print(f"El número total de bits usados para la encriptación es {len(response)}")
    return response

# Compresses the text for each 8 bits.
# IF THE LAST BYTE IS INCOMPLETE, A "1" IS ADDED.
def compress(text: str, save_file_name):
    codification = encode(text, save_file_name)
    compression = ""
    for partition_beginning in range(0, len(codification), 8):
        # If the remaining is less than 8, add a 1 to record the value.
        if partition_beginning+8 >= len(codification):
            char_num = int("1" + codification[partition_beginning: len(codification)], base=2)
        else:
            char_num = int(codification[partition_beginning: partition_beginning+8], base=2)
        compression += chr(char_num)
    with open(f"{save_file_name}_compression.txt", "w", encoding="utf-8") as outfile:
        outfile.write(compression)
    return compression

# Has to be txt and json file respectivelly.
def decompress(compressed_file_name: str, code_file_name: str):
    with open(f"{compressed_file_name}", "r", encoding="utf-8") as file:
        compression = file.read()
    with open(f"{code_file_name}", "r", encoding="utf-8") as file:
        reverse_code_table = json.loads(file.read())
    codification = ""
    len_last_char = 0
    for index, character in enumerate(compression):
        if index != len(compression)-1:
            codification += complete_char_to_binary(character)
        else:
            codification += char_to_binary(character)
            # EXPLANAITION MISSING. Remove the length of the 0b.
            len_last_char = len(bin(ord(character)))-2
    # Remove that extra character
    codification = codification[:-len_last_char]+codification[-len_last_char+1:]
    return reverse_codification(codification, reverse_code_table)

# Converts char to ordinal and then to binary str. Then removes the "0b"
# from the string.
def char_to_binary(char):
    return bin(ord(char))[2:]

# Same as char_to_binary but also completes with zeros for lenght to be 8.
def complete_char_to_binary(char):
    result = char_to_binary(char)
    while len(result)<8:
        result = "0" + result
    return result

def reverse_codification(codification: str, reverse_codes: dict):
    carry = ""
    result = ""
    for bit in codification:
        if carry+bit in reverse_codes:
            result += reverse_codes[carry+bit]
            carry = ""
        else:
            carry += bit
    return result


# Tests
'''
assert (binary_sum_one(list("01")) == list("10"))
assert (binary_sum_one(list("11")) == list("100"))
assert (binary_times_pow_2(list("110"), 3) == list("110000"))
assert (generate_codes("aab", "test1") == {"a": "0", "b": "10"})
assert (char_to_binary('b') == "1100010")
assert (complete_char_to_binary('b') == "01100010")
print(compress("Hola222222", save_file_name="holi"))
print(decompress("holi_compression.txt", "holi_reverse_codes.json"))
'''

executing = True
while(executing):
    initial_message = input("A continuación encuentra las opciones disponibles:\n" +
                            '1. Encriptar un texto "m" en un archivo con nombre "n".\n' +
                            '2. Desencriptar un archivo de nombre "n" con la codificación "c".\n' +
                            "3. Salir.\n")
    match initial_message:
        case "1": 
            text_name = input("Ingrese el nombre del archivo txt a comprimir.\n")
            with open(text_name, "r", encoding="utf-8") as file:
                text = file.read()
                destiny_name = input("Ingrese el nombre del archivo destino (sin extensión ni .txt).\n")
                compress(text, destiny_name)
        case "2":
            compressed_file = input("Ingrese el nombre del archivo comprimido," 
                                    +" esta vez con el \".txt\".\n")
            code_file = input("Ingrese el nombre del archivo que guardó la codificación, con el \".json\". \n")
            original_name = compressed_file[:compressed_file.rfind('_compression')] 
            with open(f"{original_name}_decompressed.txt", "w", encoding="utf-8") as outfile:
                result = decompress(compressed_file, code_file)
                outfile.write(result)
            print(f"En el archivo {original_name}_decompressed.txt encontrará el texto descomprimido.\n")
            print(f"Entre medias, puede ver el texto aquí: \n{result}")
        case "3":
            executing = False
        case _:
            print("Opción no válida")