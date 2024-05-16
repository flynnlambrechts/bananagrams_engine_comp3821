from flask import Flask
from flask_cors import CORS
from src.game import Game

from src.players.StandardPlayerDangling import StandardPlayerDangling
from src.players.OnlinePlayer import OnlinePlayer

# from src.ScoreWordStrategies.score_word_simple_stranding import ScoreWordSimpleStranding
from src.ScoreWordStrategies.score_word_letter_count_long import ScoreLetterCountLong
import threading

import os
import sys

# Assuming your Flask app is in the 'flask_app' directory
# export PYTHONPATH='/Users/flynnlambrechts/Desktop/COMP3821/bananagrams_engine_comp3821/src':$PYTHONPATH
# flask run
flask_app_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, flask_app_dir)

from app_utils import board_to_object

app = Flask(__name__)
CORS(app)


def make_new_game():
    global game
    game = Game(
        [StandardPlayerDangling, OnlinePlayer],
        [ScoreLetterCountLong, ScoreLetterCountLong],
    )
    
    global game_thread
    game_thread = threading.Thread(target=game.start)


make_new_game()

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/start")
def start():
    game_thread.start()
    return "Game Started"


@app.route("/game_state")
def game_state():
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


@app.route("/reset")
def reset():
    game.end_game()
    game_thread.join()
    make_new_game()
    return "Reset"
