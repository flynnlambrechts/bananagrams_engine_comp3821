from sys import argv

if len(argv) == 1:
    print('Usage: pypy3 main.py <players>')
    print('Example: pypy3 main.py rspp')
    exit(1)

import trie_service  # Initialize trie service
from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer
from players.NewStrandingPlayer import NewStrandingPlayer
from pouch import letter_distribution
from src.players.NewStrandingPlayer import NewStrandingPlayer


def parse_players(players: str):
    player_map = {
        's': StandardPlayer,
        'r': StrandingPlayer,
        'p': PseudoPlayer,
        't': TwoLetterJunkStrandingPlayer,
        'n': NewStrandingPlayer
    }
    return [player_map[p] for p in players]


game = Game(players=parse_players(argv[1]))

game.start()

# metrics = game.players[0].strand_metric
# print("STRANDING INFO")
# for metric in metrics:
#     print(f"eval: {metric[0]} -> {0 if metric[0]
#           < 0.2 else 1}, took \t {metric[1]}")

# print("RIGHT ANGLE INFO")
# for metric in game.players[0].right_angle_metric:
#     average_quality = sum(
#         1/letter_distribution[char] for char in metric[2])/len(metric[2])
#     print(f"result {metric[1]}, {
#           metric[0]}. \t HS {metric[5]}. P1: {metric[3]}, P2: {metric[4]}. Hand: {metric[2]}. Av. bad: {average_quality}")
