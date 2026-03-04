class CubeGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # grid[0] = bottom row, grid[height-1] = top row
        self.grid = [[0] * width for _ in range(height)]

    def drop(self, cubes):
        """Drop a list of column indices simultaneously, then clear full rows."""
        for col in cubes:
            pass  # TODO: place cube in correct row

        # TODO: clear full rows and shift remaining rows down

    def getGrid(self):
        """Returns the grid state. Row 0 is the bottom."""
        return self.grid

    def getHeight(self, col):
        """Returns the current stack height in a given column."""
        pass  # TODO: count filled cells from bottom up


if __name__ == "__main__":
    grid = CubeGrid(4, 5)
    grid.drop([0, 1, 2, 3])  # fills bottom row → should clear
    grid.drop([0, 0, 1])  # col 0 stacks 2, col 1 gets 1
    print(grid.getGrid())
