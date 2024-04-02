def send_probes(coords: tuple[int, int], board):
    def _get_probe_diags(dir: tuple):
        x = dir[0]
        y = dir[1]

        if x == 0:
            return [(1, 0), (-1, 0)]
        else:
            return [(0, 1), (0, -1)]

    def _probe_on_board(board, row: int, col: int, tile_coords = (0,0)) -> bool:
        '''
        note that self.board.min_row() etc don't take into account the tile
        just placed hence a function for if the probe is on the board is
        worthwhile
        '''

        min_r = min(board.min_row(), tile_coords[0])
        max_r = max(board.max_row(), tile_coords[0])
        min_c = min(board.min_col(), tile_coords[1])
        max_c = max(board.max_col(), tile_coords[1])

        return (min_r <= row <= max_r) and (min_c <= col <= max_c)


    tiles = board.tiles.keys()
    probe_hits = []
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for i in range(4):
        count = 0
        row = coords[0]
        col = coords[1]
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
            if not _probe_on_board(board, row, col, coords):
                break
            for j in range(3):
                checked_tile = (
                    row + dirs[(i + 1 - j) % 4][0],
                    col + dirs[(i + 1 - j) % 4][1])
                if checked_tile in tiles:
                    hit = (checked_tile, i, i - 2, count)
                    probe_hits.append(hit)
                    
                    if j == 1:
                        diags = _get_probe_diags(dirs[i])
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