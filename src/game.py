from pouch import Pouch
from board import Board


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.pouch = Pouch()
        self.hand = ''.join(self.pouch.setup())  # Convert list[str] to str

    def play_word(self, word_string, row, col, direction, reverse=False):
        '''
        Play word function self._valid_word tries to remove each letter of the
        word from hand
        if it's able to remove each letter, then it did work. Currently,
        cannot remove the anchor
        letter from hand so it returns invalid if used with an anchor letter
        '''

        self._update_hand(word_string, row, col, direction)
        self.board.add_word(word_string, row, col, direction, reverse)

        # Peel if hand is empty
        if len(self.hand) == 0:
            # print('Peel!')
            self.pouch.peel()
            # TODO: If self.hand == -1, end the game

    def _update_hand(self, word_string, start_row, start_col, direction):
        # Take a snapshot of our hand in case we need to revert it
        original_hand = self.hand

        # Calculate change in row and col based on `direction`
        d_row = int(direction == 1)
        d_col = int(direction == 0)

        char_index = 0
        for char in word_string:
            tile_coords = (start_row + d_row * char_index,
                           start_col + d_col * char_index)

            # If a character isn't in our hand and won't
            # use a tile that's already on the board
            if char not in self.hand and tile_coords not in self.board.tiles:
                # Restore our hand and raise an Error
                self.hand = original_hand
                raise ValueError(f'Tried to remove "{word_string}" from ' +
                                 'hand, but ran out of characters.')
            char_index += 1
            # Remove the char from our hand
            self.hand = self.hand.replace(char, '', 1)

    def __str__(self) -> str:
        '''
        Used to support print(Game) functionality
        '''

        game_str = (
            '[Game Status]\n' +
            f' - Hand: {self.hand}' +
            f'\n - Tiles in pouch: {len(self.pouch.remaining)}'
        )

        board_str = str(self.board)
        if board_str:
            game_str += f'\n - Board:\n{board_str}'

        return game_str
