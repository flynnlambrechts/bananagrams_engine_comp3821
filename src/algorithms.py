from word import Word


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
