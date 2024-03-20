from Game.Game import Game
from Algorithm.Trie.Trie import Trie
from Algorithm.algorithm_functions import find_start_word
from Algorithm.Trie.Word import Word

word_dictionary = 'word_dictionary.txt'

# Initialize our objecs
game = Game()
all_words = Trie(mode='sort', src=word_dictionary)
forward_words = Trie('forward', src=word_dictionary)
reverse_words = Trie('reverse', src=word_dictionary)

# List of tiles where new words can be added
anchors: list[str] = []

print(game)

# Find the first word, play it, and add its first and last characters/tiles
# to `anchors`
print('Finding starting word...')
start_word: Word = find_start_word(all_words.all_subwords(game.hand))
game.play_word(str(start_word), row=0, col=0, direction=0, reverse=False)
print(f'Playing "{start_word}"...')
anchors += [game.board.tiles[(0, 0)],
            game.board.tiles[(0, len(str(start_word)) - 1)]]

print(game)
