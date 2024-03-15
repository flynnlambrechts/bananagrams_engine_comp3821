MAX_LIMIT = 50

class Tile:
    def __init__(self, board, row, col, char):
        self.coords = (row, col)
        self.char = char
        self.lims = []
        self.board = board
        print("max and min rows: ")
        print(self.board.min_row(), self.board.max_row())
        print("max and min cols: ")
        print(self.board.min_col(), self.board.max_col())
        self.lims.append(self.find_lims(1,0))
        self.lims.append(self.find_lims(-1,0))
        self.lims.append(self.find_lims(0,1))
        self.lims.append(self.find_lims(0,-1))

    def find_lims(self, dr, dc):
        print(f"going in direction {dr}, {dc}")
        count = -1
        cur_row = self.coords[0]
        cur_col = self.coords[1]
        no_barriers = True
        while(no_barriers):
            count += 1
            cur_row += dr
            cur_col += dc
            print(f"At ({cur_row}, {cur_col})")
            check_tiles = [(cur_row + dr, cur_col + dc),
                           (cur_row + dc, cur_col + dr),
                           (cur_row - dc, cur_col - dr),
                           (cur_row, cur_col)
                        #    (cur_row + (dr + 1) % 2, cur_row + (dc + 1) % 2),
                        #    (cur_row - ((dr + 1) % 2), cur_row - ((dc + 1) % 2))
                        ]
            print(f"check_tiles are {check_tiles}")
            for tile in check_tiles:
                if tile in self.board.tiles:
                    print("collision!")
                    no_barriers = False
                    lims_pos = int((abs(dr) * (dr - 1) / -2) + (abs(dc) * ((dr - 1) / -2 + 2)))
                    updateable = self.board.tiles[tile].lims
                    updateable[lims_pos] = min(updateable[lims_pos], count)
            if not ((self.board.min_row() <= cur_row <= self.board.max_row()) and (self.board.min_col() <= cur_col <= self.board.max_col())):
                return MAX_LIMIT
            
        return count        

        
class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int]] = {}

    def min_row(self):
        if len(self.tiles) == 0:
            return 0
        return min([row for row, _ in self.tiles])
    
    def max_row(self):
        if len(self.tiles) == 0:
            return 0
        return max([row for row, _ in self.tiles])
    
    def min_col(self): 
        if len(self.tiles) == 0:
            return 0        
        return min([col for _, col in self.tiles])

    def max_col(self): 
        if len(self.tiles) == 0:
            return 0
        return max([col for _, col in self.tiles])

    # This allows us to use print(board)
    def __str__(self) -> str:
        if not self.tiles:
            return "Board is empty"
        col_delim = " "

        # min_row = min([row for row, _ in self.tiles])
        # max_row = max([row for row, _ in self.tiles])
        # min_col = min([col for _, col in self.tiles])
        # max_col = max([col for _, col in self.tiles])


        header = 4*" " + col_delim.join(
            map(lambda x: x[-1],
                map(str, range(self.min_col(), self.max_col() + 1))
            )
            ) + "\n"

        s =  header + f"{self.min_row():>4}"
        
        cur_row = self.min_row()
        cur_col = self.min_col()
        for (row, col), value in sorted(self.tiles.items(), key=lambda item: (item[0][0], item[0][1])):
            while cur_row < row:
                cur_row += 1
                cur_col = 0
                s += f"\n{cur_row:>4}"
            skipped = 0
            while cur_col < col:
                cur_col += 1
                skipped += 1
            
            s += 2*(skipped-1)*col_delim + value.char + col_delim
            cur_col += 1
            
        return s
    
        
    def add_tile(self, tile: str, row: int, col: int) -> None:
        tile = tile.upper()
        if len(tile) != 1:
            raise ValueError('Tile must be one character long')
        if (row, col) in self.tiles and self.tiles[(row, col)] != tile:
            raise ValueError(f'There is already a tile at ({row}, {col})')
        print(f"Adding {tile} to {row},{col}")
        self.tiles[(row,col)] = Tile(self, row, col, tile)
        # # Future nodes for caching sequences/words
        # adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        
        # if all([coord not in self.tiles for coord in adjacent]):
        #     # No character tiles around it
        #     self.tiles[(row, col)] = tile
        #     return
        
        # self.tiles[(row, col)] = tile
        
    def remove_tile(self, row: int, col: int) -> str:
        if (row, col) not in self.tiles:
            raise ValueError(f'There is no tile at ({row}, {col})')
        
        return self.tiles.pop((row, col))
        

    def add_word(self, word:str, row: int, col: int, direction: int, reverse=False) -> None:
        # direction of 1 means vertical
        # direction of 0 means horizontal
        VERTICAL = 1
        HORIZONTAL = 0
        print("adding word")
        dr = int(direction == VERTICAL)
        dc = int(direction == HORIZONTAL)
        if (reverse):
            dr *= -1
            dc *= -1
            word = word[::-1]

        for i, c in enumerate(word):
            self.add_tile(c, row + i * dr, col + i * dc)

