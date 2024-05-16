from src.board.board import Board
import json 

def board_to_object(board: Board):
    result = []
    print(str(board))
    print(str(board.tiles))
    min_row = board.min_row()
    min_col = board.min_col()
    for (coords, tile) in board.tiles.items():
        coords = (coords[0] - min_row + 1, coords[1] - min_col + 1)
        result.append({"coords": coords, "letter": tile.char})
    return result

def get_game_state(game):
    cpu = game.players[0]
    player = game.players[1]
    state = {
        "running": game.game_is_active,
        "cpu": {
            "board": board_to_object(cpu.board),
            "width": cpu.board.max_col() - cpu.board.min_col() + 1,
            "height": cpu.board.max_row() - cpu.board.min_row() + 1,
            "hand": [*cpu.hand],
        },
        "player": {"hand": [*player.hand]},
    }
    return state