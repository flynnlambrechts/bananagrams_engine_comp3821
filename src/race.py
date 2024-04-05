from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from multiprocessing import Process

import timeit

class TimeoutError(Exception):
    pass


def game1(seed) -> Game:
    game = Game(seed)
    
    game.add_player(StrandingPlayer(game))
    game.add_player(PseudoPlayer(game))
    game.add_player(PseudoPlayer(game))
    return game

def game2(seed) -> Game:
    game = Game(seed)
        
    game.add_player(StandardPlayer(game))
    game.add_player(PseudoPlayer(game))
    game.add_player(PseudoPlayer(game))
    return game
    
def do_test(func, args: tuple, kwargs: dict):
    p = Process(target=func, args=args, kwargs=kwargs, name='Time Execution')
    p.start()
    p.join(timeout=5)
    p.terminate()
    return int(bool(p.exitcode))
    
    
def race(n_tests) -> tuple[int, int]:
    # n_experiments = 1
    t1_cum = 0
    t2_cum = 0
    t1_runs = 0
    t2_runs = 0
    
    for seed in range(n_tests):
        print(f"GAME STARTING {seed}")
        seed *= 5
        game1_ins = game1(seed)
        game2_ins = game2(seed)
        
        try: 
            t1_cum += timeit.timeit(game1_ins.start, number=1)
            t1_runs += 1
        except:
            pass
        
        try:
            t2_cum += timeit.timeit(game2_ins.start, number=1)
            t2_runs += 1
        except:
            pass
    
    t1_avg = t1_cum / t1_runs
    t2_avg = t2_cum / t2_runs
    
    expected_runs = n_tests # * n_experiments
    
    print(f"Game 1 (Stranding Player) Average Speed: {t1_avg}, out of {t1_runs} with {expected_runs - t1_runs} failures")
    print(f"Game 2 (Standard Player) Average Speed: {t2_avg}, out of {t2_runs} with {expected_runs - t2_runs} failures")
    return (t1_cum / n_tests, t2_cum / n_tests)

if __name__ == "__main__":
    race(10)
        
