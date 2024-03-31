from lims import Lims
from word import Word

letter_count = {'A': 196745, 'B': 47310, 'C': 102008, 'D': 85376, 'E': 287058, 'F': 30331,
                'G': 71315, 'H': 63613, 'I': 229895, 'J': 4240, 'K': 23873, 'L': 133085,
                'M': 73708, 'N': 170300, 'O': 168711, 'P': 76371, 'Q': 4301, 'R': 177701,
                'S': 245015, 'T': 165990, 'U': 84212, 'V': 23418, 'W': 19567, 'X': 7216,
                'Y': 41123, 'Z': 12279}


class TrieNode:
    def __init__(self):
        self.children = {}
        self.anagrams = []


class Trie:
    def __init__(self, mode="sort", dictionary_path=None):
        self._root = TrieNode()
        self._mode = mode  # forward, reverse or sort, default is sort

        if dictionary_path:
            self.parse_dictionary(dictionary_path)

    def insert(self, word: Word):
        '''
        Inserts a word into the trie
        '''
        s_word = self._order_word(word.string)

        node = self._root
        word_val = 0
        for char in s_word:
            word_val += letter_count[char]
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        word.letter_ranking = word_val
        node.anagrams.append(word)

    def search(self, word: Word):
        '''
        Returns true if a given word is in the Trie
        '''
        # s_word = self._order_word(word)
        node = self._root
        for char in word.string:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.anagrams

    def parse_dictionary(self, dictionary_path: str):
        '''
        Makes a trie out of a given text file (line by line). The
        caller must provide the location of the dictionary file.
        '''
        with open(dictionary_path) as file:
            lines = file.readlines()
            for line in lines:
                self.insert(Word(line))

    def all_subwords(
            self, base: str, anchor: str = '', lims: Lims = Lims([50, 50, 50, 50])) -> list[Word]:
        '''
        Returns an array of every anagram that can be made using the letters
        in base.

        Note: the last item in the array is the count of how many nodes 
        it visited.

        Don't include anchor in the base string.
        '''
        subwords: list[Word] = []
        count = 0
        node = self._root
        if self._mode == "sort":
            subwords.extend(self._recurse_subwords(
                node, base + anchor, anchor))
        else:
            if self._mode == "reverse":
                anchor = anchor[::-1]  # reverse anchor if reverse
                # means that anchor "ING" gets all words ending with "ING"
            for char in anchor:
                node = node.children[char]
                count += 1
            subwords.extend(self._recurse_subwords(node, base))

        count += subwords.pop()

        return subwords

    def _recurse_subwords(self, node: TrieNode, subbase: str, anchor: str = "") -> list[Word]:
        '''
        The recursive part of all_subwords
        '''
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
