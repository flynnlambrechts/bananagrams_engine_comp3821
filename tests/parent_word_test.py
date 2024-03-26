from src.game import Game
from src.parent_word import ParentWord
from src.constants import *
def print_lims(board, coords: tuple):
    tile_lims = board.tiles[coords].lims.lims
    print(f"({coords[0]}, {coords[1]}): {tile_lims}")
    
def check_words(board, coords: tuple, expected_v: ParentWord|None, expected_h: ParentWord|None):
    tile = board.tiles[coords]
    good = True
    if not (isinstance(tile.vert_parent, ParentWord) and isinstance(expected_v, ParentWord)):
        if tile.vert_parent != expected_v:
            good = False
    else:
        for attr in tile.vert_parent.__dict__:
            if getattr(expected_v, attr) != getattr(tile.vert_parent, attr):
                good = False
    
    if not (isinstance(tile.horo_parent, ParentWord) and isinstance(expected_h, ParentWord)):
        if tile.horo_parent != expected_h:
            good = False
    else:
        for attr in tile.horo_parent.__dict__:
            if getattr(expected_h, attr) != getattr(tile.horo_parent, attr):
                good = False
    if not good:
        print(f"Error for {coords}: \n\tv: [expected: {expected_v} got: {tile.vert_parent}] \n\th: [expected: {expected_h}], got: {tile.horo_parent}]")

def lims_test_1(print_more: bool = False):
    game = Game()
    game.add_player()
    board = game.players[0].board

    if print_more: print(board)
    board.add_word("TRUTH", 0, 0, 0)
    board.add_word("THE", 0, 0, 1)
    board.add_word("HER", 0, 4, 1)
    if print_more: print(board)

    tiles = [(0,0), (1,0), (2,0), (0,2)]
    expected_vert_ps = [ParentWord("THE", 0, VERTICAL),
                        ParentWord("THE", 1, VERTICAL),
                        ParentWord("THE", 2, VERTICAL),
                        None]
    expected_horo_ps = [ParentWord("TRUTH", 0, HORIZONTAL),
                        None,
                        None,
                        ParentWord("TRUTH", 2, HORIZONTAL)]
    for i in range(len(tiles)):
        check_words(board, tiles[i], expected_vert_ps[i], expected_horo_ps[i])

def lims_test_2(print_more: bool = False):
    game = Game()
    game.add_player()
    board = game.players[0].board    
    
    board.add_word("FOOD", 0, 0, 0)
    board.add_word("DOOR", 0, 3, 1)
    board.add_word("CHIEF", 0, 0, 1, True)
    board.add_word("PIN", -2, -1, 0)
    board.add_word("PROD", 3, 2, 0)
    if print_more: print(board)

    tiles = [(0,0), (-2,0), (3,2), (-4,0)]
    expected_vert_ps = [ParentWord("CHIEF", 4, VERTICAL),
                        ParentWord("CHIEF", 2, VERTICAL),
                        None,
                        ParentWord("CHIEF", 0, VERTICAL)]
    expected_horo_ps = [ParentWord("FOOD", 0, HORIZONTAL),
                        ParentWord("PIN", 1, HORIZONTAL),
                        ParentWord("PROD", 0, HORIZONTAL),
                        None]
    for i in range(len(tiles)):
        check_words(board, tiles[i], expected_vert_ps[i], expected_horo_ps[i])

print("\nTest 1")
lims_test_1(True)
print("\nTest 2")
lims_test_2(True)
