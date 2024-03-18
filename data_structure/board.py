MAX_LIMIT = 50

class Tile:
    def __init__(self, board, row: int, col: int, char: str):
        self.coords = (row, col)
        self.char = char
        self.board = board
        self.lims = self.find_lims()
        # dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        # e.g. the go anticlockwise from 6:00. 
        # means that adding 2 to an index gets the opposite direction
    def find_lims(self):
        dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        lims = [MAX_LIMIT] * 4
        tiles = self.board.tiles
        for i in range(4):
            count = 0
            row = self.coords[0]
            col = self.coords[1]
            checked_tile = (row + dirs[i][0], col + dirs[i][1])
            # checking the immediate neighbour in that direction
            if checked_tile in tiles:
                tiles[checked_tile].lims[i - 2] = 0
                lims[i] = 0                
            else:
                # send a probe out checking until it goes off the edge or there's a collision
                # if collision, suitably update the limits of both tiles
                no_barriers = True
                while no_barriers:
                    row += dirs[i][0]
                    col += dirs[i][1]
                    if not self.probe_on_board(row, col):                 
                        lims[i] = MAX_LIMIT
                        no_barriers = False
                    else:
                        # there's 3 directions to check relative to the probe (everything but where the probe was previously)
                        for j in range(3):
                            checked_tile = (row + dirs[(i + 1 - j) % 4][0], col + dirs[(i + 1 - j) % 4][1])
                            if checked_tile in tiles:
                                tiles[checked_tile].lims[(i - j - 1)] = min(count, tiles[checked_tile].lims[(i - j - 1)]) # the lim direction to update in the other tile is the opposite of (i + 1 - j) = (i - 1 - j)
                                no_barriers = False
                                lims[i] = count
                    count += 1
        return lims    

    # note that self.board.min_row() etc don't take into account the tile just placed
    # hence a function for if the probe is on the board is worthwhile
    def probe_on_board(self, row, col):
        min_r = min(self.board.min_row(), self.coords[0])
        max_r = max(self.board.max_row(), self.coords[0])
        min_c = min(self.board.min_col(), self.coords[1])
        max_c = max(self.board.max_col(), self.coords[1])
        if ((min_r <= row <= max_r) and 
                (min_c <= col <= max_c)):
            return True
        else:
            return False
        
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
        if (row, col) in self.tiles and self.tiles[(row, col)].char != tile:
            raise ValueError(f'There is already a tile at ({row}, {col})')
        print(f"Adding {tile} to {row},{col}")
        self.tiles[(row,col)] = Tile(board = self, row = row, col = col, char = tile)
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
        print(f"adding word [{word}]")
        dr = int(direction == VERTICAL)
        dc = int(direction == HORIZONTAL)
        if (reverse):
            dr *= -1
            dc *= -1
            word = word[::-1]
        # print(f"dr: {dr} dc: {dc}")
        for i, c in enumerate(word):
            self.add_tile(c, row + i * dr, col + i * dc)

