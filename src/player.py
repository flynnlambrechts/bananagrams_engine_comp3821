from board import Board
from pathlib import Path
from trie import Trie
from algorithms import long_with_lowest_rank
from word import Word
from tile import Tile
from constants import VERTICAL, HORIZONTAL

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
        
        # List of tiles where new words can be added
        self.anchors: list[Tile] = []

        # Initialize our objects
        this_directory = Path(__file__).parent.resolve()
        dictionary = this_directory / '..' / 'assets' / 'word_dictionary.txt'
        print(f'[Initializing]')
        self.all_words = Trie(mode='sort', dictionary_path=dictionary)
        self.forward_words = Trie('forward', dictionary_path=dictionary)
        self.reverse_words = Trie('reverse', dictionary_path=dictionary)

    def __str__(self):
        player_str =  f' - Hand: {self.hand}'
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
        start_word: Word = long_with_lowest_rank(self.all_words.all_subwords(self.hand))
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
        
        # Precompute string repesentation of anchors
        anchor_str = ''.join([anchor.char for anchor in self.anchors])
        # Words that can be formed using an anchor
        word_candidates: tuple[Word, Tile] = []
        for anchor in self.anchors:
            # Looping over anchors to see if the hand+anchor can make a word
            word = long_with_lowest_rank(
                self.all_words.all_subwords(self.hand + anchor.char, anchor_str))

            if word is not None and word.has_anchor(anchor.char):
                word_candidates.append((word, anchor))
        self.speak("Found", f"{len(word_candidates)} word candidates")
        

        
        if len(word_candidates) == 0:
            print('[ERROR] Could not find next word')
            self.restructure_board()
            return

        # Very weird way of calculating the best next word and its
        # corresponding anchor
        word = long_with_lowest_rank([word for word, _ in word_candidates])
        anchor = next(anchor for w, anchor in word_candidates if w == word)

        self.speak("Playing", f"{word} on anchor {anchor}")
        
        self.play_word(str(word), anchor)
        self.show_board()
        
        print("New anchors: ", self.anchors)
            
        
    def restructure_board(self):
        '''If we cannot continue without our current board formation
        this function is called. It should made adjustments and try
        play a word again
        '''
        # TODO
        raise NotImplementedError("Board restructuring not implemented yet")
    
    def play_word(self, word_string, anchor=None):
        '''
        Play word function self._valid_word tries to remove each letter of the
        word from hand
        if it's able to remove each letter, then it did work. Currently,
        cannot remove the anchor
        letter from hand so it returns invalid if used with an anchor letter
        '''
        reverse = False
        if anchor != None:
            print(anchor)
            print(word_string)
            i = word_string.index(anchor.char)
            last_index = len(word_string) - 1
            lims = anchor.find_lims()

            if lims.down() and lims.up():
                direction=VERTICAL
            elif lims.right() and lims.left():
                direction=HORIZONTAL
            else:
                print(anchor.find_lims())
                raise Exception("No valid direction to play word")
            
            (row, col) = anchor.coords
            if direction == VERTICAL:
                row -= i
            else:
                col -= i
                
        else:
            direction = HORIZONTAL
            
            i = 0
            row = 0
            col = 0

        self._update_hand(word_string, row, col, direction)
        end_tile = self.board.add_word(word_string, row, col, direction, reverse)
        self.anchors.append(self.board.tiles[(row, col)])
        self.anchors.append(end_tile)
            
        # Update anchors
        # remove the used anchor
        # this also covers the case where the
        # the used anchor overlaps the new word's
        # start or end
        if anchor != None:
            # print(f"Removing anchor {anchor}")
            # print(self.anchors)
            self.anchors = list(filter(lambda a: a.coords != anchor.coords, self.anchors))
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