from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer
from players.NewStrandingPlayer import NewStrandingPlayer

game = Game()
game.add_player(NewStrandingPlayer(game))
# game.add_player(PseudoPlayer(game))
# game.add_player(PseudoPlayer(game))

game.start()
metrics = game.players[0].strand_metric
print("STRANDING INFO")
for metric in metrics:
    print(f"eval: {metric[0]} -> {0 if metric[0]
          < 0.1 else 1}, took \t {metric[1]}")

print("RIGHT ANGLE INFO")
for metric in game.players[0].right_angle_metric:
    print(f"result was {metric[1]} and took {metric[0]}")
