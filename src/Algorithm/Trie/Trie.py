from .Word import Word
from .TrieNode import TrieNode
import os

letter_count = {'A': 196745, 'B': 47310, 'C': 102008, 'D': 85376, 'E': 287058, 'F': 30331,
                'G': 71315, 'H': 63613, 'I': 229895, 'J': 4240, 'K': 23873, 'L': 133085,
                'M': 73708, 'N': 170300, 'O': 168711, 'P': 76371, 'Q': 4301, 'R': 177701,
                'S': 245015, 'T': 165990, 'U': 84212, 'V': 23418, 'W': 19567, 'X': 7216,
                'Y': 41123, 'Z': 12279}


class Trie:
    def __init__(self, mode="sort"):
        self._root = TrieNode()
        self._mode = mode  # forward, reverse or sort, default is sort
    # Inserts a word into the trie

    def insert(self, word: Word):
        s_word = self._order_word(word.word_string)

        node = self._root
        word_val = 0
        for char in s_word:
            word_val += letter_count[char]
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        word.letter_ranking = word_val
        node.anagrams.append(word)

    # Returns true if a given word is in the Trie
    def search(self, word: Word):
        # s_word = self._order_word(word)
        node = self._root
        for char in word.word_string:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.anagrams

    # Makes a trie out of a given text file (line by line)
    def make_trie(self, file_name: str):
        print(os.getcwd())
        # Currently dictionary must be located in ./Dictionaries, once we sort
        # out the project structure with some kind of tests library then we can remove the
        # requirement and get passed in other directories (There's not really any reason to store
        # the dictionaries outside of ./Dictionaries anyway though)
        with open(
            os.path.dirname((os.path.relpath(__file__))) + "/Dictionaries/" + file_name, "r"
        ) as file:
            lines = file.readlines()
            for line in lines:
                self.insert(Word(line))

    # Returns an array of every anagram that can be made using the letters in base.
    # Note that the last item in the array is the count of how many nodes it visited.
    def all_subwords(self, base: str, anchor: str = '') -> list[Word]:
        subwords: list[Word] = []
        count = 0
        node = self._root
        if self._mode == "sort":
            print("mode is sort")
            subwords.extend(self._recurse_subwords(node, base + anchor, anchor))
        else:
            if self._mode == "reverse":
                anchor = anchor[::-1]  # reverse anchor for reverse
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
        #             subwords.extend(
        # self._recurse_subwords(self.root.children[char], base.replace(char, "", 1)))
        #             count += subwords.pop()
        # else:
        #     for char in anchor:
        #         subwords.extend(self._recurse_subwords(self.root.children[anchor], base))

        # subwords.append(count)
        return subwords

    # The recursive part of all_subwords
    def _recurse_subwords(self, node: TrieNode, subbase: str, anchor: str = "") -> list[Word]:
        subwords: list[Word] = []
        if len(node.anagrams) > 0:
            if self._has_anchor(node.anagrams[0], anchor):
                subwords = node.anagrams[:]
        count = 1
        for char in node.children.keys():
            if char in subbase:
                subwords.extend(
                    self._recurse_subwords(
                        node.children[char],
                        subbase.replace(char, "", 1),
                        anchor))
                count += subwords.pop()
        subwords.append(count)
        return subwords

    def _has_anchor(self, word: Word, anchor: str) -> bool:
        return word.has_anchor(anchor)

    def find_two_letters(self, char: str):
        node = self._root.children[char]
        words = []
        for char in node.children.keys():
            words.extend(node.children[char].anagrams)
        return words

    def _order_word(self, word_string: str):
        s_word = word_string[:].upper()
        if self._mode == "sort":
            s_word = ''.join(sorted(word_string.upper()))
        elif self._mode == "reverse":
            s_word = word_string[::-1].upper()
        return s_word