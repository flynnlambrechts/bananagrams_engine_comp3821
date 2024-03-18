from src.Game.Game import Game
from src.Algorithm.Trie.Trie import Trie

trie = Trie()
trie.make_trie("word_dictionary.txt")

game = Game()
game.setup()
print(game)
print(game.hand)
words = trie.all_subwords(game.hand)
print(f"word: {words[0].word_string}")
game.play_word(words[0].word_string, 0, 0, 0, False)
print(game)
words = trie.find_two_letters("E")
for word_string in words:
    print(word_string)
