from .BananaPouch.BananaPouch import BananaPouch
from .Board.Board import Board


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.pouch = BananaPouch()
        self.hand = ""

    def setup(self):
        self.hand = ''.join(self.pouch.setup())  # I believe this makes the list of chars a string

    # Play word function self._valid_word tries to remove each letter of the word from hand
    # if it's able to remove each letter, then it did work. Currently, cannot remove the anchor
    # letter from hand so it returns invalid if used with an anchor letter
    def play_word(self, word_string, row, col, direction, reverse):
        new_hand = self._valid_word(word_string)
        if new_hand != self.hand:  # and so the word is valid
            print("valid word!")
            self.hand = new_hand
            # TODO: check if the placement is legal
            self.board.add_word(word_string, row, col, direction, reverse)
            if self.hand == '':
                print("PEEL!!!")
                self.hand = self.pouch.peel()
                # TODO: if self.hand now = -1, end the game
        else:
            print("invalid word!")

    # Needs better name
    def _valid_word(self, word_string):
        remaining_hand = self.hand[:]
        for char in word_string:
            previous = remaining_hand[:]
            remaining_hand = remaining_hand.replace(char, '', 1)

            if remaining_hand == previous:
                return self.hand
        return remaining_hand

    def __str__(self) -> str:
        print(self.board)
        s = "\nHand: " + self.hand + '\n' + "No. of tiles in pouch:"
        s = s + str(len(self.pouch.remaining))
        return s
