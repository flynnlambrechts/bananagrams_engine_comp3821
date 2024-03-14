
class Word:
    
    def __init__(self, line):
        line_split = line.split(' ')
        self.word = line_split[0]
        self.num_startswith = int(line_split[1])
        self.num_endswith = int(line_split[2])
        self.letter_ranking = 0
    
    def get_word(self):
        return self.word
    
    def get_num_startswith(self):
        return self.num_startswith
    
    def get_num_endswith(self):
        return self.num_endswith
    
    def get_letter_rank(self):
        return self.letter_ranking
    
    def set_letter_rank(self, rank):
        self.letter_ranking = rank