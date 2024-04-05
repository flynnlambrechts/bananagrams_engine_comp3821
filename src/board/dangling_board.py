
from board.board import Board
from board.tile import Tile
from utils import add_tuple_elems, multiply_tuple_elems

class DanglingBoard(Board):
    def __init__(self) -> None:
        super().__init__()
        self.dangling: list[Tile] = []
    
    def add_word(self, word: str, row: int, col: int, direction: int, reverse=False, is_junk=False, anchor=None) -> list[Tile]:
        if anchor:
            # Any tile directly connected to the anchor is no longer dangling
            dir = (0, 0)
            parent = None
            if anchor.horo_parent:
                dir = (0, 1)
                parent = anchor.horo_parent
            elif anchor.vert_parent:
                dir = (1, 0)
                parent = anchor.vert_parent
            if parent:
                pos = anchor.coords
                for i in range(parent.num_before):  
                    pos = add_tuple_elems(pos, multiply_tuple_elems(dir, -1))
                    self.remove_dangling_from_coords(pos) 
                pos = anchor.coords
                for i in range(parent.num_after):
                    pos = add_tuple_elems(pos, dir)
                    self.remove_dangling_from_coords(pos)
            else:
                raise ValueError("Anchor without connected word")
        tiles = super().add_word(word, row, col, direction, reverse, is_junk)

        # Make all the new tiles dangling
        for tile in tiles:
            if not tile.is_junction():
                self.add_dangling(tile)
        return tiles
    
    def remove_dangling_from_coords(self, coords: tuple[int, int]):
        self.remove_dangling(self.get_tile(*coords))
    
    def add_dangling(self, tile: Tile) -> bool:
        if tile == None or tile.is_junction():
            return
        tile.set_dangling(True)
        self.dangling.append(tile)

    def remove_dangling(self, tile: Tile):
        if tile == None or not tile.is_dangling():
            return
        tile.set_dangling(False)
        self.dangling.remove(tile)
        
    def __str__(self):
        s = super().__str__()
        s += "\nWithout Dangling:"
        self.pop_dangling()
        s += "\n" + super().__str__()
        return s

    def remove_tile(self, row: int, col: int) -> Tile:
        tile = super().remove_tile(row, col)
        tile.set_dangling(False)
        return tile

    def pop_dangling(self) -> list[Tile]:
        for tile in self.dangling:
            self.remove_tile(*(tile.coords))
        return self.dangling