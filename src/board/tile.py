from .lims import Lims
from parent_word import ParentWord
from constants import *


class Tile:
    def __init__(self, board, row: int, col: int, char: str, parent_word: str = '', pos: int = 0, direction: int = 0, is_junk = False):
        self.coords = (row, col)
        self.char = char
        self.board = board
        self.lims = self._update_lims()
        self.vert_parent: ParentWord|None = None
        self.horo_parent: ParentWord|None = None
        
        self.is_junk = is_junk
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
        lims = [MAX_LIMIT] * 4
        probe_hits = self.send_probes(self.board.tiles)
        # probe_hits is in the format
        # (coords, direction for probe sender, direction for probe receiver, count)
        for probe in probe_hits:
            tile = self.board.tiles[probe[0]]
            direction_for_sender = probe[1]
            direction_for_receiver = probe[2]
            dist = probe[3]
            tile.lims.lims[direction_for_receiver] = min(tile.lims.lims[direction_for_receiver], dist)
            lims[direction_for_sender] = min(lims[direction_for_sender], dist)
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

    def send_probes(self, tiles):
        probe_hits = []
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for i in range(4):
            count = 0
            row = self.coords[0]
            col = self.coords[1]
            checked_tile = (row + dirs[i][0], col + dirs[i][1])
            # checking the immediate neighbour in that direction
            if checked_tile in tiles:
                hit = (checked_tile, i, i - 2, count)
                probe_hits.append(hit)
                continue
            no_barriers = True
            while no_barriers:
                row += dirs[i][0]
                col += dirs[i][1]
                if not self._probe_on_board(row, col):
                    break
                for j in range(3):
                    checked_tile = (
                        row + dirs[(i + 1 - j) % 4][0],
                        col + dirs[(i + 1 - j) % 4][1])
                    if checked_tile in tiles:
                        hit = (checked_tile, i, i - 2, count)
                        probe_hits.append(hit)
                        
                        if j == 1:
                            diags = self._get_probe_diags(dirs[i])
                            for diag in diags:
                                checked_diag_tile = (
                                    checked_tile[0] + diag[0],
                                    checked_tile[1] + diag[1])
                                if checked_diag_tile in tiles:
                                    hit = (checked_tile, i, i - 2, count)
                                    probe_hits.append(hit)
                        elif count == 0:
                            hit = (checked_tile, i, i - j - 1, count)
                            probe_hits.append(hit)
                count += 1
        return probe_hits

    # function that sends probes, returns all required info for update_tile, but also all required info for after deleting a tile