from players.StandardPlayer import StandardPlayer
from constants import letter_count


class StandardPlayerDangling(StandardPlayer):

    def __init__(self, game, id: int, word_scorer) -> None:
        super().__init__(game, id, word_scorer=word_scorer)
        self.previous_hands = []

    def play_turn(self):
        self.show_board()
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
