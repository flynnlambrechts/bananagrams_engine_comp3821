from ScoreWordStrategies.score_word_strategy import ScoreWordStrategy
from constants import pair_end_count, pair_start_count


class ScoreWordTwoLetter(ScoreWordStrategy):
    def __init__(self) -> None:
        self.name = 'ScoreWordTwoLetter'

    def score_word(self, word_str: str, hand: str = '', anchor: str = '', min_length: int = 0):
        '''Could incorporate the hand_str into the scoring depending on the hand aswell'''
        result = 0
        for char in word_str:
            result += 10000000 - (pair_end_count[char] + pair_start_count[char])
        if ('V' in word_str):
            return 100000000
        if ('Q' in word_str):
            return 100000000
        return result
