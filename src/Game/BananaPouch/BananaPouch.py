import random
starting_letters = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3,
                    "I": 12, "J": 2, "K": 2, "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2,
                    "R": 9, "S": 6, "T": 9, "U": 6, "V": 3, "W": 3, "X": 2, "Y": 3, "Z": 2}

# Class to describe the remaining letters, plus randomly retrieving some
# It currently creates a starting 21 and peels
# No functionality yet for dumps or letting the user know when there's not enough tiles left
# Everything for single player


class BananaPouch:
    # Uses starting_letters dict to make the list of letters in pouch
    def __init__(self):
        self.remaining = []
        self.reset()

    # Returns array of 21 letters
    def setup(self) -> list[str]:
        starting_chars = []
        for i in range(21):
            starting_chars.append(self.peel())
        return starting_chars

    # Take a random letter from the list of remaining letters
    def peel(self) -> str | int:
        if len(self.remaining) > 0:
            return self.remaining.pop(random.randint(0, len(self.remaining) - 1))
        else:
            return -1

    def reset(self):
        self.remaining = []
        for char in starting_letters.keys():
            for i in range(starting_letters[char]):
                self.remaining.append(char)
