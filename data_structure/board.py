class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int]] = {}
        
    # This allows us to use print(board)
    def __str__(self) -> str:
        col_delim = " "

        min_row = min([row for row, _ in self.tiles])
        max_row = max([row for row, _ in self.tiles])
        min_col = min([col for _, col in self.tiles])
        max_col = max([col for _, col in self.tiles])


        header = 4*" " + col_delim.join(
            map(lambda x: x[-1],
                map(str, range(min_col, max_col + 1))
            )
            ) + "\n"

        s =  header + f"{min_row:>4}"
        
        cur_row = min_row
        cur_col = min_col
        for (row, col), value in sorted(self.tiles.items(), key=lambda item: (item[0][0], item[0][1])):
            while cur_row < row:
                cur_row += 1
                cur_col = min_col
                s += f"\n{cur_row:>4}"
            skipped = 0
            while cur_col < col:
                cur_col += 1
                skipped += 1
            s += 2 * max(0, skipped) * col_delim + value + col_delim
            cur_col += 1
            
        return s
    
        
    def add_tile(self, tile: str, row: int, col: int) -> None:
        tile = tile.upper()
        if len(tile) != 1:
            raise ValueError('Tile must be one character long')
        if (row, col) in self.tiles and self.tiles[(row, col)] != tile:
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
        


    def add_word(self, word:str, row: int, col: int, direction: int, reverse=False) -> None:
        # direction of 1 means vertical
        # direction of 0 means horizontal
        VERTICAL = 1
        HORIZONTAL = 0

        dr = int(direction == VERTICAL)
        dc = int(direction == HORIZONTAL)
        if (reverse):
            dr *= -1
            dc *= -1
            word = word[::-1]

        for i, c in enumerate(word):
            self.add_tile(c, row + i * dr, col + i * dc)

