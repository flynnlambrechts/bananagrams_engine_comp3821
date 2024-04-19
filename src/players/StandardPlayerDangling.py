from players.StandardPlayer import StandardPlayer
from constants import letter_count
class StandardPlayerDangling(StandardPlayer):

    def __init__(self, game, id: int, word_scorer) -> None:
        super().__init__(game, id, word_scorer=word_scorer)
        self.hand_at_last_restructure = ''

    def play_turn(self):
        self.show_board()
        return super().play_turn()

    def peel(self):
        self.hand_at_last_restructure = ''
        return super().peel()

    def restructure_board(self):
        self.show_board()
        dangling_tiles = self.board.remove_dangling()
        if sorted(self.hand) == self.hand_at_last_restructure:
            worst_letter_in_hand = min(
                self.hand, key=lambda char: letter_count[char])
            self.game.dump(self, worst_letter_in_hand)
            if len(self.hand_at_last_restructure) == len(self.hand):
                exit(1)
        if len(dangling_tiles) == 0:
            exit(1)
            return super().restructure_board()

        else:
            old_hand = self.hand
            for tile in dangling_tiles:
                self.hand += tile.char
            self.hand_at_last_restructure = sorted(self.hand)
            self.speak("DANGLING", f"Found {len(dangling_tiles)} dangling tiles, old_hand={old_hand}, new_hand={self.hand}")
            self.play_turn()