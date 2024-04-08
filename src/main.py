from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer

game = Game()
game.add_player(TwoLetterJunkStrandingPlayer(game))
# game.add_player(PseudoPlayer(game))
# game.add_player(PseudoPlayer(game))

game.start()
