from multiprocessing import Manager, Pool
import time
import statistics

import trie_service  # Initialize trie service
from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer


def parse_players(players: str):
    player_map = {
        's': StandardPlayer,
        'r': StrandingPlayer,
        'p': PseudoPlayer,
        't': TwoLetterJunkStrandingPlayer,
    }
    return [player_map[p] for p in players]


def format_time(seconds: float):
    in_ms = seconds * 1000
    return f'{in_ms:.5f} ms'


def benchmark_game(args):
    i, players, results = args
    '''
    CPU time only counts when the CPU is executing this process
    NOTE: CPU time does NOT count count the time spent writing to `stdout` or any other I/O operation
    '''
    game = Game(players)
    start_cpu_time = time.process_time()
    game.start()
    end_cpu_time = time.process_time()
    results[i].append(end_cpu_time - start_cpu_time)


if __name__ == '__main__':
    iterations = 20
    targets = [
        'pps',
        'ppr',
        'ppt',
    ]

    manager = Manager()
    results = manager.list([manager.list() for _ in targets])

    with Pool(processes=1) as pool:
        tasks = []
        for i, target in enumerate(targets):
            players = parse_players(target)
            tasks += [(i, players, results) for _ in range(iterations)]

        pool.map(benchmark_game, tasks)

    print('--- Stats ---')
    for i, result in enumerate(results):
        print(f'Target {targets[i]}:')
        print(f'- Mean: {format_time(statistics.mean(result))}')
        print(f'- Median: {format_time(statistics.median(result))}')
        print(f'- Standard Deviation: {format_time(statistics.stdev(result))}')
