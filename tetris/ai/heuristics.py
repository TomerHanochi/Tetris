import numpy as np


class Heuristics:
    size = 6

    @staticmethod
    def get(cells: list[list[str or None]]) -> tuple:
        np_cells = np.array([
            [0 if cell is None else 1 for cell in row] for row in cells
        ])

        peaks = []
        holes = 0
        cols_with_holes = 0
        pits = 0
        for i in range(np_cells.shape[1]):
            col = np_cells[:, i]
            indecies = np.where(col == 1)[0]
            height = len(col)
            if len(indecies):
                peaks.append(height - indecies[0])
            else:
                peaks.append(0)
                pits += 1

            col_holes = sum(1 for index in indecies if index != height - 1 and col[index + 1] == 0)
            holes += col_holes

            if col_holes:
                cols_with_holes += 1

        agg_height = sum(peaks)

        cleared_lines = sum(1 for row in np_cells if (row == 1).all())

        bumpiness = sum(peaks[i] - peaks[i - 1] for i in range(1, len(peaks)))

        return agg_height, cleared_lines, holes, bumpiness, cols_with_holes, pits
