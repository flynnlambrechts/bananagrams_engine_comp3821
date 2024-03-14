from Dictionary.trie import *
from run_algorithm import *

with open("starting_letters_x100.txt", "r") as file:
    trie = Trie()
    trie.make_trie("Dictionary/word_dictionary.txt")

    for line in file.readlines():
        base = ''.join(sorted(line.strip()))
        run_algorithm(base, trie)