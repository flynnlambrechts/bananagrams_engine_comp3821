from typing import Optional


class Character:
    def __init__(self, value: str, row: int, col: int) -> None:
        self.value = value
        self.row = row
        self.col = col

class Align:
    SINGLE = 'single'
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'

class Word:
    def __init__(self, start_row: int, start_col: int, align: str, length: int) -> None:
        self.start_row = start_row
        self.start_col = start_col
        self.align = align
        self.length = length
        
        if self.align == Align.VERTICAL:
            self.end_row = self.start_row
            self.end_col = self.start_col + self.length - 1
        else:
            self.end_row = self.start_row + self.length - 1
            self.end_col = self.start_col

class Board:
    def __init__(self) -> None:
        self.characters: list[Character] = []
        self.words: list[Word] = []
        self.max_row = None
        self.max_col = None
        self.min_row = None
        self.min_col = None
        
    def coord_lookup(self, row: int, col: int) -> Optional[str]:
        for char in self.characters:
            if char.row == row and char.col == col:
                return char.value
        return None
    
    def word_lookup(self, row: int, col: int) -> Optional[Word]:
        for word in self.words:
            if word.start_row == row and word.start_col == col:
                return word
        return None
    
    def add_character(self, char: str, row: int, col: int) -> None:
        if (self.coord_lookup(row - 1, col) 
            == self.coord_lookup(row + 1, col) 
            == self.coord_lookup(row, col - 1) 
            == self.coord_lookup(row, col + 1) 
            == None):
            self.words.append(Word(row, col, Align.SINGLE), 1)
            self.characters.append(Character(char, row, col))
            return
        
        if (row_successor := self.coord_lookup(row + 1, col)) != None:
            pass
        
        if (col_successor := self.coord_lookup(row, col + 1)) != None:
            pass
        
        
        if (row_predecessor := self.coord_lookup(row - 1, col)) != None:
            pass
        
        if (col_predecessor := self.coord_lookup(row, col - 1)) != None:
            pass
