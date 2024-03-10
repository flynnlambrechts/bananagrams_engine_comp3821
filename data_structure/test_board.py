from board import Board

def test_tile_exists():
    board = Board()
    
    board.add_tile('a', -1, 2)
    board.add_tile('b', 0, 6)
    board.add_tile('c', 1000, 200000)
    
    assert board.tiles[(-1, 2)] == 'a'
    assert board.tiles[(0, 6)] == 'b'
    assert board.tiles[(1000, 200000)] == 'c'
    assert (5, 1) not in board.tiles
