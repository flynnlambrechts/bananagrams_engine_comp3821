from .lims import Lims
from parent_word import ParentWord
from constants import *
from utils import add_tuple_elems


class Tile:
    def __init__(self, board, row: int, col: int, char: str, is_junk=False):
        self.coords = (row, col)
        self.char = char
        self.board = board
        
        self.lims = self._update_lims()
        # self.vert_parent: ParentWord | None = None
        # self.horo_parent: ParentWord | None = None
        self.parents = {HORIZONTAL: None, VERTICAL: None}

        self.is_junk = is_junk
        # if len(parent_word) > 0:
        #     if direction == VERTICAL:
        #         self.vert_parent = ParentWord(parent_word, direction)
        #     elif direction == HORIZONTAL:
        #         self.horo_parent = ParentWord(parent_word, direction)
        '''
        dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        e.g. the go anticlockwise from 6:00.
        means that adding 2 to an index gets the opposite direction

        down, right, up, left
        '''

    def __repr__(self):
        return f"Tile '{self.char}': coords={self.coords} is_junc={self.is_junction()}"

    def __str__(self):
        result = self.char
        is_junction = self.is_junction()
        is_dangling = self.is_dangling()
        if is_dangling and is_junction:
            result = bcolors.OKCYAN + result + bcolors.ENDC
        elif is_dangling:
            result = bcolors.OKGREEN + result + bcolors.ENDC
        elif is_junction:
            result = bcolors.FAIL + result + bcolors.ENDC
        return result
            

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
            tile.lims.lims[direction_for_receiver] = min(
                tile.lims.lims[direction_for_receiver], dist)
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
        
        for i, dir in enumerate(DIRECTIONS):
            count = 0
            (row, col) = self.coords
            checked_tile = (row + dir[0], col + dir[1])
            # checking the immediate neighbour in that direction
            if checked_tile in tiles:
                hit = (checked_tile, i, i - 2, count)
                probe_hits.append(hit)
                continue
            no_barriers = True
            while no_barriers:
                (row, col) = add_tuple_elems((row, col), dir)
                if not self._probe_on_board(row, col):
                    break
                for j in range(3):
                    checked_tile = add_tuple_elems((row, col), DIRECTIONS[(i + 1 - j) % 4])
                    if checked_tile in tiles:
                        hit = (checked_tile, i, i - 2, count)
                        probe_hits.append(hit)

                        if j == 1:
                            diags = self._get_probe_diags(dir)
                            for diag in diags:
                                checked_diag_tile = add_tuple_elems(checked_tile, diag)
                                if checked_diag_tile in tiles:
                                    hit = (checked_tile, i, i - 2, count)
                                    probe_hits.append(hit)
                        elif count == 0:
                            hit = (checked_tile, i, i - j - 1, count)
                            probe_hits.append(hit)
                count += 1
        return probe_hits
    
    def get_adjacent(self, direction: tuple[int, int]):
        (row, col) = self.coords
        return self.board.get_tile(row + direction[0], col + direction[1])
    
    def is_junction(self):
        # (row, col) = self.coords
        # has_horizontal = self.board.has_tile(row + 1, col) or self.board.has_tile(row - 1, col)
        # has_vertical = self.board.has_tile(row, col + 1) or self.board.has_tile(row, col - 1)
        # return has_horizontal and has_vertical
        return self.has_parent(HORIZONTAL) and self.has_parent(VERTICAL)
        
    def is_dangling(self) -> bool:
        if not self.has_parent(VERTICAL) and self.has_parent(HORIZONTAL):
            return self.get_parent(HORIZONTAL).is_dangling()
        elif not self.has_parent(HORIZONTAL) and self.has_parent(VERTICAL):
            return self.get_parent(VERTICAL).is_dangling()
        return False
        
    def add_parent(self, parent: ParentWord, direction: int):
        self.parents[direction] = parent
            
    def get_parent(self, direction: int):
        return self.parents[direction]
        
    def has_parent(self, direction) -> bool:
        return self.get_parent(direction) != None
    
    def pos_in_parent(self, direction):
        return self.get_parent(direction).pos(self)
    
    def num_before(self, direction):
        return self.pos_in_parent(self, direction)
    
    def num_after(self, direction):
        return self.get_parent(direction).len() - self.pos_in_parent(direction) - 1
    
    def remove_from_board(self, parent_direction: int|None) -> bool:
        """Returns true if the tile was successfully removed, returns false
        if the tile still had another parent holding it on the board
        """
        if not self.has_parent(HORIZONTAL) or not self.has_parent(VERTICAL):
            self.board.remove_tile(*self.coords)
            return True
        else:
            self.add_parent(None, parent_direction)
            return False
