from random import randint
from collections import Counter


starting_letters = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4,
                    "H": 3, "I": 12, "J": 2, "K": 2, "L": 5, "M": 3, "N": 8,
                    "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6,
                    "V": 3, "W": 3, "X": 2, "Y": 3, "Z": 2}


class Pouch:
    '''
    Describes the remaining letters, plus randomly retrieving some.
    It currently creates a starting 21 and peels. No functionality
    yet for dumps or letting the user know when there's
    not enough tiles left Everything for single player.
    '''

    def __init__(self):
        '''
        Uses starting_letters dict to make the list of letters in pouch
        '''
        self.remaining = []
        self.reset()

    def get_starting_tiles(self, n=21) -> list[str]:
        '''
        Returns array of n letters
        '''
        starting_chars = []
        for i in range(21):
            starting_chars.append(self.peel())
        return starting_chars

    def peel(self) -> str | int:
        '''
        Take a random letter from the list of remaining letters
        '''
        if len(self.remaining) > 0:
            return self.remaining.pop(randint(0, len(self.remaining) - 1))
        else:
            return -1

    def reset(self):
        self.remaining = []
        for char in starting_letters.keys():
            for i in range(starting_letters[char]):
                self.remaining.append(char)

    def n_remaining(self):
        return len(self.remaining)
    
    def __str__(self):
        return (str(dict(Counter(self.remaining))))
    
    def dump(self, char: str) -> str:
        if len(char) != 1:
            raise ValueError("Expected one char, got 0 or multiple")
        self.remaining.append(char)
        newtiles = []
        for i in range(3):
            if len(self.remaining) > 0:
                newtiles.append(self.peel())
        return newtiles
