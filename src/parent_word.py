from constants import HORIZONTAL

class ParentWord:
    def __init__(self, word: str, pos: int, direction: int) -> None:
        self.word: str = word
        self.num_before = pos
        self.num_after = len(word) - pos - 1
        self.direction = direction

    def __str__(self) -> str:
        string = "[word: " + self.word + " nums: before: " + \
            str(self.num_before) + " after: " + str(self.num_after) + " dir: "
        if self.direction == HORIZONTAL:
            string += "horo]"
        else:
            string += "vert]"
        return string
    '''
    Class determining where in a word, and in what word a tile is
    Using the same protocol for direction as in add_word
    '''
