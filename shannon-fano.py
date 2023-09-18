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
    with open(f"{save_file_name}_codes.json", "w") as outfile:
        json.dump(concatenated_codes, outfile)
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

def encode(text: str, save_file_name):
    codes = generate_codes(text, save_file_name)
    response = ""
    # Have to specify lower because otherwise it won't find in codes.
    for letter in text:
        response += codes[letter]
    print(response)
    return response

# Compresses the text for each 8 bits.
def compress(text: str, save_file_name):
    codification = encode(text, save_file_name)
    compression = ""
    for partition_beginning in range(0, len(codification), 8):
        # Convert those nums to a byte.
        partition_end = partition_beginning+8 \
            if partition_beginning+8 <= len(codification) \
            else len(codification)
        char_num = int(codification[partition_beginning: partition_end], base=2)
        compression += chr(char_num)
    with open(f"{save_file_name}_compression.txt", "w", encoding="utf-8") as outfile:
        outfile.write(compression)
    return compression

# Has to be txt and json file respectivelly.
def decompress(compressed_file_name: str, code_file_name: str):
    with open(f"{compressed_file_name}", "r", encoding="utf-8") as file:
        compression = file.read()
    with open(f"{code_file_name}", "r", encoding="utf-8") as file:
        code_table = json.loads(file.read())
    print(code_table)
    codification = ""
    for index, character in enumerate(compression):
        codification += complete_char_to_binary(character) \
            if index != len(compression)-1 else char_to_binary(character)
    print(codification)

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

# Tests
assert (binary_sum_one(list("01")) == list("10"))
assert (binary_sum_one(list("11")) == list("100"))
assert (binary_times_pow_2(list("110"), 3) == list("110000"))
assert (generate_codes("aab", "test1") == {"a": "0", "b": "10"})
assert (char_to_binary('b') == "1100010")
assert (complete_char_to_binary('b') == "01100010")

# Tests.
print(compress("Hola amiguitos", save_file_name="holi"))
decompress("holi_compression.txt", "holi_codes.json")
#compress("Hola amiguitos")