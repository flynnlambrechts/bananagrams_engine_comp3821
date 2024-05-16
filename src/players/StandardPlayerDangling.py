from .StandardPlayer import StandardPlayer
from ..constants import letter_count
import time


def board_to_object(board):
    result = []
    print(str(board))
    print(str(board.tiles))
    min_row = board.min_row()
    min_col = board.min_col()
    for (coords, tile) in board.tiles.items():
        coords = (coords[0] - min_row + 1, coords[1] - min_col + 1)
        result.append({"coords": coords, "letter": tile.char})
    return result


def get_game_state(game):
    cpu = game.players[0]
    player = game.players[1]
    state = {
        # "running": game.game_is_active,
        "cpu": {
            "board": board_to_object(cpu.board),
            "width": cpu.board.max_col() - cpu.board.min_col() + 1,
            "height": cpu.board.max_row() - cpu.board.min_row() + 1,
            "hand": [*cpu.hand],
        },
        # "player": {"hand": [*player.hand]},
    }
    return state

class StandardPlayerDangling(StandardPlayer):

    def __init__(self, game, id: int, word_scorer) -> None:
        super().__init__(game, id, word_scorer=word_scorer)
        self.previous_hands = []

    def play_turn(self):
        # self.show_board()
        # time.sleep(0.05)
        self.game.states.append(get_game_state(self.game))
        return super().play_turn()

    def peel(self):
        self.previous_hands = []
        return super().peel()

    def restructure_board(self):
        self.show_board()
        old_hand = self.hand
        dangling_tiles = self.board.remove_dangling()
        for tile in dangling_tiles:
            self.hand += tile.char
        post_removal_hand = sorted(self.hand)
        if any(prev_hand == post_removal_hand for prev_hand in self.previous_hands):
            self.speak("DANGLING", "Found a previous hand, now dumping")
            worst_letter_in_hand = min(
                self.hand, key=lambda char: letter_count[char])
            self.game.dump(self, worst_letter_in_hand)
            self.previous_hands = []
            if len(post_removal_hand) == len(self.hand):
                exit(1)
        elif len(dangling_tiles) == 0:
            exit(1)
            return super().restructure_board()

        else:
            self.previous_hands.append(sorted(self.hand))
            self.speak(
                "DANGLING",
                f"Found {len(dangling_tiles)} dangling tiles, old_hand={old_hand}, new_hand={self.hand}")
            self.play_turn()
