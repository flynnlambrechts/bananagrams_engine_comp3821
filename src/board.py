from .tile import Tile
from .parent_word import ParentWord
from .constants import VERTICAL, HORIZONTAL


class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int], Tile] = {}
        self.anchors: list[Tile] = []

    def min_row(self) -> int:
        if len(self.tiles) == 0:
            return 0
        return min([row for row, _ in self.tiles])

    def max_row(self) -> int:
        if len(self.tiles) == 0:
            return 0
        return max([row for row, _ in self.tiles])

    def min_col(self) -> int:
        if len(self.tiles) == 0:
            return 0
        return min([col for _, col in self.tiles])

    def max_col(self) -> int:
        if len(self.tiles) == 0:
            return 0
        return max([col for _, col in self.tiles])

    def __str__(self) -> str:
        '''
        This allows us to use print(board)
        '''
        if not self.tiles:
            return ''

        col_delim = " "


        header = 4*" " + col_delim.join(
            map(lambda x: x[-1],
                map(str, range(self.min_col(), self.max_col() + 1))
                )
        ) + "\n"

        s = header + f"{self.min_row():>4}"

        cur_row = self.min_row()
        cur_col = self.min_col()
        for (row, col), value in sorted(
                self.tiles.items(), key=lambda item: (item[0][0], item[0][1])):
            while cur_row < row:
                cur_row += 1
                cur_col = self.min_col()
                s += f"\n{cur_row:>4}"
            skipped = 0
            while cur_col < col:
                cur_col += 1
                skipped += 1
            s += 2 * max(0, skipped) * col_delim + value.char + col_delim
            cur_col += 1

        return s

    def add_tile(self, tile: str, row: int, col: int, parent_word: str = '', pos: int = 0, direction: int = 0) -> Tile:
        '''
        Returns the Tile played as a Tile Object
        '''
        tile = tile.upper()
        if len(tile) != 1:
            raise ValueError('Tile must be one character long')
        if (row, col) in self.tiles and self.tiles[(row, col)].char != tile:
            raise ValueError(
                f'There is already a tile at ({row}, {col}) tried to add {tile}, the existing tile is {self.tiles[(row, col)]}')
        elif (row, col) in self.tiles:
            if direction == VERTICAL:
                self.tiles[(row,col)].vert_parent = ParentWord(parent_word, pos, direction)
            else:
                self.tiles[(row,col)].horo_parent = ParentWord(parent_word, pos, direction)
        else:
            tile = Tile(board=self, row=row, col=col, char=tile, parent_word=parent_word, pos=pos, direction=direction)
            self.tiles[(row, col)] = tile
            return tile
        # # Future nodes for caching sequences/words
        # adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        # if all([coord not in self.tiles for coord in adjacent]):
        #     # No character tiles around it
        #     self.tiles[(row, col)] = tile
        #     return

        # self.tiles[(row, col)] = tile

    def remove_tile(self, row: int, col: int) -> str:
        '''Note that this won't change the ParentWord info of surrounding tiles'''
        if (row, col) not in self.tiles:
            raise ValueError(f'There is no tile at ({row}, {col})')

        return self.tiles.pop((row, col))

    def remove_anchor(self, anchor: Tile):
        self.anchors = list(filter(lambda a: a != anchor, self.anchors))

    def add_word(self, word: str, row: int, col: int, direction: int, reverse=False) -> list[Tile]:
        '''
        Potentially should take in a Word object rather than a string for word
        and also store the Word in each tile that composes the words so it is
        accessable later.
        Returns the last tile played [EDIT] Now Returns a list of all the tiles played
        '''
        dr = int(direction == VERTICAL)
        dc = int(direction == HORIZONTAL)
        tile_str = word
        if (reverse):
            dr *= -1
            dc *= -1
            tile_str = word[::-1]

        tiles = []
        for i, c in enumerate(tile_str):
            pos = i
            if reverse:
                pos = len(word) - i - 1
            new_tile = self.add_tile(c, row + i * dr, col + i * dc, word, pos, direction)
            if new_tile is not None:
                tiles.append(new_tile)
        self.anchors.extend(tiles)
        return tiles
