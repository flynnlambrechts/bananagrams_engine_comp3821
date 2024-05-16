from .score_word_strategy import ScoreWordStrategy
from constants import pair_end_count, pair_start_count


class ScoreWordTwoLetter(ScoreWordStrategy):
    def __init__(self) -> None:
        self.name = 'ScoreWordTwoLetter'

    def score_word(self, word_str: str, hand: str = '', anchor: str = '', min_length: int = 0):
        '''Could incorporate the hand_str into the scoring depending on the hand aswell'''
        result = 0
        for char in word_str:
            result += pow(10, 3) - \
                (pair_end_count[char] + pair_start_count[char])
            if char == 'V' or char == 'Q':
                result += pow(10, 4)
            if char == 'J' or char == 'X' or char == 'Z' or char == 'C':
                result += 5 * pow(10, 3)
        return result
