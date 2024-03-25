from word import Word
from tile import Tile


def long_with_lowest_rank(subwords) -> Word:
    '''
    Finds a long subword with the lowest letter_ranking
    (Means that it uses letters that appear less in the dictionary),
    The heuristic can be changed to:
    use many letters that start/appear in short words or
    use many letters that cannot easily make short words
    '''

    if len(subwords) == 0:
        return None
    longest: list[Word] = max(subwords, key=lambda word: len(word.string))

    long_subwords = []
    for word in subwords:
        if len(str(word)) >= len(str(longest)) - 3:
            long_subwords.append(word)

    if len(long_subwords) == 0:
        return None
    min_word = min(long_subwords, key=lambda word: word.letter_ranking)
    return min_word


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
