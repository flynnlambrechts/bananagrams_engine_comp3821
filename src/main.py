from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer
from players.NewStrandingPlayer import NewStrandingPlayer
from pouch import letter_distribution
game = Game()
game.add_player(NewStrandingPlayer(game))
# game.add_player(PseudoPlayer(game))
# game.add_player(PseudoPlayer(game))

game.start()
metrics = game.players[0].strand_metric
print("STRANDING INFO")
for metric in metrics:
    print(f"eval: {metric[0]} -> {0 if metric[0]
          < 0.2 else 1}, took \t {metric[1]}")

print("RIGHT ANGLE INFO")
for metric in game.players[0].right_angle_metric:
    average_quality = sum(
        1/letter_distribution[char] for char in metric[2])/len(metric[2])
    print(f"result {metric[1]}, {
          metric[0]}. \t HS {metric[5]}. P1: {metric[3]}, P2: {metric[4]}. Hand: {metric[2]}. Av. bad: {average_quality}")
