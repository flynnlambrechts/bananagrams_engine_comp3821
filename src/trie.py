from board.lims import Lims
from word import Word
from constants import letter_count


class TrieNode:
    def __init__(self):
        self.children = {}
        self.anagrams = []
        self.is_end = False


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
        node.is_end = True
        word.letter_ranking = word_val
        node.anagrams.append(word)

    def search(self, word_str):
        '''
        Returns true if a given word is in the Trie
        '''
        s_word = self._order_word(word_str)

        # this is unused but looks broken
        node = self._root
        for char in s_word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.anagrams
    
    def is_word(self, word_str):
        s_word = self._order_word(word_str)
        
        node = self._root
        for char in s_word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

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

    def find_two_letters(self, char: str, base: str = ''):
        words = []
        if self._mode == "sort":
            if base == '':
                base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for base_char in base:
                word_key = ''.join(sorted(base_char + char))
                if word_key[0] in self._root.children.keys():
                    node = self._root.children[word_key[0]]
                    if word_key[1] in node.children.keys():
                        words.extend(node.children[word_key[1]].anagrams)
        else:
            node = self._root.children[char]
            if base == '':
                node_list = node.children.keys()
            else:
                node_list = base
            for char in node_list:
                words.extend(node.children[char].anagrams)
        return words

    def _order_word(self, word_string: str):
        s_word = word_string[:].upper()
        if self._mode == "sort":
            s_word = ''.join(sorted(word_string.upper()))
        elif self._mode == "reverse":
            s_word = word_string[::-1].upper()
        return s_word
