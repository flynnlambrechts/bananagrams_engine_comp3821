from lims import Lims
from parent_word import ParentWord
from constants import *


class Tile:
    def __init__(self, board, row: int, col: int, char: str, parent_word: str = '', pos: int = 0, direction: int = 0):
        self.coords = (row, col)
        self.char = char
        self.board = board
        self.lims = self._update_lims()
        self.vert_parent: ParentWord|None = None
        self.horo_parent: ParentWord|None = None

        if direction == VERTICAL and len(parent_word) > 0:
            self.vert_parent = ParentWord(parent_word, pos, direction)
        elif direction == HORIZONTAL and len(parent_word) > 0:
            self.horo_parent = ParentWord(parent_word, pos, direction)
        '''
        dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        e.g. the go anticlockwise from 6:00.
        means that adding 2 to an index gets the opposite direction

        down, right, up, left
        '''

    def __repr__(self):
        return f"Tile: coords={self.coords}, char={self.char}"

    def _update_lims(self) -> Lims:
        '''
        Updates the limits of every tile that is impacted by the new tile placement
        '''
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
                    if not self._probe_on_board(row, col):
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
                                # for all hits: update tile that was hit
                                # in opposite direction to probe velocity
                                tiles[checked_tile].lims.lims[i - 2] = min(
                                    count,
                                    tiles[checked_tile].lims.lims[i - 2]
                                )
                                # if 'front on hit', also check diagonals, as they could also be impacted
                                if j == 1:

                                    diags = self._get_probe_diags(dirs[i])
                                    for diag in diags:
                                        checked_diag_tile = (
                                            checked_tile[0] + diag[0],
                                            checked_tile[1] + diag[1])
                                        if checked_diag_tile in tiles:
                                            tiles[checked_diag_tile].lims.lims[i - 2] = min(
                                                count + 1,
                                                tiles[checked_diag_tile].lims.lims[i - 2]
                                            )
                                elif count == 0:
                                    # if there's a diag immediately next to the tile, more than one direction is affected
                                    tiles[checked_tile].lims.lims[(i - j - 1)] = min(
                                        count,
                                        tiles[checked_tile].lims.lims[(i - j - 1)]
                                    )
                                # the lim direction to update in the other tile is the opposite of
                                # (i + 1 - j) = (i - 1 - j)
                                # if j == 1 or count == 0:

                                # else:
                                #     #sdljsdflksdjfldsfj
                                no_barriers = False
                                lims[i] = count
                    count += 1
        return Lims(lims)

    def _get_probe_diags(self, dir: tuple):
        x = dir[0]
        y = dir[1]

        if x == 0:
            return [(1, 0), (-1, 0)]
        else:
            return [(0, 1), (0, -1)]

    def _probe_on_board(self, row: int, col: int) -> bool:
        '''
        note that self.board.min_row() etc don't take into account the tile
        just placed hence a function for if the probe is on the board is
        worthwhile
        '''
        min_r = min(self.board.min_row(), self.coords[0])
        max_r = max(self.board.max_row(), self.coords[0])
        min_c = min(self.board.min_col(), self.coords[1])
        max_c = max(self.board.max_col(), self.coords[1])

        return (min_r <= row <= max_r) and (min_c <= col <= max_c)
