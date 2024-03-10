class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int]] = {}
        
    # This allows us to use print(board)
    def __str__(self) -> str:
        s = ''
        min_row = min([row for row, _ in self.tiles])
        min_col = min([col for _, col in self.tiles])
        
        cur_row = min_row
        cur_col = min_col
        for (row, col), value in sorted(self.tiles.items(), key=lambda item: (item[0][0], item[0][1])):
            while cur_row < row:
                cur_row += 1
                cur_col = 0
                s += '\n'
            while cur_col < col:
                cur_col += 1
                s += ' '
            
            s += value
            cur_col += 1
            
        return s
    
        
    def add_tile(self, tile: str, row: int, col: int) -> None:
        if len(tile) != 1:
            raise ValueError('Tile must be one character long')
        if (row, col) in self.tiles:
            raise ValueError(f'There is already a tile at ({row}, {col})')
        
        # # Future nodes for caching sequences/words
        # adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        # 
        # if all([coord not in self.tiles for coord in adjacent]):
        #     # No character tiles around it
        #     self.tiles[(row, col)] = tile
        #     return
        
        self.tiles[(row, col)] = tile
        
    def remove_tile(self, row: int, col: int) -> str:
        if (row, col) not in self.tiles:
            raise ValueError(f'There is no tile at ({row}, {col})')
        
        return self.tiles.pop((row, col))
        