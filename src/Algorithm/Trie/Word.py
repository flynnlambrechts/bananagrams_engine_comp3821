
class Word:

    def __init__(self, line):
        line_split = line.split(' ')
        self.string = line_split[0]
        self.num_startswith = int(line_split[1])
        self.num_endswith = int(line_split[2])
        self.letter_ranking = 0

    def has_anchor(self, anchor: str):
        return (len(anchor) == 0 or
                any([char in self.string for char in anchor]))

    # Used to support str(word) functionality
    def __str__(self) -> str:
        # return (f"{self.string} {self.num_startswith}" +
        # f"{self.num_endswith} {self.letter_ranking}")
        return self.string
