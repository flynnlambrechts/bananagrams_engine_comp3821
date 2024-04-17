from multiprocessing import Manager, Pool
import time
import statistics

import trie_service  # Initialize trie service
from game import Game
from players.StandardPlayer import StandardPlayer
from players.StrandingPlayer import StrandingPlayer
from players.PseudoPlayer import PseudoPlayer
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer
from players.NewStrandingPlayer import NewStrandingPlayer
from ScoreWordStrategies.score_word_hand_balance import ScoreWordHandBalance
from ScoreWordStrategies.score_word_simple_stranding import ScoreWordSimpleStranding
from ScoreWordStrategies.score_word_two_letter import ScoreWordTwoLetter


def parse_players(players: str):
    player_map = {
        's': StandardPlayer,
        'r': StrandingPlayer,
        'p': PseudoPlayer,
        't': TwoLetterJunkStrandingPlayer,
        'n': NewStrandingPlayer
    }
    return [player_map[p] for p in players]


def parse_word_scorer(word_scorers: str):
    word_scorer_map = {
        'r': ScoreWordSimpleStranding,
        'l': ScoreWordTwoLetter,
        'h': ScoreWordHandBalance
    }
    return [word_scorer_map[s] for s in word_scorers]


def format_time(seconds: float):
    in_ms = seconds * 1000
    return f'{in_ms:.5f} ms'


def benchmark_game(i, players, word_scorers, results):
    '''
    CPU time only counts when the CPU is executing this process
    NOTE: CPU time does NOT count count the time spent writing to `stdout` or any other I/O operation
    '''
    game = Game(players, word_scorers=word_scorers)
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

    scorers = [
        'rrr',
        'rrr',
        'rrr'
    ]

    manager = Manager()
    results = manager.list([manager.list() for _ in targets])

    # with Pool(processes=20) as pool:
    tasks = []
    for i, target in enumerate(targets):
        for _ in range(iterations):
            players = parse_players(target)
            word_scorers = parse_word_scorer(scorers[i])
            # tasks += [() for _ in range(iterations)]
            benchmark_game(i, players, word_scorers, results)

        # pool.map(benchmark_game, tasks)

    print('--- Stats ---')
    for i, result in enumerate(results):
        print(f'Target {targets[i]} Scorers {scorers[i]}:')
        print(f'- Mean: {format_time(statistics.mean(result))}')
        print(f'- Median: {format_time(statistics.median(result))}')
        print(f'- Standard Deviation: {format_time(statistics.stdev(result))}')
