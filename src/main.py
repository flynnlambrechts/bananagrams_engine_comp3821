from game import Game
from players.StandardPlayer import StandardPlayer

game = Game()
game.add_player(StandardPlayer(game))
game.add_player(StandardPlayer(game))
# game.add_player(StandardPlayer())

game.start()
