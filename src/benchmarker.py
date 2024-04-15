from threading import Thread
from multiprocessing import Process, Manager, Value, Lock
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


iterations = 20
targets = [
    'pps',
    'ppr',
    'ppt',
]

processes = []
manager = Manager()
results = manager.list([manager.list() for _ in targets])
num_plays = Value('i', 0)
lock = Lock()
# results = [[] for _ in targets]
for i, target in enumerate(targets):
    players = parse_players(target)
    for j in range(iterations):

        def benchmark_game(i, j, results, lock, num_plays):
            game = Game(players, process_lock=lock)
            '''
                CPU time only counts when the CPU is executing this process
                NOTE: CPU time does NOT count count the time spent writing to `stdout` or any other I/O operation
            '''
            start_cpu_time = time.process_time()
            game.start()
            end_cpu_time = time.process_time()
            results[i].append(end_cpu_time - start_cpu_time)
            with lock:
                num_plays.value += 1

        process = Process(target=benchmark_game, args=(i, j, results, lock, num_plays))
        processes.append(process)
        process.start()

for process in processes:
    process.join()

print('--- Stats ---')
print(num_plays.value)
for i, result in enumerate(results):
    print(f'Target {targets[i]}:')
    print(f'- Mean: {format_time(statistics.mean(result))}')
    print(f'- Median: {format_time(statistics.median(result))}')
    print(f'- Standard Deviation: {format_time(statistics.stdev(result))}')
