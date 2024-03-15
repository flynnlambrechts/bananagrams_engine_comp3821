from Game_Structure.game import Game
from Classes.trie import Trie
from run_algorithm import long_start_word

s_trie = Trie("sort")
s_trie.make_trie("Classes/word_dictionary.txt")

game = Game()
game.setup()
print(game)
print(game.hand)
words = s_trie.all_subwords(game.hand)
# word = long_start_word(words).word
word = words[0].word
print(f"word: {word}")
game.play_word(word, 0, 0, 0, False)
print(game)
print(game.board.tiles[(0,0)].lims)
print(game.board.tiles[(0,1)].lims)

# words = s_trie.find_two_letters("E")
# for word in words:
#     print(word.word)