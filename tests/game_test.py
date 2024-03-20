from src.Game.Game import Game
from src.Algorithm.Trie.Trie import Trie

trie = Trie()
trie.parse_file("word_dictionary.txt")

game = Game()
game.setup()
print(game)
print(game.hand)
words = trie.all_subwords(game.hand)
print(f"word: {words[0].string}")
game.play_word(words[0].string, 0, 0, 0, False)
print(game)
words = trie.find_two_letters("E")
for word_string in words:
    print(word_string)
