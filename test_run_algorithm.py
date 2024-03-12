from Dictionary.make_dict import *
from run_algorithm import *

with open("starting_letters_x100.txt", "r") as file:
    trie = Trie()
    make_trie(trie, "Dictionary/word_dictionary.txt")

    for line in file.readlines():
        base = sort_word(line.strip())
        run_algorithm(base, trie)