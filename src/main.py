from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer

game = Game()

game.add_player(StandardPlayer(game))
game.add_player(PseudoPlayer(game))
game.add_player(PseudoPlayer(game))

game.start()
