from src.game import Game
from src.board import Board
# from bananagrams_engine_comp3821.Classes.Trie import Trie
# from bananagrams_engine_comp3821.algorithm_functions import long_start_word

# s_trie = Trie("sort")
# s_trie.make_trie("Classes/word_dictionary.txt")

# game = Game()
# game.setup()
# print(game)
# print(game.hand)
# words = s_trie.all_subwords(game.hand)
# # word = long_start_word(words).word
# word = words[0].word
# print(f"word: {word}")
# game.play_word(word, 0, 0, 0, False)
# print(game)
# print(game.board.tiles[(0,0)].lims)
# print(game.board.tiles[(0,1)].lims)

# words = s_trie.find_two_letters("E")
# for word in words:
#     print(word.word)

def print_lims(board, coords: tuple):
    tile_lims = board.tiles[coords].lims.lims
    print(f"({coords[0]}, {coords[1]}): {tile_lims}")
    
def check_lims(board, coords: tuple, expected: list):
    lims = board.tiles[coords].lims.lims
    if lims == expected:
        return
    else:
        print(f"Error for {coords}: expected {expected}, got {lims}")   

def lims_test_1(print_more: bool = False):
    board = game.players[0].board
    board = Board()

    if print_more: print(board)
    board.add_word("EEEEE", 0, 0, 0)
    board.add_word("EEE", 0, 0, 1)
    board.add_word("EEE", 0, 4, 1)
    if print_more: print(board)

    tiles = [(0,0), (1,0), (2,0), (0,2)]
    expected_lims = [[0,0,50,50],[0,0,0,50],[50,2,0,50],[50,0,50,0]]
    for i in range(len(tiles)):
        check_lims(board, tiles[i], expected_lims[i])

def lims_test_2(print_more: bool = False):
    board = game.players[0].board
    board = Board()

    board.add_word("EEEE", 0, 0, 0)
    board.add_word("EEEE", 0, 3, 1)
    board.add_word("EEEEE", 0, 0, 1, True)
    board.add_word("EEE", -2, -1, 0)
    board.add_word("EEEE", 3, 2, 0)
    if print_more: print(board)

    tiles = [(0,0), (0,2), (1,3), (-4,0)]
    expected_lims = [[50,0,0,50],[0,0,1,0],[0,50,0,0],[0,50,50,50]]
    for i in range(len(tiles)):
        check_lims(board, tiles[i], expected_lims[i])

def lims_test_3(print_more: bool = False):
    board = game.players[0].board
    board = Board()
    board.add_tile("E", 0, 0)
    board.add_tile("E", -2, -1)
    board.add_tile("E", 1, 0)
    board.add_tile("E", 1, 3)
    if print_more: print(board)

    tiles = [(0,0), (-2,-1), (1,0), (1,3)]
    expected_lims = [[0,2,1,50],[1,50,50,50],[50,1,0,50],[50,50,50,1]]
    for i in range(len(tiles)):
        check_lims(board, tiles[i], expected_lims[i])

def lims_test_4(print_more: bool = False):
    board = game.players[0].board
    board = Board()

    board.add_word("EE", 0, 0, 0)
    board.add_word("EEEE", 0, 0, 1)
    if print_more: print(board)

    tiles = [(0,0), (0,1), (1,0)]
    expected_lims = [[0,0,50,50],[0,50,50,0],[0,0,0,50]]
    for i in range(len(tiles)):
        check_lims(board, tiles[i], expected_lims[i])

game = Game()
game.add_player()
board = game.players[0].board
print("\nTest 1")
lims_test_1(True)
print("\nTest 2")
lims_test_2(True)
print("\nTest 3")
lims_test_3(True)
print("\nTest 4")
lims_test_4(True)