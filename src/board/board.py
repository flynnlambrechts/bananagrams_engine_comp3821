from .tile import Tile
from parent_word import ParentWord
from constants import VERTICAL, HORIZONTAL, bcolors
from pprint import pprint


class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int], Tile] = {}
        self.anchors: list[Tile] = []
        self.junk_on_board = False
        self.words = []

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
        """
        This allows us to use print(board)
        """
        # for word in self.words:
        #     print(str(word))

        if not self.tiles:
            return ""

        col_delim = " "

        header = (
            4 * " "
            + col_delim.join(
                map(
                    lambda x: x[-1], map(str,
                                         range(self.min_col(), self.max_col() + 1))
                )
            )
            + "\n"
        )

        s = header + f"{self.min_row():>4}"

        cur_row = self.min_row()
        cur_col = self.min_col()
        for (row, col), tile in sorted(
            self.tiles.items(), key=lambda item: (item[0][0], item[0][1])
        ):
            while cur_row < row:
                cur_row += 1
                cur_col = self.min_col()
                s += f"\n{cur_row:>4}"
            skipped = 0
            while cur_col < col:
                cur_col += 1
                skipped += 1
            tile_text = str(tile)
            s += 2 * max(0, skipped) * col_delim + tile_text + col_delim

            cur_col += 1

        return s

    def add_tile(self, tile: str, row: int, col: int, is_junk=False) -> Tile:
        '''
        Returns the Tile played as a Tile Object
        '''
        if is_junk:
            self.junk_on_board = True

        tile = tile.upper()
        if len(tile) != 1:
            raise ValueError("Tile must be one character long")
        if (row, col) in self.tiles and self.tiles[(row, col)].char != tile:
            error_str = f"There is already a tile at ({row}, "
            error_str += "{col}) tried to add {tile}, the existing tile is {self.tiles[(row, col)]}"
            raise ValueError(error_str)
        elif not (row, col) in self.tiles:
            tile = Tile(board=self, row=row, col=col,
                        char=tile, is_junk=is_junk)
            self.tiles[(row, col)] = tile
            return tile
        else:
            return None

    def remove_tile(self, row: int, col: int) -> Tile:
        """Note that this won't change the ParentWord info of surrounding tiles"""
        if (row, col) not in self.tiles:
            raise ValueError(
                f"There is no tile at ({row}, {col})\n{str(self)}")

        removed_tile = self.tiles.pop((row, col))
        self.remove_anchor(removed_tile)
        probe_hits_list = removed_tile.send_probes(self.tiles)
        for probe in probe_hits_list:
            tile = self.tiles[probe[0]]
            tile.lims = tile._update_lims()
        return removed_tile

    def remove_anchor(self, anchor: Tile):
        self.anchors = list(filter(lambda a: a != anchor, self.anchors))

    def add_word(self, word: str, row: int, col: int, direction: int, reverse=False, is_junk=False) -> list[Tile]:
        '''
        Potentially should take in a Word object rather than a string for word
        and also store the Word in each tile that composes the words so it is
        accessable later.
        Returns a list of all the tiles played
        '''

        dr = int(direction == VERTICAL)
        dc = int(direction == HORIZONTAL)
        tile_str = word
        if reverse:
            dr *= -1
            dc *= -1
            tile_str = word[::-1]

        word = ParentWord(tile_str, direction)
        self.words.append(word)
        new_tiles = []
        for i, c in enumerate(tile_str):
            pos = i
            if reverse:
                pos = len(word) - i - 1
            new_tile = self.add_tile(
                c, row + i * dr, col + i * dc, is_junk=is_junk)
            if new_tile is not None:
                word.add_tile(new_tile, pos)
                new_tiles.append(new_tile)
            else:
                existing_tile = self.get_tile(row + i * dr, col + i * dc)
                print(repr(existing_tile), "already exists updated parents")
                print(existing_tile)
                word.add_tile(existing_tile, pos)

        self.anchors.extend(word.get_tiles())
        print("Played", word.get_tiles())
        print("New Tiles", new_tiles)
        return new_tiles

    def has_tile(self, row: int, col: int) -> bool:
        return (row, col) in self.tiles

    def get_tile(self, row: int, col: int) -> Tile | None:
        if not self.has_tile(row, col):
            return None
        return self.tiles[(row, col)]

    def remove_word(self, tile_in_word: Tile, direction: int) -> list[Tile]:
        print("attempted remove")
        if parent := tile_in_word.get_parent(direction):
            print(f"removing {parent}")
            self.words.remove(parent)
            if parent in self.words:
                print("parent still in words")
            return parent.remove_from_board()
        else:
            raise ValueError(f"No {direction} word to remove")

    def remove_junk_tiles(self, tiles: list[Tile]) -> list[Tile]:
        junk_words = []
        for tile in self.tiles.values():
            if tile.is_junk and not tile.is_junction():
                # direction = HORIZONTAL if tile.has_parent(HORIZONTAL) else VERTICAL
                if not tile.has_parent(VERTICAL):
                    
                    direction = HORIZONTAL
                else:
                    direction = VERTICAL
                parent = tile.get_parent(direction)
                if parent not in junk_words:
                    junk_words.append(parent)
                    # removed_tiles.extend(self.remove_word(tile, direction))
        removed_tiles = []
        for word in junk_words:
            removed_tiles.extend(word.remove_from_board())
            self.words.remove(word)

        return removed_tiles

    def remove_dangling(self) -> list[Tile]:
        dangling_words = []
        for word in self.words:
            if word.is_dangling():
                dangling_words.append(word)
        self.words = list(
            filter(lambda word: not word.is_dangling(), self.words))
        dangling = []
        for word in dangling_words:
            dangling.extend(word.remove_from_board())
        return dangling
