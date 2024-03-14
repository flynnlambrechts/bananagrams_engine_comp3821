from Game_Structure.game import Game
from Classes.trie import Trie
from .run_algorithm import long_start_word

game = Game()
game.setup()

trie = Trie()
trie.make_trie("Classes/word_dictionary.txt")

anchors = []
start_word = long_start_word(trie.all_subwords(game.hand))
anchors.append(start_word[0])
anchors.append(start_word[-1])
game.play_word(start_word, 0, 0, 0, False)

next_word = long_start_word(trie.all_subwords(game.hand + anchors[0]))

anchor_pos = next_word.find(anchors[0])


game.play_word(next_word, 0, 0, 1, False)

"""
Prioritisation for next word:
- two letter word stack
- common first/last letter
- anything with the first/last letter as seed
"""
