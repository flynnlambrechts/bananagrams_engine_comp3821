import json
import pickle

class TrieNode:
    def __init__(self):
        self.children = {}
        self.anagrams = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        s_word = sort_word(word)
        node = self.root
        for char in s_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.anagrams.append(word)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.anagrams

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def all_subwords(self, base):
        subwords = []
        for char in self.root.children.keys():
            if char in base:
                subwords.append(self._recurse_subwords(self.root.children[char], base.replace(char, "", 1)))
        return subwords
    
    def _recurse_subwords(self, node, subbase):
        subwords = node.anagrams
        for char in node.children.keys():
            if char in subbase:
                subwords.append(self._recurse_subwords(node.children[char], subbase.replace(char, "", 1)))
        return subwords



def add_word_hash(hash_dict, word):
    s_word = sort_word(word)
    if s_word in hash_dict.keys():
        hash_dict[s_word].append(word)
    else:
        hash_dict[s_word] = [word]

def sort_word(word):
    return ''.join(sorted(word.upper()))

def make_trie(trie, file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            trie.insert(line.strip())

def make_hash(hash_dict, file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        
        for line in lines:
            add_word_hash(hash_dict, line.strip())
            # print(sort_word(line.strip()))

def save_hash(hash_dict, file_name):
    with open(file_name, "w") as file:
        json.dump(hash_dict, file)
        # for anagrams in word_dict:
        #     for anagram in word_dict[anagrams]:
        #         print(f"{anagrams}: {anagram}")
        #     print()

# def save_trie(trie, file_name):
#     with open(file_name, "w") as file:
#         pickle.dump(trie, file)
#         # for anagrams in word_dict:
#         #     for anagram in word_dict[anagrams]:
#         #         print(f"{anagrams}: {anagram}")
#         #     print()

# trie = Trie()
# make_trie(trie, "Dictionary/word_dictionary.txt")
# save_trie(trie, "trie_dict.json")