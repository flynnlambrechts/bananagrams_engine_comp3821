from multiprocessing import Manager, Pool
import time
import statistics
import signal

# Custom imports
from players.player import Player
import trie_service  # Initialize trie service
from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer


TIMEOUT_DURATION = 5


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


def winner_frequencies(winners):
    word_counts = {}
    total_count = 0

    for item in winners:
        # item is a list of winners, but there should only
        # be one winner so we take the first winner
        parts = item[0].split()
        word = parts[0]

        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word] += 1
        total_count += 1

    for key in word_counts:
        word_counts[key] /= total_count

    return word_counts


def timeout_handler(signum, frame):
    raise TimeoutError('Function execution exceeded ' +
                       f'{TIMEOUT_DURATION} seconds')


def benchmark_game(args):
    i, players, times, winners, fail_counts = args
    '''
    CPU time only counts when the CPU is executing this process
    NOTE: CPU time does NOT count count the time spent writing to `stdout` or any other I/O operation
    '''
    game = Game(players, seed=1)
    # Setup and start timer
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIMEOUT_DURATION)

    try:
        start_cpu_time = time.process_time()
        game.start()
        end_cpu_time = time.process_time()
    except TimeoutError:
        fail_counts[i] += 1
        return
    finally:
        signal.alarm(0)  # Cancel the alarm

    times[i].append(end_cpu_time - start_cpu_time)
    winners[i].append(game.winners)


if __name__ == '__main__':
    iterations = 5
    targets = [
        'pps',
        'ppr',
        'ppt',
    ]

    manager = Manager()
    times = manager.list([manager.list() for _ in targets])
    winners = manager.list([manager.list() for _ in targets])
    fail_counts = manager.list([0 for _ in targets])

    with Pool(processes=1) as pool:
        tasks = []
        for i, target in enumerate(targets):
            players = parse_players(target)
            tasks += [(i, players, times, winners, fail_counts)
                      for _ in range(iterations)]

        pool.map(benchmark_game, tasks)

    print('--- Stats ---')
    for target, times, winners, fail_count in zip(targets, times, winners, fail_counts):
        print(f'Target {target}')

        print(f'- Mean: {format_time(statistics.mean(times))}')
        print(f'- Median: {format_time(statistics.median(times))}')
        print(f'- Standard Deviation: {format_time(statistics.stdev(times))}')

        print(f'- Fail count: {fail_count}')
        print('- Top winners:')
        freqs = winner_frequencies(winners)
        for i, (k, v) in enumerate(sorted(freqs.items(), key=lambda t: -t[1])):
            print(f'  {i+1}. {k}: {format(v, ".0%")}')
