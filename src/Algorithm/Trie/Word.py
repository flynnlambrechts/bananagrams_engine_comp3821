
class Word:

    def __init__(self, line):
        line_split = line.split(' ')
        self.word_string = line_split[0]
        self.num_startswith = int(line_split[1])
        self.num_endswith = int(line_split[2])
        self.letter_ranking = 0

    def has_anchor(self, anchor: str):
        remaining = self.word_string[:]
        for char in anchor:
            previous = remaining[:]
            remaining = remaining.replace(char, '', 1)
            if remaining == previous:
                return False
        return True

    def __str__(self) -> str:
        return f"{self.word_string} {self.num_startswith} {self.num_endswith} {self.letter_ranking}"
