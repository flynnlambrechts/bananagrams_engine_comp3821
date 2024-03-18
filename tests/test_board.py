from src.Game.Board.Board import Board
from pytest import raises


def test_add_tile():
    board = Board()

    board.add_tile('a', -1, 2)
    board.add_tile('b', 0, 6)
    board.add_tile('c', 1000, 200000)

    assert board.tiles[(-1, 2)] == 'a'
    assert board.tiles[(0, 6)] == 'b'
    assert board.tiles[(1000, 200000)] == 'c'

    with raises(ValueError):
        board.add_tile('x', -1, 2)


def test_remove_tile():
    board = Board()

    board.add_tile('a', -1, 2)
    assert board.remove_tile(-1, 2) == 'a'
    with raises(ValueError):
        board.remove_tile(-1, 2)
