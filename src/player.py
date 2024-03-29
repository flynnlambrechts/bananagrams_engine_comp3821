from board import Board
from pathlib import Path
from trie import Trie
from algorithms import long_with_best_rank, where_to_play_word, score_word_simple_stranding
from word import Word
from tile import Tile
from constants import VERTICAL, HORIZONTAL, NO_SPACE_FOR_WORD, MAX_LIMIT

is_prefix_of = {'A': 16194, 'B': 15218, 'C': 25015, 'D': 16619, 'E': 11330, 'F': 10633, 'G': 9351, 'H': 10524, 'I': 9604, 'J': 2311, 'K': 3361, 'L': 8058, 'M': 15811, 'N': 6564, 'O': 8895, 'P': 24327, 'Q': 1411, 'R': 15014, 'S': 31986, 'T': 14563, 'U': 9522, 'V': 4590, 'W': 5921, 'X': 309, 'Y': 1036, 'Z': 1159}
is_suffix_of = {'A': 5560, 'B': 371, 'C': 6121, 'D': 25039, 'E': 28261, 'F': 534, 'G': 20216, 'H': 3293, 'I': 1601, 'J': 12, 'K': 2327, 'L': 8586, 'M': 4620, 'N': 12003, 'O': 1887, 'P': 1547, 'Q': 10, 'R': 14784, 'S': 107294, 'T': 13933, 'U': 379, 'V': 45, 'W': 610, 'X': 583, 'Y': 19551, 'Z': 159}
pair_start_count = {'A': 16, 'B': 5, 'C': 1, 'D': 4, 'E': 13, 'F': 3, 'G': 3, 'H': 5, 'I': 6, 'J': 2, 'K': 4, 'L': 3, 'M': 7, 'N': 5, 'O': 17, 'P': 4, 'Q': 1, 'R': 1, 'S': 4, 'T': 4, 'U': 8, 'V': 0, 'W': 2, 'X': 2, 'Y': 4, 'Z': 3}
pair_end_count = {'A': 15, 'B': 2, 'C': 0, 'D': 4, 'E': 15, 'F': 3, 'G': 2, 'H': 6, 'I': 14, 'J': 0, 'K': 1, 'L': 2, 'M': 6, 'N': 5, 'O': 17, 'P': 2, 'Q': 0, 'R': 4, 'S': 5, 'T': 5, 'U': 6, 'V': 0, 'W': 3, 'X': 3, 'Y': 7, 'Z': 0}

class Player:

    '''
    Player class manages a board and a hand
    '''

    def __init__(self, game) -> None:
        self.name = "Player"
        self.playing = False
        self.game = game

        self.board = Board()

        # Player waits until game gives them their hand
        self.hand: str = ''

        # Initialize our objects
        this_directory = Path(__file__).parent.resolve()
        dictionary = this_directory / '..' / 'assets' / 'word_dictionary.txt'
        print(f'[Initializing]')
        self.all_words = Trie(mode='sort', dictionary_path=dictionary)
        self.forward_words = Trie('forward', dictionary_path=dictionary)
        self.reverse_words = Trie('reverse', dictionary_path=dictionary)

    def __str__(self):
        player_str = f' - Hand: {self.hand}'
        board_str = str(self.board)
        if board_str:
            player_str += f'\n - Board:\n{board_str}'

        return player_str

    def show_board(self):
        self.speak("Board")
        print(str(self.board))

    def give_tiles(self, tiles: list[str]):
        tiles = ''.join(tiles)
        self.speak(f"Got", tiles)
        self.hand += ''.join(tiles)

    def speak(self, subject, information=''):
        print(f"{self.name}: [{subject}] {information}")

    def play(self):
        while True:
            self.play_turn()

    def play_first_turn(self):
        # Find the first word, play it, and add its first and last characters/tiles
        # to `anchors`
        start_word: Word = long_with_best_rank(self.all_words.all_subwords(self.hand), 
                                               rank_strategy = "strand",
                                               closeness_to_longest = 2)
        
        self.speak("Playing", start_word)
        self.play_word(str(start_word))
        self.show_board()
        # self.anchors += [self.board.tiles[(0, 0)], self.board.tiles[(0, len(str(start_word)) - 1)]]

    def play_turn(self):
        print("")
        # Peel if hand is empty
        if len(self.hand) == 0:
            # print('Peel!')
            self.game.peel()

        # If this is the first turn the player acts differently
        if not self.playing:
            self.playing = True
            self.play_first_turn()
            return

        # Otherwise generic implementation of play turn
        self.speak('Finding Word', f"available letters {self.hand}")

        # strand_anchors = filter(, self.board.anchors)

        # strand_candidate = 


        # Precompute string repesentation of anchors
        anchor_str = ''.join([anchor.char for anchor in self.board.anchors])
        # Words that can be formed using an anchor
        word_candidates: tuple[Word, Tile] = []
        for anchor in self.board.anchors:
            # Looping over anchors to see if the hand+anchor can make a word
            word = long_with_best_rank(self.all_words.all_subwords(
                self.hand, anchor.char, anchor.lims), rank_strategy="old", anchor= anchor)

            if word is not None and word.has_anchor(anchor.char):
                word_candidates.append((word, anchor))
        self.speak("Found", f"{len(word_candidates)} word candidates")

        if len(word_candidates) == 0:
            print('[ERROR] Could not find next word')
            return self.restructure_board()
            

        # Very weird way of calculating the best next word and its
        # corresponding anchor
        word = long_with_best_rank([word for word, _ in word_candidates], rank_strategy="old")
        anchor = next(anchor for w, anchor in word_candidates if w == word)

        self.speak("Playing", f"{word} on anchor {anchor}")

        self.play_word(str(word), anchor)
        self.show_board()


    def restructure_board(self):
        '''If we cannot continue without our current board formation
        this function is called. It should made adjustments and try
        play a word again
        '''
        print("attempted board restructure")
        # TODO
        # return "Error"
        raise NotImplementedError("Board restructuring not implemented yet")

    def play_word(self, word_string, anchor:Tile=None):
        # print("playing", word_string)
        '''
        Given a word string and an anchor tile, plays the word in the position as
        Determined by where_to_play_word. 
        Updates its hand. 
        board.add_word updates the anchor list for it. 
        '''
        reverse = False
        if anchor is not None:
            word_placement = where_to_play_word(word_string, anchor)
            if word_placement == NO_SPACE_FOR_WORD:
                raise Exception("No valid direction to play word")
            else:
                (i, direction) = word_placement
                (row, col) = anchor.coords
                if direction == VERTICAL:
                    row -= i
                else:
                    col -= i
            # i = word_string.index(anchor.char)
            # last_index = len(word_string) - 1
            # lims = anchor.lims

            # if lims.down and lims.up:
            #     direction = VERTICAL
            # elif lims.right and lims.left:
            #     direction = HORIZONTAL
            # else:
            #     print(anchor.find_IOI())
            #     raise Exception("No valid direction to play word")

            # (row, col) = anchor.coords
            

        else:
            direction = HORIZONTAL

            i = 0
            row = 0
            col = 0

        self._update_hand(word_string, row, col, direction)
        new_tiles = self.board.add_word(word_string, row, col, direction, reverse)

        # Update anchors
        # remove the used anchor
        # this also covers the case where the
        # the used anchor overlaps the new word's
        # start or end
        if anchor is not None:
            self.board.remove_anchor(anchor)
            # print(f"Removing anchor {anchor}")
            # print(self.anchors)
            # print(self.anchors)
        return direction

    def _update_hand(self, word_string, start_row, start_col, direction):
        # Take a snapshot of our hand in case we need to revert it
        original_hand = self.hand

        # Calculate change in row and col based on `direction`
        d_row = int(direction == VERTICAL)
        d_col = int(direction == HORIZONTAL)

        char_index = 0
        for char in word_string:
            tile_coords = (start_row + d_row * char_index,
                           start_col + d_col * char_index)

            # If a character isn't in our hand and isn't
            # on the board
            if char not in self.hand and tile_coords not in self.board.tiles:
                # Restore our hand and raise an Error
                self.hand = original_hand
                raise ValueError(f'Tried to remove \"{word_string}\" from ' +
                                 'hand, but ran out of characters.')
            char_index += 1
            # Remove the char from our hand if it wasn't on the board
            if tile_coords not in self.board.tiles:
                self.hand = self.hand.replace(char, '', 1)

    def find_strand_extending_anchors(self):
        '''returns tiles that have infinite space in 1 direction and some space at 90 degrees'''
        strand_extending_anchors = []
        for tile in self.board.tiles.values():
            if tile.vert_parent == None:
                if (tile.lims.left == MAX_LIMIT or tile.lims.right == MAX_LIMIT) and (tile.lims.up > 0 or tile.lims.down > 0):
                    strand_extending_anchors.append(tile)
            elif (tile.lims.up == MAX_LIMIT or tile.lims.down == MAX_LIMIT) and (tile.lims.left > 0 or tile.lims.right > 0):
                strand_extending_anchors.append(tile)

        return strand_extending_anchors
    
    '''TODO: deal with nothing coming up'''
    def find_best_strand_extension(self, anchors: list[Tile]):
        prefix_anchors = set() # prefix of the new word
        suffix_anchors = set() # suffix of the new word

        for anchor in anchors:
            pair_list = self.all_words.find_two_letters(anchor.char)

            bad_dir = anchor.lims.lims.index(min(anchor.lims.lims))
            if bad_dir < 2:
                # the anchor is the first letter of a word
                # which means it's an anchor for a suffix of a new word
                for pair in pair_list:
                    if pair[pair.index(anchor.char) - 1] in self.hand:
                        suffix_anchors.add(pair[pair.index(anchor.char) - 1])
            else:
                for pair in pair_list:
                    if pair[pair.index(anchor.char) - 1] in self.hand:
                        prefix_anchors.add(pair[pair.index(anchor.char) - 1])

        for prefix in prefix_anchors:
            words = self.forward_words.all_subwords(self.hand.replace(prefix,'',1), prefix)
            longest: Word = max(words, key=lambda word: len(word.string))
            best_prefix: Word = max(words, key=lambda word: score_word_simple_stranding(word.string, len(longest.string)))
        for suffix in suffix_anchors:
            words = self.reverse_words.all_subwords(self.hand.replace(suffix,'',1), suffix)
            longest: Word = max(words, key=lambda word: len(word.string))
            best_suffix: Word = max(words, key=lambda word: score_word_simple_stranding(word.string, len(longest.string)))
        return max([best_prefix, best_suffix], 
                   key = lambda word: score_word_simple_stranding(word.string, 
                                                                  max(len(best_prefix.string), len(best_suffix.string))))