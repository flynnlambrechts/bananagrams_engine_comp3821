from word import Word
from tile import Tile


def long_with_lowest_rank(subwords, anchor: Tile = None) -> Word:
    '''
    Finds a long subword with the lowest letter_ranking
    (Means that it uses letters that appear less in the dictionary),
    The heuristic can be changed to:
    use many letters that start/appear in short words or
    use many letters that cannot easily make short words
    '''
    def word_has_space(word: Word, anchor: Tile) -> bool:
        if anchor is None:
            return True

        lims = anchor.find_lims()

        if lims.down and lims.up:
            return True
        elif lims.left and lims.right:
            return True

        return False

    words = [word for word in subwords if word_has_space(word, anchor)]

    if len(words) == 0:
        return None
    longest: list[Word] = max(words, key=lambda word: len(word.string))

    long_words = []
    for word in words:
        if len(str(word)) >= len(str(longest)) - 3:
            long_words.append(word)

    if len(long_words) == 0:
        return None
    min_word = min(long_words, key=lambda word: word.letter_ranking)
    return min_word
