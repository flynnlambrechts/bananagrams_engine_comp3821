import pickle
from algorithms import get_dangling_tiles

with open('pickles/board.pkl', "rb") as f:
    board = pickle.load(f)
    print(str(board))
    get_dangling_tiles(board)