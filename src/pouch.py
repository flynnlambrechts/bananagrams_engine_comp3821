import random
import time
from constants import letter_distribution


class Pouch:
    '''
    Describes the remaining letters, plus randomly retrieving some.
    It currently creates a starting 21 and peels. No functionality
    yet for dumps or letting the user know when there's
    not enough tiles left Everything for single player.
    '''

    def __init__(self, seed=None):
        '''
        Uses starting_letters dict to make the list of letters in pouch
        '''
        self.remaining = []
        self.reset()
        self.seed = seed
        if self.seed == None:
            self.seed = int(time.time())
        random.seed(self.seed)

    def n_remaining(self):
        return len(self.remaining)

    def get_starting_tiles(self, n=21) -> list[str]:
        '''
        Returns array of n letters
        '''
        return [self.peel() for _ in range(n)]

    def peel(self) -> str | int:
        '''
        Take a random letter from the list of remaining letters
        '''
        if len(self.remaining) > 0:
            return self.remaining.pop(random.randint(0, len(self.remaining) - 1))
        raise ValueError("Not Enough tiles for peel")

    def reset(self):
        self.remaining = [char for char, count in letter_distribution.items()
                          for _ in range(count)]

    def dump(self, char: str) -> str:
        if len(char) != 1:
            raise ValueError("Expected one char, got 0 or multiple")

        self.remaining.append(char)
        newtiles = [self.peel() for _ in range(3) if len(self.remaining) > 0]
        return newtiles
