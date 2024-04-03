from .tile import Tile
from parent_word import ParentWord
from constants import VERTICAL, HORIZONTAL


class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int], Tile] = {}
        self.anchors: list[Tile] = []
        self.junk_on_board = False
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

    def add_tile(self, tile: str, row: int, col: int, parent_word: str = '', pos: int = 0, direction: int = 0, is_junk = False) -> Tile:
        '''
        Returns the Tile played as a Tile Object
        '''
        if is_junk: self.junk_on_board = True
            
        tile = tile.upper()
        if len(tile) != 1:
            raise ValueError('Tile must be one character long')
        if (row, col) in self.tiles and self.tiles[(row, col)].char != tile:
            raise ValueError(
                f'There is already a tile at ({row}, {col}) tried to add {tile}, the existing tile is {self.tiles[(row, col)]}')
        elif (row, col) in self.tiles:
            if direction == VERTICAL:
                self.tiles[(row, col)].vert_parent = ParentWord(
                    parent_word, pos, direction)
            else:
                self.tiles[(row, col)].horo_parent = ParentWord(
                    parent_word, pos, direction)
        else:
            tile = Tile(board=self, row=row, col=col, char=tile, parent_word=parent_word, pos=pos, direction=direction, is_junk=is_junk)
            self.tiles[(row, col)] = tile
            return tile
        # # Future nodes for caching sequences/words
        # adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        # if all([coord not in self.tiles for coord in adjacent]):
        #     # No character tiles around it
        #     self.tiles[(row, col)] = tile
        #     return

        # self.tiles[(row, col)] = tile

    def remove_tile(self, row: int, col: int) -> Tile:
        '''Note that this won't change the ParentWord info of surrounding tiles'''
        if (row, col) not in self.tiles:
            raise ValueError(f'There is no tile at ({row}, {col})')

        removed_tile = self.tiles.pop((row, col))
        probe_hits_list = removed_tile.send_probes(self.tiles)
        for probe in probe_hits_list:
            tile = self.tiles[probe[0]]
            tile.lims = tile._update_lims()
        return  removed_tile

    def remove_anchor(self, anchor: Tile):
        self.anchors = list(filter(lambda a: a != anchor, self.anchors))

    def add_word(self, word: str, row: int, col: int, direction: int, reverse=False, is_junk = False) -> list[Tile]:
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
            new_tile = self.add_tile(c, row + i * dr, col + i * dc, word, pos, direction, is_junk)
            if new_tile is not None:
                tiles.append(new_tile)
        self.anchors.extend(tiles)
        return tiles

    def remove_word(self, tile_in_word: Tile, direction: int) -> list[Tile]:
        removed_tiles = []
        coord_to_move_along = 0
        if direction == VERTICAL:
            if tile_in_word.vert_parent == None:
                # print(f"tile: {tile_in_word}")
                raise ValueError("No vertical word to remove")
            parent_word = tile_in_word.vert_parent

        else:
            if tile_in_word.horo_parent == None:
                # print(f"tile: {tile_in_word}")
                raise ValueError("No horizontal word to remove")
            parent_word = tile_in_word.horo_parent
            coord_to_move_along = 1
        
        coords_list = [tile_in_word.coords]
        for i in range(parent_word.num_before):
            if coord_to_move_along == 0:
                coords_list.append((tile_in_word.coords[0] - i - 1, tile_in_word.coords[1]))
            else:
                coords_list.append((tile_in_word.coords[0], tile_in_word.coords[1] - i - 1))
        for i in range(parent_word.num_after):
            if coord_to_move_along == 0:
                coords_list.append((tile_in_word.coords[0] + i + 1, tile_in_word.coords[1]))
            else:
                coords_list.append((tile_in_word.coords[0], tile_in_word.coords[1] + i + 1))

        for coords in coords_list:
            tile_to_remove = self.tiles[coords]
            if tile_to_remove.horo_parent == None or tile_to_remove.vert_parent == None:
                removed_tiles.append(self.remove_tile(coords[0], coords[1])) 
            else:
                if direction == VERTICAL:
                    tile_to_remove.vert_parent = None
                else:
                    tile_to_remove.horo_parent = None

        # for i in range(parent_word.num_before):
        #     coords = tile_in_word.coords
        #     coords[coord_to_move_along] -= (i + 1)
        #     tile_to_remove = self.tiles[coords]
        #     if tile_to_remove.horo_parent == None or tile_to_remove.vert_parent == None:
        #         removed_tiles.append(self.remove_tile(coords[0], coords[1])) 
        #     else:
        #         if direction == VERTICAL:
        #             tile_to_remove.vert_parent = None
        #         else:
        #             tile_to_remove.horo_parent = None
        # for i in range(parent_word.num_after):
        #     coords = tile_in_word.coords
        #     coords[coord_to_move_along] += (i + 1)
        #     tile_to_remove = self.tiles[coords]
        #     if tile_to_remove.horo_parent == None or tile_to_remove.vert_parent == None:
        #         removed_tiles.append(self.remove_tile(coords[0], coords[1])) 
        #     else:
        #         if direction == VERTICAL:
        #             tile_to_remove.vert_parent = None
        #         else:
        #             tile_to_remove.horo_parent = None
        return removed_tiles

    def remove_junk_tiles(self, tiles: list[Tile]) -> list[Tile]:
        removed_tiles = []
        for tile in tiles:
            if tile.vert_parent == None:
                direction = HORIZONTAL
            else: 
                direction = VERTICAL

            if tile not in removed_tiles:
                removed_tiles.extend(self.remove_word(tile, direction))
        # print("removed tiles:")
        # print(removed_tiles)
        return removed_tiles