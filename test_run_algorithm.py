from Classes.trie import *
from run_algorithm import *

with open("starting_letters_x1000.txt", "r") as file:
    trie = Trie()
    trie.make_trie("Classes/word_dictionary.txt")

    for line in file.readlines():
        base = ''.join(sorted(line.strip()))
        run_algorithm(base, trie)