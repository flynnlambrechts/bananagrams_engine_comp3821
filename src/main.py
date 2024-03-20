from Game.Game import Game
from Algorithm.Trie.Trie import Trie
from Algorithm.algorithm_functions import long_with_lowest_rank
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
print('[Finding Word]')
start_word: Word = long_with_lowest_rank(all_words.all_subwords(game.hand))
print(f'[Playing] "{start_word}"')
game.play_word(str(start_word), row=0, col=0, direction=0)
anchors += [game.board.tiles[(0, 0)],
            game.board.tiles[(0, len(str(start_word)) - 1)]]

print(game)

print('[Finding Word]')
try:
    current_word = long_with_lowest_rank(all_words.all_subwords(
        game.hand, ''.join([anchor.char for anchor in anchors])))
except ValueError:
    print('[ERROR] Could not find any subwords')
    exit()

print(f'[Playing] "{current_word}"')
# Find which anchor is being used and play the word there
for tile in anchors:
    if tile.char not in str(current_word):
        continue
    i = str(current_word).index(tile.char)
    game.play_word(str(current_word),
                   row=tile.coords[0] - i, col=tile.coords[1], direction=1)
    break

print(game)
