from pouch import letter_distribution
from board.tile import Tile


def _min_distribution(a, b):
    '''
    Maximum number of pairings of a and b given the letter distribution
    '''
    return min(letter_distribution[a], letter_distribution[b])


# Set of letters which form a two-letter-word with the key
two_letter_peers = {alpha: set() for alpha in letter_distribution.keys()}

# How many (non-unique) two-letter words the key can be a part of
letter_pair_frequency = {alpha: 0 for alpha in letter_distribution.keys()}

with open('../assets/word_dictionary.txt', 'r') as f:
    for line in f.readlines():
        # Preprocessing the line, skipping irrelevant words
        word = line.split()[0]
        if len(word) != 2:
            continue

        # Computing two_letter_peers
        two_letter_peers[word[0]].add(word[1])
        two_letter_peers[word[1]].add(word[0])

        # Computing letter_pair_frequency
        num_times = _min_distribution(word[0], word[1])
        letter_pair_frequency[word[0]] += num_times
        letter_pair_frequency[word[1]] += num_times

'''
j:  junk character
a:  anchor character

min_distribution(j, a)
- maximum number of pairings of `j` and `a`

letter_pair_frequency[a]
- number of non-unique letter words the anchor can be a part of

for j in letter_distribution.keys() for a in letter_distribution.keys()
- get every pair of alphas `j` and `a`

if j in two_letter_peers[a]
- skips cases of where `j` and `a` do not form a two letter word together


In other words, this dict, given a junk and then an anchor letter, returns the
proportion of two-letter words formed with the anchor letter which are formed
using the junk letter as well.

The higher the value, more desirable it is to match that junk letter to that
anchor.

TODO: Provide more meaningful variable name.
'''
junk_anchor_synergy = {(j, a): _min_distribution(
    j, a) / letter_pair_frequency[a] for j in letter_distribution.keys() for a in letter_distribution.keys() if j in two_letter_peers[a]}


def best_anchor_candidates(junk: str, anchors: list[Tile]):
    '''
    Assumes every anchor is a junk anchor
    '''
    # Candidates tuple format : (synergy_rating: float, anchor: Tile)
    candidates = [(junk_anchor_synergy[junk, a.char], a)
                  for a in anchors if a.char in two_letter_peers[junk]]

    # Anchors sorted by descending synergy
    return [t[1] for t in sorted(candidates, key=lambda t: -t[0])]
