from board.board import Board

from algorithms import where_to_play_word, get_dangling_tiles
from utils import add_tuple_elems

from board.tile import Tile
from pathlib import Path
from constants import VERTICAL, HORIZONTAL, NO_SPACE_FOR_WORD
from pickle_manager import load_tries


class Player:
    '''
    Player class manages a board and a hand
    '''
    counter = 0
    
    # Initialize our objects
    this_directory = Path(__file__).parent.resolve()
    dictionary = this_directory / '..' / '..' / 'assets' / 'word_dictionary.txt'
    print('[Initializing]')
    all_words, forward_words, reverse_words = load_tries()

    def __init__(self, game) -> None:
        Player.counter += 1
        self.name = f"{type(self).__name__} {Player.counter}"
        self.playing = False
        self.game = game
        self.board_attempt = 0
        self.board = Board()

        # Player waits until game gives them their hand
        self.hand: str = ''


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
        self.hand += ''.join(tiles)
        self.speak(f"Got", f"{tiles}, new hand: {self.hand}")

    def speak(self, subject, information=''):
        print(f"{self.name}: [{subject.upper()}] {information}")

    def peel(self):
        self.game.lock.acquire()
        if (self.hand == ""):
            self.speak("Peel")
            if not self.game.peel():
                self.speak("Bananas", "I Won Here's My Board")
                self.show_board()
                # get_dangling_tiles(self.board)
                
        self.game.lock.release()

    def play(self):
        while self.game.game_is_active:
            self.play_turn()

    def game_over(self):
        self.game_running = False
        self.speak("Finishing", f"Remaining tiles {self.hand}")

    def play_word(self, word_string, anchor:Tile=None, anchor_index = None, is_junk = False):
        # print("playing", word_string, "anchor:", anchor)
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
                print(self)
                print(f"want to play {word_string} at {anchor}")
                print(anchor.lims)
                raise Exception("No valid direction to play word")
            else:
                (i, direction) = word_placement
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
        new_tiles = self.board.add_word(word_string, row, col, direction, reverse, is_junk)

        # Update anchors
        # remove the used anchor
        # this also covers the case where the
        # the used anchor overlaps the new word's
        # start or end
        if anchor is not None:
            self.board.remove_anchor(anchor)

        return new_tiles

    def _update_hand(self, word_string, start_row, start_col, direction):
        # Take a snapshot of our hand in case we need to revert it
        original_hand = self.hand
        # print(f"updating hand... word: {word_string} hand: {self.hand}")
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
