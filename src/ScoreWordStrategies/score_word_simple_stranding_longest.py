from ScoreWordStrategies.score_word_strategy import ScoreWordStrategy
from constants import pair_end_count, pair_start_count, is_prefix_of, is_suffix_of


class ScoreWordSimpleStrandingLongest(ScoreWordStrategy):
    def __init__(self) -> None:
        self.name = 'ScoreWordSimpleStrandingLongest'

    def score_word(self, word_str: str, hand: str = '', anchor: str = '', min_length: int = 0):
        if word_str is None:
            return -1000000
        if len(word_str) < min_length:
            return -1000000
        # all_other_letters = self._all_other_letters(word_str)
        if len(word_str) > 2:
            word_middle = word_str[1:-1]
            middle_score = sum(pair_end_count[char] + pair_start_count[char]
                               for char in word_middle) / (len(word_str) - 2)
        else:
            middle_score = 0

        edge_score = ((pair_end_count[word_str[0]] + pair_start_count[word_str[0]] +
                       pair_end_count[word_str[-1]] + pair_start_count[word_str[-1]]) * 1000)

        return edge_score - 1000 * middle_score + len(word_str) * pow(10, 6)