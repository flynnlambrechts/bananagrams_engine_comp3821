import json

letter_count = {'A': 196745, 'B': 47310, 'C': 102008, 'D': 85376, 'E': 287058, 'F': 30331, 'G': 71315,
 'H': 63613, 'I': 229895, 'J': 4240, 'K': 23873, 'L': 133085, 'M': 73708, 'N': 170300,
 'O': 168711, 'P': 76371, 'Q': 4301, 'R': 177701, 'S': 245015, 'T': 165990, 'U': 84212,
 'V': 23418, 'W': 19567, 'X': 7216, 'Y': 41123, 'Z': 12279}

class TrieNode:
    def __init__(self):
        self.children = {}
        self.anagrams = []

class Word:
    
    def __init__(self, line):
        line_split = line.split(' ')
        self.word = line_split[0]
        self.num_startswith = int(line_split[1])
        self.num_endswith = int(line_split[2])
        self.letter_ranking = 0
    
    def get_word(self):
        return self.word
    
    def get_num_startswith(self):
        return self.num_startswith
    
    def get_num_endswith(self):
        return self.num_endswith
    
    def get_letter_rank(self):
        return self.letter_ranking
    
    def set_letter_rank(self, rank):
        self.letter_ranking = rank

# Trie with standard operations plus a recursive search of 
# all anagrams that use some of the given letters
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        s_word = sort_word(word.get_word())
        node = self.root
        word_val = 0
        for char in s_word:
            word_val += letter_count[char]
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        word.set_letter_rank(word_val)
        node.anagrams.append(word)

    def search(self, word):
        node = self.root
        for char in word.get_word:
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
        count = 0
        for char in self.root.children.keys():
            if char in base:
                subwords.extend(self._recurse_subwords(self.root.children[char], base.replace(char, "", 1)))
                count += subwords.pop()
        # subwords.append(count)
        return subwords
    
    def _recurse_subwords(self, node, subbase):
        subwords = node.anagrams[:]
        count = 1
        for char in node.children.keys():
            if char in subbase:
                subwords.extend(self._recurse_subwords(node.children[char], subbase.replace(char, "", 1)))
                count += subwords.pop()
        subwords.append(count)
        return subwords

# Adds words to the python dictionary, equivalent to a hash
def add_word_hash(hash_dict, word):
    s_word = sort_word(word)
    if s_word in hash_dict.keys():
        hash_dict[s_word].append(word)
    else:
        hash_dict[s_word] = [word]

# Sorts and capitalises a string
def sort_word(word):
    return ''.join(sorted(word.upper()))

# Makes a trie out of a given file (line by line)
def make_trie(trie, file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            trie.insert(Word(line))

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

# Yet to find an easy way to save the trie. 
# It's not so easy to convert to json
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