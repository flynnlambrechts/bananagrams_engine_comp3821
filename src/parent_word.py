from constants import HORIZONTAL, VERTICAL

class ParentWord:
    '''
    Class determining where in a word, and in what word a tile is
    Using the same protocol for direction as in add_word
    '''
    def __init__(self, word: str, direction: int) -> None:
        self.word: str = word
        self.direction = direction
        self.tiles = [None] * len(word)
        
    def add_tile(self, tile, pos):
        self.tiles[pos] = tile
        tile.add_parent(self, self.direction)
        
    def get_tiles(self):
        return self.tiles

    def __str__(self) -> str:
        return f"String: {self.word}, Length: {len(self.tiles)}, Direction: {self.direction}, Junctions {self.count_junctions()}, Tiles {self.tiles}"

    def count_junctions(self):
        count = 0
        for tile in self.tiles:
            if tile.is_junction():
                count += 1
        return count
    
    def is_dangling(self):
        return self.count_junctions() <= 1
    
    def remove_from_board(self):
        tiles = []
        for tile in self.tiles:
            if tile.remove_from_board(self.direction):
                tiles.append(tile)
                
        return tiles

    def pos(self, tile):
        return self.tiles.index(tile)
    
    def len(self):
        return len(self.word)