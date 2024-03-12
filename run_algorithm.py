from Dictionary.make_dict import *

def run_algorithm (base:str, trie:Trie):
    subwords = trie.all_subwords(base)
    start_word = long_start_word(subwords)
    print(start_word.get_word(), start_word.get_letter_rank())


# Finds a long subword with the lowest letter_ranking 
# (Means that it uses letters that appear less in the dictionary), The heuristic can be changed to:
# use many letters that start/appear in short words or use many letters that cannot easily make short words
def long_start_word(subwords):
    # Word[]
    longest = max(subwords, key=lambda word: len(word.get_word()))

    long_subwords = []
    for word in subwords:
        if len(word.get_word()) >= len(longest.get_word()) - 3:
            long_subwords.append(word)

    min_word = min(long_subwords, key=lambda word : word.get_letter_rank())
    return min_word
