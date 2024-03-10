class Board:
    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int]] = {}
        # self.max_row = None
        # self.max_col = None
        # self.min_row = None
        # self.min_col = None
        
    def add_tile(self, tile: str, row: int, col: int) -> None:
        if (row, col) in self.tiles:
            raise ValueError(f'There is already a character at ({row}, {col})')
        
        adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        
        if all([coord not in self.tiles for coord in adjacent]):
            # No character tiles around it
            self.tiles[(row, col)] = tile
            return
        
        self.tiles[(row, col)] = tile
        