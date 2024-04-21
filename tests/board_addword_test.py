from src.Game.Board.Board import Board
VERTICAL = 1
HORIZONTAL = 0


print("")

board2 = Board()
board2.add_word("EEE", 0, 4, 1)
print(board2)

print("")

board3 = Board()
board3.add_word("EEEEE", 0, 0, 0)
board3.add_word("EEE", 0, 0, 1)
board3.add_word("EEE", 0, 4, 1)
print(board3)

print("")

board = Board()
board.add_word("hello", 1, 1, HORIZONTAL)
board.add_word("world", 2, 5, HORIZONTAL)
board.add_word("lower", 2, 8, VERTICAL)
board.add_word("partner", 6, 8, HORIZONTAL, reverse=True)
board.add_word("watermelon", 4, 8, HORIZONTAL)

# print(board)
