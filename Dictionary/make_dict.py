import json

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
        return node.is_end_word

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
                subwords.append(self._recurse_subwords(self.children[char], subbase.replace(char, "", 1)))
        return subwords


word_dict = {}
trie = Trie()

def add_word_hash(word):
    s_word = sort_word(word)
    if s_word in word_dict.keys():
        word_dict[s_word].append(word)
        key_list.append(s_word)
    else:
        word_dict[s_word] = [word]

def sort_word(word):
    return ''.join(sorted(word.upper()))


with open("word_dictionary.txt", "r") as file:
    lines = file.readlines()
    
    for line in lines:
        add_word_hash(line.strip())
        trie.insert(line.strip())
        # print(sort_word(line.strip()))


with open("hash_dict.json", "w") as file:
    json.dump(word_dict, file)
    # for anagrams in word_dict:
    #     for anagram in word_dict[anagrams]:
    #         print(f"{anagrams}: {anagram}")
    #     print()