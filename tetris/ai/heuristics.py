import numpy as np


class Heuristics:
    size = 4

    @staticmethod
    def get(cells: list[list[int]]) -> tuple:
        np_cells = np.array(cells)

        peaks = list()
        holes = 0
        for i in range(np_cells.shape[1]):
            col = np_cells[:, i]
            indecies = np.where(col == 1)[0]
            height = len(col)
            peaks.append(height - indecies[0] if len(indecies) else 0)

            col_holes = sum(1 for index in indecies if index != height - 1 and col[index + 1] == 0)
            holes += col_holes

        agg_height = sum(peaks)

        cleared_lines = sum(1 for row in np_cells if (row == 1).all())

        bumpiness = sum(abs(peaks[i] - peaks[i - 1]) for i in range(1, len(peaks)))

        return agg_height, cleared_lines, holes, bumpiness
