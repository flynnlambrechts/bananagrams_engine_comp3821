from .score_word_strategy import ScoreWordStrategy
from constants import letter_distribution


class ScoreWordHandBalance(ScoreWordStrategy):
    def __init__(self) -> None:
        self.name = 'ScoreWordHandBalance'

    def score_word(self, word_str: str, hand: str = '', anchor: str = '', min_length: int = 0):
        '''Basic concept: function that (almost) always gives positive points for playing tiles, but gives more points if you play letters that are more overrepresented. 

        Define error as |proportion of letter in hand - proportion of letter in game|.

        Score is the change in the sum of error for every letter'''

        '''Notes to consider: if hand is close to perfectly balanced, nothing will look very good, and rare letters will be the last to be played. So maybe this algorithm should only run if the hand is at a particular level of unbalance. Or, use this algo to pick between the top words selected through some other means'''
        if len(word_str) < min_length:
            return 0
        hand_after_playing = hand
        played_tiles = word_str.replace(anchor, '', 1)
        for char in played_tiles:
            hand_after_playing.replace(char, '', 1)

        hand_len = len(hand)
        hand_after_playing_len = len(hand_after_playing)
        initial_unbalance = 0
        for char in set(hand):
            initial_unbalance += abs(hand.count(char) /
                                     hand_len - letter_distribution[char]/144)
        post_unbalance = 0
        for char in set(hand):
            post_unbalance += abs(hand_after_playing.count(char) /
                                  hand_after_playing_len - letter_distribution[char]/144)

        return initial_unbalance - post_unbalance
