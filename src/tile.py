from .lims import Lims
from .parent_word import ParentWord
from .constants import *
from .lims_algos import send_probes
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
        probe_hits = send_probes(self.coords, self.board)
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



    

    # function that sends probes, returns all required info for update_tile, but also all required info for after deleting a tile