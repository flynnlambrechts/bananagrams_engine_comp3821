from src.algorithms import anchor_ranking
from src.game import Game

game = Game()
game.add_player()
board = game.players[0].board

board.add_word("EEEEE", 0, 0, 0)
board.add_word("EEE", 0, 0, 1)
board.add_word("EEE", 0, 4, 1)

print(board)

print(anchor_ranking(board.tiles))