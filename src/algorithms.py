from word import Word
from board.tile import Tile
from constants import NO_SPACE_FOR_WORD, HORIZONTAL, VERTICAL, TOTAL_TILE_COUNT
from pouch import letter_distribution
is_prefix_of = {'A': 16194, 'B': 15218, 'C': 25015, 'D': 16619, 'E': 11330, 'F': 10633, 'G': 9351, 'H': 10524, 'I': 9604, 'J': 2311, 'K': 3361, 'L': 8058, 'M': 15811, 'N': 6564, 'O': 8895, 'P': 24327, 'Q': 1411, 'R': 15014, 'S': 31986, 'T': 14563, 'U': 9522, 'V': 4590, 'W': 5921, 'X': 309, 'Y': 1036, 'Z': 1159}
is_suffix_of = {'A': 5560, 'B': 371, 'C': 6121, 'D': 25039, 'E': 28261, 'F': 534, 'G': 20216, 'H': 3293, 'I': 1601, 'J': 12, 'K': 2327, 'L': 8586, 'M': 4620, 'N': 12003, 'O': 1887, 'P': 1547, 'Q': 10, 'R': 14784, 'S': 107294, 'T': 13933, 'U': 379, 'V': 45, 'W': 610, 'X': 583, 'Y': 19551, 'Z': 159}
pair_start_count = {'A': 16, 'B': 5, 'C': 1, 'D': 4, 'E': 13, 'F': 3, 'G': 3, 'H': 5, 'I': 6, 'J': 2, 'K': 4, 'L': 3, 'M': 7, 'N': 5, 'O': 17, 'P': 4, 'Q': 1, 'R': 1, 'S': 4, 'T': 4, 'U': 8, 'V': 0, 'W': 2, 'X': 2, 'Y': 4, 'Z': 3}
pair_end_count = {'A': 15, 'B': 2, 'C': 0, 'D': 4, 'E': 15, 'F': 3, 'G': 2, 'H': 6, 'I': 14, 'J': 0, 'K': 1, 'L': 2, 'M': 6, 'N': 5, 'O': 17, 'P': 2, 'Q': 0, 'R': 4, 'S': 5, 'T': 5, 'U': 6, 'V': 0, 'W': 3, 'X': 3, 'Y': 7, 'Z': 0}



def where_to_play_word(word_str: str, anchor: Tile) -> tuple[int, int]:
    '''
    Given an anchor and a word, determines if there's space to play it. 
    If there is space to play it, it returns the index of the character in the word and direction as (index, direction),
    Returning NO_SPACE_FOR_WORD (-1,-1) if there is no space to play it on the given anchor. 
    '''
    if anchor is None:
        return (0, HORIZONTAL)

    lims = anchor.lims
    # step 1: find all instances of the anchor in word.
    # for all in instances of anchor in word:
    # 2: calculate forward and backward requirements
    # 3: true if there's a 50/50 instance
    # 4: true if it fits within an instance
    # 5: true if it can go in one direction and it's not extending a word
    # if (lims.down == MAX_LIMIT and lims.up == MAX_LIMIT) or (lims.left == MAX_LIMIT and lims.right == MAX_LIMIT):
    #     return True
    anchor_indexes = [i for i, t in enumerate(word_str) if t == anchor.char]
    for anchor_index in anchor_indexes:
        tiles_before = anchor_index
        tiles_after = len(word_str) - anchor_index - 1
        if lims.left and lims.right and lims.left >= tiles_before and lims.right >= tiles_after:
            return (anchor_index, HORIZONTAL)
        if lims.up and lims.down and lims.up >= tiles_before and lims.down >= tiles_after:
            return (anchor_index, VERTICAL)

        if tiles_before == 0:
            if lims.down >= tiles_after and anchor.vert_parent == None:
                return (anchor_index, VERTICAL)
            if lims.right >= tiles_after and anchor.horo_parent == None:
                return (anchor_index, HORIZONTAL)
        if tiles_after == 0:
            if lims.up >= tiles_before and anchor.vert_parent == None:
                return (anchor_index, VERTICAL)
            if lims.left >= tiles_before and anchor.horo_parent == None:
                return (anchor_index, HORIZONTAL)
    return NO_SPACE_FOR_WORD


def long_with_best_rank(words: list[Word], rank_strategy = "strand",anchor: Tile = None, closeness_to_longest = 0) -> Word:
    '''
    Finds a long subword with the lowest letter_ranking
    (Means that it uses letters that appear less in the dictionary),
    The heuristic can be changed to:
    use many letters that start/appear in short words or
    use many letters that cannot easily make short words

    closeness_to_longest determines the length of words relative to the longest word that can be considered
    '''

    words = [word for word in words if where_to_play_word(word.string, anchor) != NO_SPACE_FOR_WORD]

    if len(words) == 0:
        return None
    longest: Word = max(words, key=lambda word: len(word.string))

    long_words = []
    for word in words:
        if len(word.string) >= len(longest.string) - closeness_to_longest:
            long_words.append(word)

    if len(long_words) == 0:
        return None
    if rank_strategy == "strand":
        return max(long_words, key=lambda word: score_word_simple_stranding(word.string))
    else:
        return min(long_words, key=lambda word: word.letter_ranking / len(word.string))

def long_with_lowest_rank(subwords, anchor: Tile = None, closeness_to_longest=0, attempt=0) -> Word:
    '''
    Finds a long subword with the lowest letter_ranking
    (Means that it uses letters that appear less in the dictionary),
    The heuristic can be changed to:
    use many letters that start/appear in short words or
    use many letters that cannot easily make short words

    closeness_to_longest determines the length of words relative to the longest word that can be considered
    '''

    words = [word for word in subwords if where_to_play_word(
        word.string, anchor) != NO_SPACE_FOR_WORD]

    if len(words) == 0:
        return None
    longest: Word = max(words, key=lambda word: len(word.string))

    long_words = []
    for word in words:
        if len(word.string) >= len(longest.string) - closeness_to_longest:
            long_words.append(word)

    if len(long_words) == 0:
        return None
    long_words.sort(key=lambda word: word.letter_ranking / len(word.string))

    # min_word = min(long_words, key=lambda word: word.letter_ranking / len(word.string))
    if attempt >= len(long_words):
        print(f"attempt: {attempt}, len(long_words): {len(long_words)}")
        return None
    return long_words[attempt]


'''None of the below is actually being used'''
def anchor_ranking(tiles: dict[tuple[int, int]]) -> list:
    tile_list = list(tiles.values())
    return sorted(tile_list, key=lambda tile: _eval_anchor_candidate(tile), reverse=True)
def anchor_ranking(tiles: dict[tuple[int, int]]) -> list:
    tile_list = list(tiles.values())
    return sorted(tile_list, key=lambda tile: _eval_anchor_candidate(tile), reverse=True)


def _eval_anchor_candidate(tile: Tile) -> int:
    '''
    Currently very simple way of giving a numeric score to a possible anchor.
    Total of the limits in every direction plus a bonus if there's space on opposite sides
    (e.g. you can add, not just extend words)
    '''
    score = 0
    score += sum(tile.lims.lims)
    if (tile.lims.left() > 8 and tile.lims.right() > 8) or (
            tile.lims.up() > 8 and tile.lims.down() > 8):
        score += 100
    return score

# def best_next_strand(words, )

'''so much room for more interesting stuff, but it's a start'''
def score_word_simple_stranding(word_str, min_length = 0):
    if word_str == None:
        return -1000000
    if len(word_str) < min_length:
        return -1000000
    # all_other_letters = self._all_other_letters(word_str)
    if len(word_str) > 2:
        word_middle = word_str[1:-1]
        middle_score = sum(pair_end_count[char] + pair_start_count[char] for char in word_middle) / (len(word_str) - 2)
    else:
        middle_score = 0
    
    edge_score = (is_prefix_of[word_str[0]] + is_suffix_of[word_str[0]] + 
                  is_prefix_of[word_str[-1]] + is_suffix_of[word_str[-1]] + 
                  (pair_end_count[word_str[0]] + pair_start_count[word_str[0]] +
                  pair_end_count[word_str[-1]] + pair_start_count[word_str[-1]]) * 1000)
    
    
    return edge_score - 1000 * middle_score

def _all_other_letters(self, word_str):
    all_other_letters = self.hand
    for char in word_str:
        all_other_letters.replace('',char,1)
    all_other_letters += ''.join([tile.string for tile in self.board.tiles.values()])
    return all_other_letters

def score_word_hand_balance(word_str: str, hand: str, anchor: str, min_length: int = 0):
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
        initial_unbalance += abs(hand.count(char)/hand_len - letter_distribution[char]/144)
    post_unbalance = 0
    for char in set(hand):
        post_unbalance += abs(hand_after_playing.count(char)/hand_after_playing_len - letter_distribution[char]/144)
    
    return initial_unbalance - post_unbalance
     
    