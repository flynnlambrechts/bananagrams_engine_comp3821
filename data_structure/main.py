from board import Board
VERTICAL = 1
HORIZONTAL = 0


board = Board()
board.add_word("HELLO", 1, 1, HORIZONTAL)
board.add_word("world", 2, 5, HORIZONTAL)
board.add_word("lower", 2, 8, VERTICAL)
board.add_word("partner", 6, 8, HORIZONTAL, reverse=True)
board.add_word("watermelon",4, 8, HORIZONTAL)

print(board)

