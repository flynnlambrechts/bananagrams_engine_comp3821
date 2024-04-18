from players.StandardPlayer import StandardPlayer

class StandardPlayerDangling(StandardPlayer):
    # def play_turn(self):
    #     self.show_board()
    #     return super().play_turn()
    
    def restructure_board(self):
        self.show_board()
        dangling_tiles = self.board.remove_dangling()
        self.show_board()
        if len(dangling_tiles) == 0:
            return super().restructure_board()
            
        else:
            old_hand = self.hand
            for tile in dangling_tiles:
                self.hand += tile.char

            self.speak("DANGLING", f"Found {len(dangling_tiles)} dangling tiles, old_hand={old_hand}, new_hand={self.hand}")
            self.play_turn()
