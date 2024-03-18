from .Tile import Tile


class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int]] = {}

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

    def add_tile(self, tile: str, row: int, col: int) -> None:
        tile = tile.upper()
        if len(tile) != 1:
            raise ValueError('Tile must be one character long')
        if (row, col) in self.tiles and self.tiles[(row, col)].char != tile:
            raise ValueError(f'There is already a tile at ({row}, {col})')
        print(f"Adding {tile} to {row},{col}")
        self.tiles[(row, col)] = Tile(board=self, row=row, col=col, char=tile)
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

    # Potentially should take in a Word object rather than a string for word and also store the
    # Word in each tile that composes the words so it is accessable later
    def add_word(self, word: str, row: int, col: int, direction: int, reverse=False) -> None:
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
