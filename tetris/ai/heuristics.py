import numpy as np


class Heuristics:
    """Heuristics class used because of project requirements."""
    size = 4

    @staticmethod
    def get(cells: list[list[int]]) -> tuple:
        """
        Calculates predetermined Heuristics for a given board state.
        :param cells: binary board state, 1 if there is a block and 0 if there isn't.
        :return: 1. aggregate height: the sum of all columns height
                 2. cleared lines: the number of full rows.
                 3. holes: the number of empty cells that have a block over them.
                 4. bumpiness: the sum of absolute difference in height between each column and
                               the column before it.
        """
        np_cells = np.array(cells)

        # a list of the height of each column
        col_heights = list()
        holes = 0
        for i in range(np_cells.shape[1]):
            col = np_cells[:, i]
            # indecies of blocks in the column
            indecies = np.where(col == 1)[0]
            length = len(col)
            # the height of the column is the length of the column minus the index of the
            # first block in it
            col_heights.append(length - indecies[0] if len(indecies) else 0)

            # adds the number of empty cells that have a block over them in the column
            holes += sum(1 for index in indecies if index != length - 1 and col[index + 1] == 0)

        agg_height = sum(col_heights)

        cleared_lines = sum(1 for row in np_cells if (row == 1).all())

        bumpiness = sum(
            abs(col_heights[i] - col_heights[i - 1]) for i in range(1, len(col_heights))
        )

        return agg_height, cleared_lines, holes, bumpiness
