from Game_Structure.game import Game
from Classes.trie import Trie
from .run_algorithm import long_start_word

game = Game()
game.setup()

all_words = Trie("sort")
forward_words = Trie("forward")
reverse_words = Trie("reverse")
all_words.make_trie("Classes/word_dictionary.txt")
forward_words.make_trie("Classes/word_dictionary.txt")
reverse_words.make_trie("Classes/word_dictionary.txt")

anchors = []
start_word = long_start_word(all_words.all_subwords(game.hand))

game.play_word(start_word, 0, 0, 0, False)
anchors.append(game.board.tiles[(0,0)])
anchors.append(game.board.tiles[(0,len(start_word) - 1)])

next_word = long_start_word(all_words.all_subwords(game.hand + anchors[0]))

"""
Given an anchor:
Find its two letter words
"""

anchor_pos = next_word.find(anchors[0])


game.play_word(next_word, 0, 0, 1, False)

"""
Prioritisation for next word:
- two letter word stack
- common first/last letter
- anything with the first/last letter as seed
"""



def two_letter_find(anchor, hand, direction):
    twos = all_words.find_two_letters(anchor)
    pair_chars = []
    for word in twos:
        char = word.word.replace(anchor, '', 1)
        if char in hand:
            pair_chars.append(char)
    trie = forward_words
    if direction == "reverse":
        trie = reverse_words
    best_words = []
    for char in pair_chars:
        best_words.append(long_start_word(trie.all_subwords(hand.replace(char, '', 1), char)))
    
    best = min(best_words, key = lambda word: word.letter_ranking/len(word))
    return best

def corner_find(anchor, hand, direction):
    trie = forward_words
    if direction == "reverse":
        trie = reverse_words
    return long_start_word(trie.all_subwords(hand, anchor))
    # todo: rate words based on maximising the average score in the remaining hand
    # plus something for general length
    
    # future work: start monte carloing within a certain point????

