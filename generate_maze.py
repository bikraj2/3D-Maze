

import random
import numpy as np
import time
class Maze:
    def __init__(self, width: int, height: int):
        # Make dimensions odd
        width -= width % 2
        width += 1
        self.width = width
        height -= height % 2
        height += 1
        self.height = height

        # Fill maze with 1's (walls)
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        
        # Opening at top - start of maze
        self.maze[0][1] = 0

        # Random starting point
        start = [0,0]
        while start[0] % 2 == 0:
            start[0] = random.randint(1, height - 1)
        while start[1] % 2 == 0:
            start[1] = random.randint(1, width - 1)

        self.maze[start[0]][start[1]] = 0
        print(start)
        open_cells = [start]

        while open_cells:
            cell, neighbors = [], []
            
            # Add unnecessary element for elegance of code
            # Allows open_cells.pop() at beginning of do while loop
            open_cells.append([-1, -1])
            
            # Define current cell as last element in open_cells
            # and get neighbors, discarding "locked" cells
            while True:
                open_cells.pop()
                if not open_cells:
                    break
                cell = open_cells[-1]
                neighbors = self._get_neighbors(cell[0], cell[1])
                if neighbors:
                    break

            # If we're done, don't bother continuing
            if not open_cells:
                break

            # Choose random neighbor and add it to open_cells
            random.seed(int(time.time())) 
            choice = random.choice(neighbors)
            open_cells.append(choice)
            
            # Set neighbor to 0 (path, not wall)
            # Set connecting node between cell and choice to 0
            self.maze[choice[0]][choice[1]] = 0
            self.maze[(choice[0] + cell[0]) // 2][(choice[1] + cell[1]) // 2] = 0

        # Opening at bottom - end of maze
        self.maze[-1][-2] = 0
        self.maze[-2][-2] = 0

    def _get_neighbors(self, ic, jc):
        neighbors = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for d in directions:
            ni, nj = ic + d[0], jc + d[1]
            if 0 < ni < len(self.maze) and 0 < nj < len(self.maze[0]) and self.maze[ni][nj] == 1:
                neighbors.append([ni, nj])
        random.shuffle(neighbors)  # Shuffle to ensure random order
        return neighbors

if __name__ == "__main__":
    random.seed(int(time.time()))  # Seed the random number generator
    maze = Maze(10, 10)
    print(np.matrix(maze.maze))


