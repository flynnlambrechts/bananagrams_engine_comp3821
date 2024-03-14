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
    def __init__(self, mode = "sort"):
        self.root = TrieNode()
        self.mode = mode # forward, reverse or sort, default is sort
    # Inserts a word into the trie
    def insert(self, word: Word):
        s_word = self._order_word(word.word)
        
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
    def search(self, word: str):
        s_word = self._order_word(word)
        node = self.root
        for char in word.word:
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
    def all_subwords(self, base: str, anchor = ''):
        subwords = []
        count = 0
        node = self.root
        if self.mode == "sort":
            print("mode is sort")
            subwords.extend(self._recurse_subwords(node, base + anchor, anchor))
        else:
            if self.mode == "reverse":
                anchor = anchor[::-1] # reverse anchor for reverse
                # means that anchor "ING" gets all words ending with "ING"
            for char in anchor:
                node = node.children[char]
                count += 1
            print("mode is not sort")
            subwords.extend(self._recurse_subwords(node, base))

        count += subwords.pop()
        
        # if not anchor:
        #     for char in self.root.children.keys():
        #         if char in base:
        #             subwords.extend(self._recurse_subwords(self.root.children[char], base.replace(char, "", 1)))
        #             count += subwords.pop()
        # else:
        #     for char in anchor
        #     subwords.extend(self._recurse_subwords(self.root.children[anchor], base))

        # subwords.append(count)
        return subwords
    
    # The recursive part of all_subwords
    def _recurse_subwords(self, node, subbase, anchor = ""):
        subwords = []
        if len(node.anagrams) > 0:
            if self._has_anchor(node.anagrams[0].word, anchor):
                subwords = node.anagrams[:]
        count = 1
        for char in node.children.keys():
            if char in subbase:
                subwords.extend(self._recurse_subwords(node.children[char], subbase.replace(char, "", 1), anchor))
                count += subwords.pop()
        subwords.append(count)
        return subwords
    
    def _has_anchor(self, word, anchor):
        remaining = word[:]
        for char in anchor:
            previous = remaining[:]
            remaining = remaining.replace(char, '', 1)
            if remaining == previous:
                return False
        return True

    def find_two_letters(self, char):
        node = self.root.children[char]
        words = []
        for char in node.children.keys():
            words.extend(node.children[char].anagrams)
        return words
    
    def _order_word(self, word):
        s_word = word[:].upper()
        if self.mode == "sort":
            s_word = ''.join(sorted(word.upper()))
        elif self.mode == "reverse":
            s_word = word[::-1].upper()
        return s_word