import timeit
from game import Game
from players.StandardPlayer import StandardPlayer

seeds = list(range(0, 10))
game = Game()
game.add_player(StandardPlayer(game))

time_taken = timeit.timeit("game.start()", globals=globals(), number=1)
print(time_taken)
        