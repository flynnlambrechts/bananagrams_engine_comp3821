from pathlib import Path
from game import Game
from trie import Trie
from algorithms import long_with_lowest_rank
from word import Word
from tile import Tile

this_directory = Path(__file__).parent.resolve()
dictinoary = this_directory / '..' / 'assets' / 'word_dictionary.txt'

# Initialize our objecs
print('[Initializing]')
game = Game()
all_words = Trie(mode='sort', dictionary_path=dictinoary)
forward_words = Trie('forward', dictionary_path=dictinoary)
reverse_words = Trie('reverse', dictionary_path=dictinoary)

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
# Precompute string repesentation of anchors
anchor_str = ''.join([anchor.char for anchor in anchors])
# Words that can be formed using an anchor
word_candidates: tuple[Word, Tile] = []
for anchor in anchors:
    # Looping over anchors to see if the hand+anchor can make a word
    word = long_with_lowest_rank(
        all_words.all_subwords(game.hand + anchor.char, anchor_str))

    if word is not None:
        word_candidates.append((word, anchor))

if len(word_candidates) == 0:
    print('[ERROR] Could not find next word')
    exit()

# Very weird way of calculating the best next word and its
# corresponding anchor
word = long_with_lowest_rank([word for word, _ in word_candidates])
anchor = next(anchor for w, anchor in word_candidates if w == word)

print(f'[Playing] "{word}"')
i = str(word).index(anchor.char)
game.play_word(str(word),
               row=anchor.coords[0] - i,
               col=anchor.coords[1],
               direction=1)

print(game)
