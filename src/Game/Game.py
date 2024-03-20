from .BananaPouch.BananaPouch import BananaPouch
from .Board.Board import Board


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.pouch = BananaPouch()

        # I believe this makes the  list of chars a string
        self.hand = ''.join(self.pouch.setup())

    # Play word function self._valid_word tries to remove each letter of the
    # word from hand
    # if it's able to remove each letter, then it did work. Currently,
    # cannot remove the anchor
    # letter from hand so it returns invalid if used with an anchor letter
    def play_word(self, word_string, row, col, direction, reverse):
        self._update_hand(word_string)  # Consider putting this in a try-except

        self.board.add_word(word_string, row, col, direction, reverse)

        # Peel if hand is empty
        if len(self.hand) == 0:
            # print('Peel!')
            self.pouch.peel()
            # TODO: If self.hand == -1, end the game

    def _update_hand(self, word_string):
        # Take a snapshot of our hand in case we need to revert it
        original_hand = self.hand

        for char in word_string:
            # If a character isn't in our hand
            if char not in self.hand:
                # Restore our hand and raise an Error
                self.hand = original_hand
                raise ValueError(f'Tried to remove "{word_string}" from ' +
                                 'hand, but ran out of characters.')

            # Remove the char from our hand
            self.hand.replace(char, '', 1)

    # Used to support print(Game) functionality
    def __str__(self) -> str:
        game_str = (
            '[Game Status]\n' +
            f' - Hand: {self.hand}' +
            f'\n - Tiles in pouch: {len(self.pouch.remaining)}'
        )

        board_str = str(self.board)
        if board_str:
            game_str += f'\n - Board:\n{board_str}'

        return game_str
