class TrieNode:
    def __init__(self):
        self.children = {}
        self.anagrams = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Inserts a word into the trie
    def insert(self, word):
        s_word = ''.join(sorted(word.upper()))
        node = self.root
        for char in s_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.anagrams.append(word)

    # Returns true if a given word is in the Trie
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.anagrams

    # Makes a trie out of a given text file (line by line)
    def make_trie(self, file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
            for line in lines:
                self.insert(line.strip())

    # Returns an array of every anagram that can be made using the letters in base.
    # Note that the last item in the array is the count of how many nodes it visited. 
    def all_subwords(self, base):
        subwords = []
        count = 0
        for char in self.root.children.keys():
            if char in base:
                subwords.extend(self._recurse_subwords(self.root.children[char], base.replace(char, "", 1)))
                count += subwords.pop()
        subwords.append(count)
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