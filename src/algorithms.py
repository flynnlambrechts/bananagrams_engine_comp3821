from .word import Word
from .tile import Tile
from .constants import NO_SPACE_FOR_WORD, HORIZONTAL, VERTICAL

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

def long_with_lowest_rank(subwords, anchor: Tile = None, closeness_to_longest = 0, attempt = 0) -> Word:
    '''
    Finds a long subword with the lowest letter_ranking
    (Means that it uses letters that appear less in the dictionary),
    The heuristic can be changed to:
    use many letters that start/appear in short words or
    use many letters that cannot easily make short words

    closeness_to_longest determines the length of words relative to the longest word that can be considered
    '''

    words = [word for word in subwords if where_to_play_word(word.string, anchor) != NO_SPACE_FOR_WORD]

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
