from ScoreWordStrategies.score_word_strategy import ScoreWordStrategy
from constants import letter_count


class ScoreLetterCountLong(ScoreWordStrategy):
    def __init__(self) -> None:
        self.name = 'ScoreLetterCountLong'

    def score_word(self, word_str: str, hand: str = '', anchor: str = '', min_length: int = 0):
        result = 0
        for char in word_str:
            result += pow(10, 7) - letter_count[char]
        return result
