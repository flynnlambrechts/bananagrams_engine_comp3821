from board.board import Board
from algorithms import where_to_play_word
from utils import add_tuple_elems
from pprint import pprint
from board.tile import Tile
from pathlib import Path
from constants import VERTICAL, HORIZONTAL, NO_SPACE_FOR_WORD
import multiprocessing
from word import Word
from ScoreWordStrategies.score_word_strategy import ScoreWordStrategy
from ScoreWordStrategies.score_word_simple_stranding import ScoreWordSimpleStranding
import pickle
from pprint import pprint


class Player:
    '''
    Player class manages a board and a hand
    '''

    def __init__(self, game, id: int, word_scorer=ScoreWordSimpleStranding()) -> None:
        self.name = f'{type(self).__name__} {id}'
        self.playing = False
        self.game = game
        self.board_attempt = 0
        self.board = Board()
        self.word_scorer = word_scorer

        # Player waits until game gives them their hand
        self.hand: str = ''

    def show_board(self):
        self.speak("Board")
        print(str(self.board))

    def give_tiles(self, tiles: list[str]):
        tiles = ''.join(tiles)
        self.hand += ''.join(tiles)
        self.speak(f"Got", f"{tiles}, new hand: {self.hand}")

    def speak(self, subject, information=''):
        print(f"{self.name} {self.word_scorer.name}: [{
              subject.upper()}] {information}")

    def peel(self):
        self.game.lock.acquire()
        if len(self.hand) == 0:
            self.speak("Peel")
            if not self.game.peel():
                self.speak("Bananas", "I Won Here's My Board")
                self.show_board()

        self.game.lock.release()

    def play(self):
        while self.game.game_is_active:
            self.play_turn()

    def game_over(self):
        self.game_running = False
        self.speak("Finishing", f"Remaining tiles {self.hand}")

    def play_word(self, word_string, anchor: Tile = None, anchor_index=None, is_junk=False):
        '''
        Given a word string and an anchor tile, plays the word in the position as
        Determined by where_to_play_word. 
        Updates its hand. 
        board.add_word updates the anchor list for it. 
        '''
        # self.speak("PLAYING", word_string)
        reverse = False
        if anchor is not None:
            word_placement = where_to_play_word(word_string, anchor)

            if word_placement == NO_SPACE_FOR_WORD:
                print(self)
                print(f"want to play {word_string} at {repr(anchor)}")
                print(anchor.lims)
                raise Exception("No valid direction to play word")

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

        # self._update_hand(word_string, row, col, direction)
        new_tiles = self.board.add_word(
            word_string, row, col, direction, reverse, is_junk)
        print("new tiles:")
        pprint(new_tiles)
        self._update_hand(new_tiles)

        # Update anchors
        # remove the used anchor
        # this also covers the case where the
        # the used anchor overlaps the new word's
        # start or end
        # pprint(self.board.anchors)
        if anchor is not None:
            self.board.remove_anchor(anchor)
        # pprint(self.board.anchors)
        return new_tiles

    def _update_hand(self, tiles_played):
        for tile in tiles_played:
            self.hand = self.hand.replace(tile.char, '', 1)

    # def _update_hand(self, word_string, start_row, start_col, direction):
    #     # Take a snapshot of our hand in case we need to revert it
    #     original_hand = self.hand
    #     # print(f"updating hand... word: {word_string} hand: {self.hand}")
    #     # Calculate change in row and col based on `direction`
    #     d_row = int(direction == VERTICAL)
    #     d_col = int(direction == HORIZONTAL)

    #     char_index = 0
    #     for char in word_string:
    #         tile_coords = (start_row + d_row * char_index,
    #                        start_col + d_col * char_index)

    #         # If a character isn't in our hand and isn't
    #         # on the board
    #         if char not in self.hand and tile_coords not in self.board.tiles:
    #             # Restore our hand and raise an Error
    #             self.hand = original_hand
    #             raise ValueError(f'Tried to remove \"{word_string}\" from ' +
    #                              f'hand, but ran out of characters. {tile_coords} not on board')
    #         char_index += 1
    #         # Remove the char from our hand if it wasn't on the board
    #         if tile_coords not in self.board.tiles:
    #             self.hand = self.hand.replace(char, '', 1)

    def long_with_best_rank(
            self, words: list[Word],
            rank_strategy="strand", anchor: Tile = None, closeness_to_longest=0) -> Word:
        '''
        Finds a long subword with the lowest letter_ranking
        (Means that it uses letters that appear less in the dictionary),
        The heuristic can be changed to:
        use many letters that start/appear in short words or
        use many letters that cannot easily make short words

        closeness_to_longest determines the length of words relative to the longest word that can be considered
        '''

        words = [word for word in words if where_to_play_word(
            word.string, anchor) != NO_SPACE_FOR_WORD]

        if len(words) == 0:
            return None
        longest: Word = max(words, key=lambda word: len(word.string))

        long_words = [word for word in words if len(
            word.string) >= len(longest.string) - closeness_to_longest]
        if len(long_words) == 0:
            return None
        # rank_strategy string tracking strand should have deferred responsibility to word_scorer (make a new word scorer object)
        if rank_strategy == "strand":
            return max(long_words, key=lambda word: self.word_scorer.score_word(
                word.string, '', '' if anchor is None else anchor.char))
        else:
            return min(long_words, key=lambda word: word.letter_ranking / len(word.string))

    def __str__(self):
        player_str = f' - Hand: {self.hand}'
        board_str = str(self.board)
        if board_str:
            player_str += f'\n - Board:\n{board_str}'

        return player_str
