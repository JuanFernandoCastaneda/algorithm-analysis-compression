import math

class TreeNode:
    def __init__(self, freq, char, isLeaf=False):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None
        self.isLeaf = isLeaf

    def add_left(self, child_node):
        self.left = child_node
    
    def add_right(self, child_node):
        self.right = child_node

    def __str__(self) -> str:
        if self.isLeaf:
            return f'(char: {self.char} freq: {self.freq})'
        else:
            return f'(freq: {self.freq} left: {self.left} right: {self.right})'
def create_huffman_tree(text):
    #lista de caracteres
    chars_occurrances ={}
    for char in text:
        if char not in chars_occurrances:
            chars_occurrances[char] = 1
        else:
            chars_occurrances[char] += 1
    
    char_nodes = []
    for key,value in chars_occurrances.items():
        treeLeaf = TreeNode(freq = value, char = key,isLeaf= True)
        char_nodes.append(treeLeaf)

    char_nodes.sort(key=lambda x:x.freq , reverse=True)

    while len(char_nodes) > 1:
        char1 = char_nodes.pop()
        char2 = char_nodes.pop()

        new_node = TreeNode(freq = char1.freq + char2.freq, char = None, isLeaf = False)

        if char1.isLeaf:
            new_node.add_left(char1)
            new_node.add_right(char2)
        else:
            new_node.add_left(char2)
            new_node.add_right(char1)

        char_nodes.append(new_node)
        char_nodes.sort(key=lambda x:x.freq , reverse=True)
    return char_nodes[0]

def create_huffman_dictionary(huffman_tree):
    dictionary = {}
    def traverse_tree(node, current_code):
        if node.isLeaf:
            dictionary[node.char] = current_code
            return
        traverse_tree(node.left, current_code + '0')
        traverse_tree(node.right, current_code + '1')
    traverse_tree(huffman_tree, '')
    return dictionary

# def huffman_tree_probability(huffman_tree):
#     probabilities = {}
#     total = huffman_tree.freq
#     def traverse_tree(node, current_code):
#         if node.isLeaf:
#             probabilities[node.char] = node.freq/total
#             return
#         traverse_tree(node.left, current_code + '0')
#         traverse_tree(node.right, current_code + '1')
#     traverse_tree(huffman_tree, '')
#     return probabilities

def calculate_entropy(text):
    unique = set(text)
    size = len(unique)
    entropy = math.log2(size)
    return entropy


def encode_text(text, huffman_tree):
    dictionary = create_huffman_dictionary(huffman_tree)
    encoded_text = ''
    for char in text:
        encoded_text += dictionary[char]
    return encoded_text

def decode_huffman_code(code, huffman_tree):
    decoded = ''
    current_node = huffman_tree
    for bit in code:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.isLeaf:
            decoded += current_node.char
            current_node = huffman_tree
    return decoded

if __name__ == '__main__':
    file = input("Escriba el nombre del archivo: ")
    file = "./huffman/texto.txt"
    try :
        with open(file, "r") as f:
            text = f.read()
            huffman_tree = create_huffman_tree(text)
            encoded_text = encode_text(text, huffman_tree)
            # print("Arbol de Huffman: ")
            # print(huffman_tree)
            print("Texto codificado: ")
            print(encoded_text)
            decoded_text = decode_huffman_code(encoded_text, huffman_tree)
            print("Texto decodificado: ")
            print(decoded_text)
            print("Entropia en el peor de los casos: ")
            print(calculate_entropy(text))
    except FileNotFoundError:
        print("No se pudo abrir el archivo")
        exit()
    
    