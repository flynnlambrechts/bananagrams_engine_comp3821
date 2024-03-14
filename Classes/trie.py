from .word import Word

letter_count = {'A': 196745, 'B': 47310, 'C': 102008, 'D': 85376, 'E': 287058, 'F': 30331, 'G': 71315,
 'H': 63613, 'I': 229895, 'J': 4240, 'K': 23873, 'L': 133085, 'M': 73708, 'N': 170300,
 'O': 168711, 'P': 76371, 'Q': 4301, 'R': 177701, 'S': 245015, 'T': 165990, 'U': 84212,
 'V': 23418, 'W': 19567, 'X': 7216, 'Y': 41123, 'Z': 12279}

class TrieNode:
    def __init__(self):
        self.children = {}
        self.anagrams = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Inserts a word into the trie
    def insert(self, word):
        s_word = ''.join(sorted(word.get_word().upper()))
        node = self.root
        word_val = 0
        for char in s_word:
            word_val += letter_count[char]
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        word.set_letter_rank(word_val)
        node.anagrams.append(word)

    # Returns true if a given word is in the Trie
    def search(self, word):
        node = self.root
        for char in word.get_word():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.anagrams

    # Makes a trie out of a given text file (line by line)
    def make_trie(self, file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
            for line in lines:
                self.insert(Word(line))

    # Returns an array of every anagram that can be made using the letters in base.
    # Note that the last item in the array is the count of how many nodes it visited. 
    def all_subwords(self, base):
        subwords = []
        count = 0
        for char in self.root.children.keys():
            if char in base:
                subwords.extend(self._recurse_subwords(self.root.children[char], base.replace(char, "", 1)))
                count += subwords.pop()
        # subwords.append(count)
        return subwords
    
    # The recursive part of all_subwords
    def _recurse_subwords(self, node, subbase):
        subwords = node.anagrams[:]
        count = 1
        for char in node.children.keys():
            if char in subbase:
                subwords.extend(self._recurse_subwords(node.children[char], subbase.replace(char, "", 1)))
                count += subwords.pop()
        subwords.append(count)
        return subwords