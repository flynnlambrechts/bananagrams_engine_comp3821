from Game_Structure.game import Game
from Classes.trie import Trie

trie = Trie()
trie.make_trie("Classes/word_dictionary.txt")

game = Game()
game.setup()
print(game)
print(game.hand)
words = trie.all_subwords(game.hand)
print(f"word: {words[0].get_word()}")
game.play_word(words[0].get_word(), 0, 0, 0, False)
print(game)