from .Lims import Lims
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

        # down, right, up, left
    def find_lims(self) -> Lims:
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        lims = [MAX_LIMIT] * 4
        tiles = self.board.tiles
        for i in range(4):
            count = 0
            row = self.coords[0]
            col = self.coords[1]
            checked_tile = (row + dirs[i][0], col + dirs[i][1])
            # checking the immediate neighbour in that direction
            if checked_tile in tiles:
                tiles[checked_tile].lims.lims[i - 2] = 0
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
                        # there's 3 directions to check relative to the probe
                        # (everything but where the probe was previously)
                        for j in range(3):
                            checked_tile = (
                                row + dirs[(i + 1 - j) % 4][0],
                                col + dirs[(i + 1 - j) % 4][1])
                            if checked_tile in tiles:
                                # the lim direction to update in the other tile is the opposite of
                                # (i + 1 - j) = (i - 1 - j)
                                tiles[checked_tile].lims.lims[(i - j - 1)] = min(
                                    count,
                                    tiles[checked_tile].lims.lims[(i - j - 1)]
                                )
                                no_barriers = False
                                lims[i] = count
                    count += 1
        return Lims(lims)

    # note that self.board.min_row() etc don't take into account the tile just placed
    # hence a function for if the probe is on the board is worthwhile
    def probe_on_board(self, row: int, col: int) -> bool:
        min_r = min(self.board.min_row(), self.coords[0])
        max_r = max(self.board.max_row(), self.coords[0])
        min_c = min(self.board.min_col(), self.coords[1])
        max_c = max(self.board.max_col(), self.coords[1])
        if ((min_r <= row <= max_r) and
                (min_c <= col <= max_c)):
            return True
        else:
            return False
