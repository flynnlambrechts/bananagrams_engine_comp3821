import json
from trienode import TrieNode
from bananagrams_engine_comp3821.Classes.Trie import Trie

# Adds words to the python dictionary, equivalent to a hash
def add_word_hash(hash_dict, word):
    s_word = ''.join(sorted(word.upper()))
    if s_word in hash_dict.keys():
        hash_dict[s_word].append(word)
    else:
        hash_dict[s_word] = [word]

# Makes a hash out of a given file (line by line)
def make_hash(hash_dict, file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        
        for line in lines:
            add_word_hash(hash_dict, line.strip())
            # print(sort_word(line.strip()))

# Saves the dictionary as a json file
def save_hash(hash_dict, file_name):
    with open(file_name, "w") as file:
        json.dump(hash_dict, file)
        # for anagrams in word_dict:
        #     for anagram in word_dict[anagrams]:
        #         print(f"{anagrams}: {anagram}")
        #     print()
