from multiprocessing import Manager
import time
import statistics
import signal
from sys import argv

# Custom imports
from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer
from players.NewStrandingPlayer import NewStrandingPlayer
from ScoreWordStrategies.score_word_hand_balance import ScoreWordHandBalance
from ScoreWordStrategies.score_word_simple_stranding import ScoreWordSimpleStranding
from ScoreWordStrategies.score_word_two_letter import ScoreWordTwoLetter
from ScoreWordStrategies.score_word_hand_balance_longest import ScoreWordHandBalanceLongest
from players.StandardPlayerDangling import StandardPlayerDangling
from ScoreWordStrategies.score_word_simple_stranding_longest import ScoreWordSimpleStrandingLongest
from ScoreWordStrategies.score_word_letter_count_long import ScoreLetterCountLong
from constants import THRESHOLD_DIFFERENT_STRANDING_METHODS, HOW_UNGREEDY_IS_STRAND
TIMEOUT_DURATION = 1


def parse_players(players: str):
    player_map = {
        's': StandardPlayer,
        'r': StrandingPlayer,
        'p': PseudoPlayer,
        'd': StandardPlayerDangling,
        't': TwoLetterJunkStrandingPlayer,
        'n': NewStrandingPlayer
    }
    return [player_map[p] for p in players]


def parse_word_scorer(word_scorers: str):
    word_scorer_map = {
        # 'r': ScoreWordSimpleStranding,
        # 'h': ScoreWordHandBalance,
        # The above weren't used as they didn't rank words based on length so the word lengths
        # would need to be pre-filtered (which our algorithms don't currently do)
        'l': ScoreWordTwoLetter,
        'R': ScoreWordSimpleStrandingLongest,
        'H': ScoreWordHandBalanceLongest,
        'C': ScoreLetterCountLong
    }
    return [word_scorer_map[s] for s in word_scorers]


def format_time(seconds: float):
    in_ms = seconds * 1000
    return f'{in_ms:.5f} ms'


def winner_frequencies(winners):
    word_counts = {}
    total_count = 0

    for item in winners:
        # item is a list of winners, but there should only
        # be one winner so we take the first winner
        parts = item[0].split('\n')
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


def benchmark_game(i, j, players, times, winners, fail_counts, word_scorers):
    '''
    CPU time only counts when the CPU is executing this process
    NOTE: CPU time does NOT count count the time spent writing to `stdout` or any other I/O operation
    '''
    game = Game(players, word_scorers, seed=j)
    # game = Game(players, word_scorers)
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
    iterations = 100
    targets = [
        # 'ppn',
        # 'ppn',
        # 'ppn',
        # 'ppr',
        # 'ppr',
        # 'ppr',
        # 'ppt',
        # 'ppt',
        argv[1]
    ]

    scorers = [
        # 'rrl',
        # 'rrH',
        # 'rrR',
        # 'rrl',
        # 'rrH',
        # 'rrR',
        # 'rrl',
        # 'rrH',
        argv[2]
    ]

    manager = Manager()
    times = manager.list([manager.list() for _ in targets])
    winners = manager.list([manager.list() for _ in targets])
    fail_counts = manager.list([0 for _ in targets])

    # with Pool(processes=1) as pool:
    tasks = []
    if len(targets) == len(scorers):

        for i, target in enumerate(targets):
            for j in range(iterations):
                players = parse_players(target)
                word_scorers = parse_word_scorer(scorers[i])
                benchmark_game(i, j, players, times, winners,
                               fail_counts, word_scorers)
                # tasks += [(i, j, players, times, winners, fail_counts, word_scorers)
                #   for _ in range(iterations)]

                # pool.map(benchmark_game, tasks)
    else:
        print("Error, mismatched length of scorers and players")

    print('--- Stats ---')
    print(
        f"how ungreedy: {HOW_UNGREEDY_IS_STRAND}, threshold: {THRESHOLD_DIFFERENT_STRANDING_METHODS}")
    print(f"Iterations: {iterations}")
    for target, scorer, times, winners, fail_count in zip(
            targets, scorers, times, winners, fail_counts):
        print(f'Target {target}, Scorer {scorer}')

        print(f'- Mean: {format_time(statistics.mean(times))}')
        print(f'- Median: {format_time(statistics.median(times))}')
        print(f'- Standard Deviation: {format_time(statistics.stdev(times))}')

        print(f'- Fail count: {fail_count}')
        print('- Top winners:')
        freqs = winner_frequencies(winners)
        for i, (k, v) in enumerate(sorted(freqs.items(), key=lambda t: -t[1])):
            print(f'  {i+1}. {k}: {format(v, ".0%")}')
