from players.StrandingPlayer import StrandingPlayer
from two_letter_junk import best_anchor_candidates
from trie import Trie, letter_count
from algorithms import where_to_play_word
from word import Word
from board.tile import Tile
from constants import NO_SPACE_FOR_WORD, pair_start_count, pair_end_count
from trie_service import forward_trie


class TwoLetterJunkStrandingPlayer(StrandingPlayer):
    '''
    Everything is the same except for play_junk
    '''

    def play_junk(self, anchors: list[Tile]):
        '''
        Go through the anchors, play as much as possible each time
        Everything played here is labeled as junk and will be removed at the next rearrange
        '''
        _verbose = False
        if _verbose:
            print('[!] Before Junk Hand:', self.hand)

        # sort anchors by usefulness
        anchors.sort(
            key=lambda anchor: pair_start_count[anchor.char] +
            pair_end_count[anchor.char],
            reverse=True)

        # Remove anchors that are junk
        anchors = [a for a in anchors if not a.is_junk]

        for letter in self.hand:
            candidates = best_anchor_candidates(letter, anchors)

            for anchor in candidates:
                # Try letter + anchor combination first.
                # if it doesn't work out, try anchor + letter.
                word = letter + anchor.char
                placement = where_to_play_word(word, anchor)

                if placement == NO_SPACE_FOR_WORD or not forward_trie.is_word(word):
                    word = anchor.char + letter
                    placement = where_to_play_word(word, anchor)

                if placement == NO_SPACE_FOR_WORD or not forward_trie.is_word(word):
                    # Can't find an anchor
                    continue

                if _verbose:
                    print(
                        f'[!] Playing letter + anchor ({letter}+{anchor.char}) = {word}')
                new_tiles = self.play_word(
                    word, anchor, anchor_index=placement[0], is_junk=True)
                self.junk_tiles += new_tiles
                break

        if _verbose:
            print('[!] After Junk Hand:', self.hand)
