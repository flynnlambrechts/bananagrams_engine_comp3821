from board.board import Board
from pathlib import Path
from players import StrandingPlayer
from two_letter_junk import best_anchor_candidates
from trie import Trie, letter_count
from algorithms import long_with_best_rank, where_to_play_word, score_word_simple_stranding
from word import Word
from board.tile import Tile
from constants import VERTICAL, HORIZONTAL, NO_SPACE_FOR_WORD, MAX_LIMIT, ANCHOR_IS_PREFIX, ANCHOR_IS_SUFFIX
from lims_algos import send_probes
from board.lims import Lims
from players.player import Player
is_prefix_of = {'A': 16194, 'B': 15218, 'C': 25015, 'D': 16619, 'E': 11330, 'F': 10633, 'G': 9351, 'H': 10524, 'I': 9604, 'J': 2311, 'K': 3361, 'L': 8058, 'M': 15811, 'N': 6564, 'O': 8895, 'P': 24327, 'Q': 1411, 'R': 15014, 'S': 31986, 'T': 14563, 'U': 9522, 'V': 4590, 'W': 5921, 'X': 309, 'Y': 1036, 'Z': 1159}
is_suffix_of = {'A': 5560, 'B': 371, 'C': 6121, 'D': 25039, 'E': 28261, 'F': 534, 'G': 20216, 'H': 3293, 'I': 1601, 'J': 12, 'K': 2327, 'L': 8586, 'M': 4620, 'N': 12003, 'O': 1887, 'P': 1547, 'Q': 10, 'R': 14784, 'S': 107294, 'T': 13933, 'U': 379, 'V': 45, 'W': 610, 'X': 583, 'Y': 19551, 'Z': 159}
pair_start_count = {'A': 16, 'B': 5, 'C': 1, 'D': 4, 'E': 13, 'F': 3, 'G': 3, 'H': 5, 'I': 6, 'J': 2, 'K': 4, 'L': 3, 'M': 7, 'N': 5, 'O': 17, 'P': 4, 'Q': 1, 'R': 1, 'S': 4, 'T': 4, 'U': 8, 'V': 0, 'W': 2, 'X': 2, 'Y': 4, 'Z': 3}
pair_end_count = {'A': 15, 'B': 2, 'C': 0, 'D': 4, 'E': 15, 'F': 3, 'G': 2, 'H': 6, 'I': 14, 'J': 0, 'K': 1, 'L': 2, 'M': 6, 'N': 5, 'O': 17, 'P': 2, 'Q': 0, 'R': 4, 'S': 5, 'T': 5, 'U': 6, 'V': 0, 'W': 3, 'X': 3, 'Y': 7, 'Z': 0}

class TwoLetterJunkStrandingPlayer(Player):
    '''
    Everything is the same except for play_junk
    '''
    
    def __init__(self, game) -> None:
        super().__init__(game)
        self.dump_on_failure: bool = True
        # the property defines whether you should dump if you can't play everything vs restructure. 
        # if you've received new tiles while junk was on the board, don't dump. 
        self.dump_count = 0

    def give_tiles(self, tiles: list[str]):
        self.dump_on_failure = False
        super().give_tiles(tiles)

    def play_first_turn(self):
        # Find the first word, play it, and add its first and last characters/tiles
        # to `anchors`
        start_word: Word = long_with_best_rank(self.all_words.all_subwords(self.hand), 
                                               rank_strategy = "strand",
                                               closeness_to_longest = 2)
        
        # self.speak("Playing", start_word)
        self.play_word(str(start_word))
        self.show_board()
        # self.anchors += [self.board.tiles[(0, 0)], self.board.tiles[(0, len(str(start_word)) - 1)]]

    def play_turn(self):
        # print("")
        # Peel if hand is empty
        if len(self.hand) == 0:
            self.peel()
        if not self.game.game_is_active:
                return

        # If this is the first turn the player acts differently
        if not self.playing:
            self.playing = True
            self.play_first_turn()
            return

        # Otherwise generic implementation of play turn
        # self.speak('Finding Word', f"available letters {self.hand}")

        strand_anchors = self.find_strand_extending_anchors()
        other_anchors = list(set(self.board.tiles.values()) - set(strand_anchors))
        
        if len(self.hand) < 5:
            self.speak("STRANDING", "hand is small. playing junk")
            self.play_junk(list(self.board.tiles.values()))
            if len(self.hand) > 0:
                return self.restructure_board()
            return
        # new word: tuple(word, anchor, anchor is suffix)
        if self.play_best_strand_extension(strand_anchors):
            self.speak("STRANDING", "playing strand extension")
            return
        elif self.play_right_angle_word():
            self.speak("STRANDING", "playing right angle")
            return
        else:
            print("attempting to play junk because can't do anything else")
            self.play_junk(other_anchors)
            if len(self.hand) > 0:
                return self.restructure_board()
            return


    def restructure_board(self):
        '''If we cannot continue without our current board formation
        this function is called. It should made adjustments and try
        play a word again
        '''

        '''Current implementation removes all 'junk tiles' (stuff that isn't contributing to stranding)
        and dumps if it's stuck. Then play resumes.'''
        # print("attempted board restructure")
        self.remove_junk()
        old_hand = self.hand
        # print(self)
        if self.dump_on_failure:
            worst_letter_in_hand = min(self.hand, key = lambda char: letter_count[char]) # this could be more sophisticated
            # print(f"Dumping {worst_letter_in_hand}")
            self.game.dump(self, worst_letter_in_hand)
            self.dump_count += 1
            # print(f"new hand: {self.hand}")
            if len(old_hand) == len(self.hand):
                self.speak("ERROR", "tried to dump at the end and choked")
                exit(1)
                return "Error"
        else:
            print("restructured without dumping")
        
        self.dump_on_failure = True
        # TODO
        # return "Error"
        # raise NotImplementedError("Board restructuring not implemented yet")

    

    def find_strand_extending_anchors(self):
        '''
        used for the below find_strand_extension function. 
        returns tiles that have infinite space in 1 direction and some space at 90 degrees'''
        strand_extending_anchors = []
        for tile in self.board.tiles.values():
            if tile.vert_parent == None:
                if (tile.lims.left == MAX_LIMIT or tile.lims.right == MAX_LIMIT) and (tile.lims.up > 0 or tile.lims.down > 0):
                    strand_extending_anchors.append(tile)
            elif tile.horo_parent == None:
                if (tile.lims.up == MAX_LIMIT or tile.lims.down == MAX_LIMIT) and (tile.lims.left > 0 or tile.lims.right > 0):
                    strand_extending_anchors.append(tile)

        return strand_extending_anchors

    
    '''TODO: think about preferred side to strand e.g.
    FOLLOW
         EMBARGO
    It would be nicer to made GO or NO the stranding word rather than ON or OR
    '''
    def play_best_strand_extension(self, anchors: list[Tile]) -> Word|None:
        '''Finds the best and longest word that can be attached via a two letter word.'''
        # print("looking for strand extension")
        prefix_anchors = dict() # prefix of the new word
        suffix_anchors = dict() # suffix of the new word

        for anchor in anchors:
            pair_list = self.all_words.find_two_letters(anchor.char, self.hand)

            if anchor.vert_parent == None:
                parent = anchor.horo_parent
            else:
                parent = anchor.vert_parent
            if parent.num_before == 0:
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
                        dict_to_add_to[pair.string[1]] = (anchor, pair.string, 0)
            # if (parent.direction == VERTICAL and anchor.lims.left > 0) or (parent.direction == HORIZONTAL and anchor.lims.up > 0):
            if self.first_anchor_can_be_nth_char(anchor, parent, 1):
                # when the first_anchor char is second, you're good
                # when the first_anchor char is both, you're good
                # print(f"{anchor} can be the first letter in the 2 letter word")
                # TODO!!!! use hypothetical lims here
                for pair in pair_list:
                    if pair.string[1] == anchor.char:
                        dict_to_add_to[pair.string[0]] = (anchor, pair.string, 1)
        
        all_words = dict()

        for prefix in prefix_anchors.keys():
            words = self.forward_words.all_subwords(self.hand.replace(prefix,'',1), prefix)
            if len(words) > 0:
                local_best = long_with_best_rank(words)
                all_words[local_best] = "prefix"
        for suffix in suffix_anchors.keys():
            words = self.reverse_words.all_subwords(self.hand.replace(suffix,'',1), suffix)
            if len(words) > 0:
                local_best = long_with_best_rank(words)
                all_words[local_best] = "suffix"
        best_word = long_with_best_rank(list(all_words.keys()))
        if best_word == None:
            return False
        if len(best_word.string) < 3: 
            return False
        # print(f"best: {best_word.string}")
        if all_words[best_word] == "prefix":
            key_info = prefix_anchors[best_word.string[0]]
            second_anchor_index = 0
        else:
            key_info = suffix_anchors[best_word.string[-1]]
            second_anchor_index = len(best_word.string) - 1
        first_anchor = key_info[0]
        two_letter_word = key_info[1]
        first_anchor_index = key_info[2]
        second_anchor = self.play_word(two_letter_word, first_anchor, first_anchor_index)[0]
        self.play_word(best_word.string, second_anchor, second_anchor_index)
        return True
    
    def play_right_angle_word(self):
        '''Looks for words where either the first or last letter is already on the board'''
        '''TODO: use actual anchors, rather than the whole board'''

        # print("looking for right angle word")
        prefix_anchors = dict()
        suffix_anchors = dict()
        for anchor in self.board.tiles.values():
            if any(lim == MAX_LIMIT for lim in anchor.lims.lims):
                if anchor.horo_parent == None:
                    if anchor.lims.left == MAX_LIMIT:
                        suffix_anchors[anchor.char] = anchor
                    if anchor.lims.right == MAX_LIMIT:
                        prefix_anchors[anchor.char] = anchor
                elif anchor.vert_parent == None:
                    if anchor.lims.up == MAX_LIMIT:
                        suffix_anchors[anchor.char] = anchor
                    if anchor.lims.down == MAX_LIMIT:
                        prefix_anchors[anchor.char] = anchor
        # print("prefix anchors")
        # print(prefix_anchors)
        # print("suffix anchors")
        # print(suffix_anchors)
        all_words = dict()
        for prefix in prefix_anchors.keys():
            words = self.forward_words.all_subwords(self.hand.replace(prefix,'',1), prefix)
            for word in words:
                all_words[word] = (prefix_anchors[prefix], ANCHOR_IS_PREFIX)
            # all_words = all_words | set(words)
        for suffix in suffix_anchors.keys():
            words = self.reverse_words.all_subwords(self.hand.replace(suffix,'',1), suffix)
            for word in words:
                all_words[word] = (suffix_anchors[suffix], ANCHOR_IS_SUFFIX)
            # all_words = all_words | set(words)
        best_word = long_with_best_rank(list(all_words.keys()))
        if best_word == None:
            return False
        if len(best_word.string) < 3: return False
        if all_words[best_word][1] == ANCHOR_IS_PREFIX:

            anchor_index = 0
        else:
            anchor_index = len(best_word.string) - 1
        self.play_word(best_word.string, all_words[best_word][0], anchor_index)
        return True

        # print(f"best word: {best_word.string}, anchor: {all_words[best_word]}")
        if best_word.string.index(all_words[best_word].char) == 0:
            # then ANCHOR_IS_PREFIX
            return (best_word, all_words[best_word], ANCHOR_IS_PREFIX)
        else:
            return (best_word, all_words[best_word], ANCHOR_IS_SUFFIX)
        # if best_word.string[0] in prefix_anchors.keys():
        #     return (best_word, prefix_anchors[best_word.string[0]], ANCHOR_IS_PREFIX)
        # else:
        #     return (best_word, suffix_anchors[best_word.string[-1]], ANCHOR_IS_SUFFIX)


    def play_junk(self, anchors: list[Tile]):
        '''
        Go through the anchors, play as much as possible each time
        Everything played here is labeled as junk and will be removed at the next rearrange
        '''
        _verbose = True
        if _verbose: print('[!] Before Junk Hand:', self.hand)
        
        # sort anchors by usefulness
        anchors.sort(key = lambda anchor: pair_start_count[anchor.char] + pair_end_count[anchor.char], reverse=True)

        # Remove anchors that are junk
        anchors = [a for a in anchors if not a.is_junk]
        
        for letter in self.hand:
            candidates = best_anchor_candidates(letter, anchors)
            
            for anchor in candidates:
                # Try letter + anchor combination first.
                # if it doesn't work out, try anchor + letter.
                word = letter + anchor.char
                placement = where_to_play_word(word, anchor)
                
                if placement == NO_SPACE_FOR_WORD or not self.forward_words.is_word(word):
                    word = anchor.char + letter
                    placement = where_to_play_word(word, anchor)
                
                if placement == NO_SPACE_FOR_WORD or not self.forward_words.is_word(word): 
                    # Can't find an anchor 
                    continue
                
                if _verbose: print(f'[!] Playing letter + anchor ({letter}+{anchor.char}) = {word}')
                self.play_word(word, anchor, anchor_index=placement[0], is_junk=True)
                break
            
        if _verbose: print('[!] After Junk Hand:', self.hand)
        
    def remove_junk(self):
        '''
        Removes every tile where is_junk == True. 
        equivalent to removing every tile that was placed during play_junk.
        '''
        self.speak("STRANDING", "removing junk...")
        # print("board before: ")
        # print(self)
        bad_tiles = []
        for tile in self.board.tiles.values():
            if tile.is_junk:
                bad_tiles.append(tile)
        # print("bad_tiles: ")
        # print(bad_tiles)
        removed_tiles = self.board.remove_junk_tiles(bad_tiles)
        for tile in removed_tiles:
            # note that we are not using self.give_tiles. This is important, as self.give_tiles is only for new tiles. 
            self.hand += tile.char
        # print("junk on board now false")
        self.speak("STRANDING", "board after removing junk:")
        self.show_board()
        
        self.board.junk_on_board = False

    def hypothetical_lims(self, probe_coords):
        '''Finds the lims for any place on the board without modifying the lims of other tiles'''
        lims = [MAX_LIMIT] * 4
        probe_hits = send_probes(probe_coords, self.board)
        for probe in probe_hits:
            direction_for_sender = probe[1]
            dist = probe[3]
    
            lims[direction_for_sender] = min(lims[direction_for_sender], dist)
        return Lims(lims)

    def first_anchor_can_be_nth_char(self, anchor, parent, n):
        if parent.num_before == 0:
            is_suffix = 1 # the new char will be the suffix of the new word
        else:
            is_suffix = 0 # the new char will be the prefix of the new word
        if parent.direction == VERTICAL:
            hypothetical_lim_index = 0 + 2 * is_suffix # the strand will go down if prefix, up if suffix
            if n == 0:
                anchor_lim_index = 1 # right lim, as the new char will be to the right
                hypothetical_lim_offset = (0,1) # the new letter will be played to the right of the anchor
            else:
                anchor_lim_index = 3 # left lim, as the new char will be to the left
                hypothetical_lim_offset = (0,-1) # the new letter will be played to the left of the anchor

        if parent.direction == HORIZONTAL:
            hypothetical_lim_index = 1 + 2 * is_suffix # the strand will go to the right if prefix, left if suffix
            if n == 0:
                anchor_lim_index = 0 # down lim
                hypothetical_lim_offset = (1,0) # the new letter will be played below the anchor
            else:
                anchor_lim_index = 2 # up lim
                hypothetical_lim_offset = (-1,0) # the new letter will be played above the anchor
        hypothetical_coords = (anchor.coords[0] + hypothetical_lim_offset[0], anchor.coords[1] + hypothetical_lim_offset[1])
        # print(f"checking anchor can be index {n} char: anchor: {anchor} lim index: {anchor_lim_index}, hypothetical coords: {hypothetical_coords}")
        # print(f"hypothetical coords: {hypothetical_coords}, direction: {hypothetical_lim_index}")
        if anchor.lims.lims[anchor_lim_index] > 0 and self.hypothetical_lims(hypothetical_coords).lims[hypothetical_lim_index] == MAX_LIMIT:
            return True
        else: return False
                    