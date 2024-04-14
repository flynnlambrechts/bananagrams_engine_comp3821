from sys import argv 

if len(argv) == 1:
    print('Usage: pypy3 main.py <player> <player> ...')
    exit(1)

import trie_service # Initialize trie service
from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer

game = Game()
player_map = {
    's': StandardPlayer,
    'r': StrandingPlayer,
    'p': PseudoPlayer,
    't': TwoLetterJunkStrandingPlayer,
}
for p in argv[1:]:
    game.add_player(player_map[p](game))
game.start()
