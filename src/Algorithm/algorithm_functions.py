from Algorithm.Trie.Word import Word
from .Trie.Trie import Trie


def run_algorithm(base: str, trie: Trie):
    subwords = trie.all_subwords(base)
    start_word = find_start_word(subwords)
    print(str(start_word), start_word.letter_ranking)


# Finds a long subword with the lowest letter_ranking
# (Means that it uses letters that appear less in the dictionary),
# The heuristic can be changed to:
# use many letters that start/appear in short words or
# use many letters that cannot easily make short words
def find_start_word(subwords):
    longest: list[Word] = max(subwords, key=lambda word: len(word.string))

    long_subwords = []
    for word in subwords:
        if len(str(word)) >= len(str(longest)) - 3:
            long_subwords.append(word)

    min_word = min(long_subwords, key=lambda word: word.letter_ranking)
    return min_word
