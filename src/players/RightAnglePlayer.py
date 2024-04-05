from players.StrandingPlayer import StrandingPlayer

class RightAnglePlayer(StrandingPlayer):
    def play_turn(self):
        # print("")
        # Peel if hand is empty
        if len(self.hand) == 0:
            self.peel()
        if not self.game.game_is_active:
                return

        # If this is the first turn the player acts differently
        if not self.playing:
            self.playing = True
            self.play_first_turn()
            return

        # Otherwise generic implementation of play turn
        # self.speak('Finding Word', f"available letters {self.hand}")

        strand_anchors = self.find_strand_extending_anchors()
        other_anchors = list(set(self.board.tiles.values()) - set(strand_anchors))
        
        if len(self.hand) < 5:
            self.speak("STRANDING", "hand is small. playing junk")
            self.play_junk(list(self.board.tiles.values()))
            if len(self.hand) > 0:
                return self.restructure_board()
            return

        if self.play_right_angle_word():
            self.speak("STRANDING", "playing right angle")
            return
        else:
            print("attempting to play junk because can't do anything else")
            self.play_junk(other_anchors)
            if len(self.hand) > 0:
                return self.restructure_board()
            return
