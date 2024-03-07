import json
import random
from Dictionary.make_dict import *

# Starting letter count
starting_letters = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2, "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3, "W": 3, "X": 2, "Y": 3, "Z": 2}

# Class to describe the remaining letters, plus randomly retrieving some
# It currently creates a starting 21 and peels
# No functionality yet for dumps or letting the user know when there's not enough tiles left
# Everything for single player
class BananaPouch:
    # Uses starting_letters dict to make the list of letters in pouch
    def __init__(self):
        self.remaining = []
        self.reset()

    # Returns array of 21 letters
    def setup(self):
        starting_chars = []
        for i in range(21):
            starting_chars.append(self.peel())
        return starting_chars
    
    # Take a random letter from the list of remaining letters
    def peel(self):
        if len(self.remaining) > 0:
            return self.remaining.pop(random.randint(0,len(self.remaining) - 1))
        else:
            return -1
    def reset(self):
        self.remaining = []
        for char in starting_letters.keys():
            for i in range(starting_letters[char]):
                self.remaining.append(char)

# Currently useless, but aiming to find all/best anagrams using the hash
# So far only finds if a base or base minus one char has anagrams
# def find_best_ana(base):
#     base_unique = ''.join(set(base))
#     ana_list = []
#     if base in word_dict.keys():
#         ana_list.append(base)
#     for i in base_unique:
#         base_cat = base.replace(i, '', 1)
#         if base_cat in word_dict.keys():
#             ana_list.append(base_cat)
#     return ana_list

# Loads the hash dictionary
# with open("Dictionary/hash_dict.json", "r") as file:
#     word_dict = json.load(file)

# trie = Trie()
# make_trie(trie, "Dictionary/word_dictionary.txt")
# print("trie created!")
# pouch = BananaPouch()
# starting_tiles = ''.join(sorted(pouch.setup()))

# print(starting_tiles)
# all_anas = trie.all_subwords(starting_tiles)
# print(all_anas)
# print(len(all_anas))


# # for each line, check for anagrams
# with open("test.txt", "r") as file:
#     lines = file.readlines()
#     for line in lines:
#         base = sort_word(line.strip())
#         print(trie.search(base))
#         print(trie.all_subwords(base))
#         # print(find_best_ana(base))