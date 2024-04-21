from board.board import Board
from pathlib import Path
from players import StrandingPlayer
from two_letter_junk import best_anchor_candidates
from trie import Trie, letter_count
from algorithms import where_to_play_word
from word import Word
from board.tile import Tile
from constants import VERTICAL, HORIZONTAL, NO_SPACE_FOR_WORD, MAX_LIMIT, ANCHOR_IS_PREFIX, ANCHOR_IS_SUFFIX, DICT_SIZE, THRESHOLD_DIFFERENT_STRANDING_METHODS, HOW_UNGREEDY_IS_STRAND, is_prefix_of, is_suffix_of, pair_start_count, pair_end_count
from lims_algos import send_probes
from board.lims import Lims
from players.player import Player
from trie_service import all_words_trie, forward_trie, reverse_trie
import time
from players.TwoLetterJunkStrandingPlayer import TwoLetterJunkStrandingPlayer
from pprint import pprint


class NewStrandingPlayer(TwoLetterJunkStrandingPlayer):
    '''
    Everything is the same except for play_junk
    '''

    def __init__(self, game, id: int, word_scorer) -> None:
        super().__init__(game, id, word_scorer=word_scorer)
        self.dump_on_failure: bool = True
        # the property defines whether you should dump if you can't play everything vs restructure.
        # if you've received new tiles while junk was on the board, don't dump.
        self.dump_count = 0
        self.junk_tiles = []  # Which tiles on the board are junk
        self.strand_metric = []
        self.right_angle_metric = []

    # def give_tiles(self, tiles: list[str]):
    #     self.dump_on_failure = False
    #     super().give_tiles(tiles)

    # def play_first_turn(self):
    #     # Find the first word, play it, and add its first and last characters/tiles
    #     # to `anchors`
    #     start_word: Word = self.long_with_best_rank(all_words_trie.all_subwords(self.hand),
    #                                                 rank_strategy="strand",
    #                                                 closeness_to_longest=2)

    #     self.play_word(str(start_word))
    #     self.show_board()

    def play_turn(self):
        self.speak(
            "turn",
            f"game no {self.game.pouch.seed}. player played {len(self.board.tiles.keys())} tiles so far, {self.game.pouch.n_remaining()}")
        if len(self.hand) == 0:
            # Peel if hand is empty
            self.peel()
        if not self.game.game_is_active:
            return
        if not self.playing:
            # If this is the first turn the player acts differently
            self.playing = True
            self.play_first_turn()
            return

        # Otherwise generic implementation of play turn
        # self.speak('Finding Word', f"available letters {self.hand}")
        strand_anchors = self.find_strand_extending_anchors()
        other_anchors = list(
            set(self.board.tiles.values()) - set(strand_anchors))

        if len(self.hand) < 5:
            # self.speak("STRANDING", "hand is small. playing junk")
            self.play_junk(list(self.board.tiles.values()))
            if len(self.hand) > 0:
                return self.restructure_board()
        elif self.play_best_strand_extension(strand_anchors):
            # new word: tuple(word, anchor, anchor is suffix)
            self.speak("STRANDING", "playing strand extension")
        elif self.play_right_angle_word():
            self.speak("STRANDING", "playing right angle")
        else:
            # print("attempting to play junk because can't do anything else")
            self.play_junk(other_anchors)
            if len(self.hand) > 0:
                return self.restructure_board()

    # def restructure_board(self):
    #     '''
    #     If we cannot continue without our current board formation
    #     this function is called. It should made adjustments and try
    #     play a word again

    #     Current implementation removes all 'junk tiles' (stuff that isn't contributing to stranding)
    #     and dumps if it's stuck. Then play resumes.
    #     '''
    #     self.remove_junk()
    #     old_hand = self.hand
    #     if self.dump_on_failure:
    #         worst_letter_in_hand = min(
    #             self.hand, key=lambda char: letter_count[char])

    #         self.game.dump(self, worst_letter_in_hand)
    #         self.dump_count += 1

    #         if len(old_hand) == len(self.hand):
    #             self.speak("ERROR", "tried to dump at the end and choked")
    #             exit(1)
    #     else:
    #         print("restructured without dumping")

    #     self.dump_on_failure = True
    #     # TODO
    #     # return "Error"
    #     # raise NotImplementedError("Board restructuring not implemented yet")

    # def find_strand_extending_anchors(self):
    #     '''
    #     used for the below find_strand_extension function.
    #     returns tiles that have infinite space in 1 direction and some space at 90 degrees
    #     '''
    #     strand_extending_anchors = []
    #     for tile in self.board.tiles.values():
    #         if tile.vert_parent == None:
    #             if (tile.lims.left == MAX_LIMIT or tile.lims.right == MAX_LIMIT) and (tile.lims.up > 0 or tile.lims.down > 0):
    #                 strand_extending_anchors.append(tile)
    #         elif tile.horo_parent == None:
    #             if (tile.lims.up == MAX_LIMIT or tile.lims.down == MAX_LIMIT) and (tile.lims.left > 0 or tile.lims.right > 0):
    #                 strand_extending_anchors.append(tile)

    #     return strand_extending_anchors

    '''
    TODO: think about preferred side to strand e.g.
    FOLLOW
         EMBARGO
    It would be nicer to made GO or NO the stranding word rather than ON or OR
    '''

    def play_best_strand_extension(self, anchors: list[Tile]) -> Word | None:
        '''Finds the best and longest word that can be attached via a two letter word.'''
        # print("looking for strand extension")
        prefix_anchors = dict()  # prefix of the new word
        suffix_anchors = dict()  # suffix of the new word
        start_time = time.process_time()
        for anchor in anchors:
            pair_list = all_words_trie.find_two_letters(anchor.char, self.hand)

            parent = anchor.get_only_parent()

            if parent.pos(anchor) == 0:
                # the anchor is the first letter of a word
                # so the letter will be an anchor for a suffix word
                dict_to_add_to = suffix_anchors
            else:
                dict_to_add_to = prefix_anchors
            # if (parent.direction == VERTICAL and anchor.lims.right > 0) or (parent.direction == HORIZONTAL and anchor.lims.down > 0):
            if self.first_anchor_can_be_nth_char(anchor, parent, 0):
                # when the first_anchor char is first, you're good
                # when the first_anchor char is both, you're good
                # print(f"{anchor} can be the first letter in the 2 letter word")
                # TODO!!!! use hypothetical lims here
                for pair in pair_list:
                    if pair.string[0] == anchor.char:
                        dict_to_add_to[pair.string[1]] = (
                            anchor, pair.string, 0)
            # if (parent.direction == VERTICAL and anchor.lims.left > 0) or (parent.direction == HORIZONTAL and anchor.lims.up > 0):
            if self.first_anchor_can_be_nth_char(anchor, parent, 1):
                # when the first_anchor char is second, you're good
                # when the first_anchor char is both, you're good
                # print(f"{anchor} can be the first letter in the 2 letter word")
                # TODO!!!! use hypothetical lims here
                for pair in pair_list:
                    if pair.string[1] == anchor.char:
                        dict_to_add_to[pair.string[0]] = (
                            anchor, pair.string, 1)

        ease_of_stranding_score = 0
        for prefix in prefix_anchors.keys():
            ease_of_stranding_score += is_prefix_of[prefix]
        for suffix in suffix_anchors.keys():
            ease_of_stranding_score += is_suffix_of[suffix]

        if ease_of_stranding_score > THRESHOLD_DIFFERENT_STRANDING_METHODS * DICT_SIZE:
            self.speak("stranding", "all_words approach")
            all_words = all_words_trie.all_subwords(self.hand)
            all_words.sort(key=lambda word: word.len(), reverse=True)

            best_words = all_words[:min(
                HOW_UNGREEDY_IS_STRAND, len(all_words))]
            if len(best_words) == 0:
                self.strand_metric.append(
                    (ease_of_stranding_score/DICT_SIZE, time.process_time()-start_time))
                return False
            # do all_word search
            # longest_length = best_words[0].len()
            best_words.sort(key=lambda word: self.word_scorer.score_word(
                word.string, hand = self.hand))
            word_found = False
            i = 0
            while word_found is False:
                word_str = best_words[i].string
                if word_str[0] in prefix_anchors.keys():
                    key_info = prefix_anchors[word_str[0]]
                    second_anchor_index = 0
                    word_found = True
                if word_str[-1] in suffix_anchors.keys():
                    key_info = suffix_anchors[word_str[-1]]
                    second_anchor_index = len(word_str) - 1
                    word_found = True
                i += 1
                if i >= len(best_words):
                    # self.strand_metric.append(
                    #     (ease_of_stranding_score/DICT_SIZE, time.process_time()-start_time))

                    return False

            first_anchor = key_info[0]
            two_letter_word = key_info[1]
            first_anchor_index = key_info[2]
            second_anchor = self.play_word(
                two_letter_word, first_anchor, first_anchor_index)[0]
            self.play_word(word_str, second_anchor,
                           second_anchor_index)
            
            return True
        else:
            self.speak("stranding", "old approach")

            all_words = dict()

            for prefix in prefix_anchors.keys():
                words = forward_trie.all_subwords(
                    self.hand.replace(prefix, '', 1), prefix)
                if len(words) > 0:
                    local_best = max(words, key = lambda word: self.word_scorer.score_word(word.string, hand = self.hand))
                    # self.long_with_best_rank(words)
                    all_words[local_best] = "prefix"

            for suffix in suffix_anchors.keys():
                words = reverse_trie.all_subwords(
                    self.hand.replace(suffix, '', 1), suffix)
                if len(words) > 0:
                    local_best = max(words, key = lambda word: self.word_scorer.score_word(word.string, hand = self.hand)) #= self.long_with_best_rank(words)
                    all_words[local_best] = "suffix"
            if len(all_words.keys()) > 0:
                best_word = max(list(all_words.keys()), key = lambda word: self.word_scorer.score_word(word.string, hand = self.hand)) #self.long_with_best_rank(list(all_words.keys()))
            else:
                return False

            if best_word is None or len(best_word.string) < 3:
                return False

            if all_words[best_word] == "prefix":
                key_info = prefix_anchors[best_word.string[0]]
                # pprint(key_info)
                second_anchor_index = 0
            else:
                key_info = suffix_anchors[best_word.string[-1]]
                # pprint(key_info)
                second_anchor_index = len(best_word.string) - 1

            first_anchor = key_info[0]
            two_letter_word = key_info[1]
            first_anchor_index = key_info[2]

            second_anchor = self.play_word(
                two_letter_word, first_anchor, first_anchor_index)[0]
            # print("two_tiles:")
            # pprint(two_tiles)
            # second_anchor = two_tiles[0]
            # if second_anchor == first_anchor:
            #     second_anchor = two_tiles[1]

            self.play_word(best_word.string, second_anchor,
                           second_anchor_index)
            return True
