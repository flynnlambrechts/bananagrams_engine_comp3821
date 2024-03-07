from anagram_solver import *
from Dictionary.make_dict import *
import timeit
trie = Trie()
make_trie(trie, "Dictionary/word_dictionary.txt")

# with open("starting_letters_x1000.txt", "w") as file:
#     for i in range (1000):
#         pouch.reset()
#         starting_tiles = ''.join(sorted(pouch.setup()))
#         file.write(starting_tiles + '\n')

with open("starting_letters_x1000.txt", "r") as file:
    times = []
    words_found = []
    lines = file.readlines()
    for line in lines:
        base = sort_word(line.strip())
        


