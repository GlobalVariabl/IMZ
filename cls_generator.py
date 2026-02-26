import random
from collections import deque
import sys
sys.setrecursionlimit(3000)  # set new limit
class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple, exit_: tuple,
                 output_file: str, perfect: bool):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.output_file = output_file
        self.perfect = perfect
        self.maze = [[15 for _ in range(width)] for _ in range(height)]

    N, E, S, W = 0, 1, 2, 3

    directions = {
        N: (-1, 0),
        E: (0, 1),
        S: (1, 0),
        W: (0, -1)
    }

    oposite = {N: S, E: W, S: N, W: E}

    def allocate_irea_for_print(self, visited: list[list]) -> bool:
        start_x = self.height - 5
        start_y = self.width - 7
        if start_x < 2 or start_y < 2:
            return False
        start_x //= 2
        start_y //= 2

        # alocate 4 in 7 blocks

        visited[start_x][start_y] = True
        visited[start_x + 1][start_y] = True
        visited[start_x + 2][start_y] = True

        visited[start_x + 2][start_y + 1] = True
        visited[start_x + 2][start_y + 2] = True
        visited[start_x + 3][start_y + 2] = True
        visited[start_x + 4][start_y + 2] = True

        # alocate 2 in 11 blocks

        visited[start_x][start_y + 4] = True
        visited[start_x][start_y + 5] = True
        visited[start_x][start_y + 6] = True
        visited[start_x + 1][start_y + 6] = True
        visited[start_x + 2][start_y + 4] = True
        visited[start_x + 2][start_y + 5] = True
        visited[start_x + 2][start_y + 6] = True
        visited[start_x + 3][start_y + 4] = True
        visited[start_x + 4][start_y + 4] = True
        visited[start_x + 4][start_y + 5] = True
        visited[start_x + 4][start_y + 6] = True
        return True

    def generate_maze(self) -> None:
        visited = [[False for _ in
                    range(self.width)] for _ in range(self.height)]
        if not self.allocate_irea_for_print(visited):
            # message will be hear
            pass

        def creat_path(x: int, y: int):

            visited[x][y] = True
            directs = [d for d in self.directions.keys()]
            random.shuffle(directs)

            for direct in directs:

                next_x = (x + self.directions[direct][0])
                next_y = (y + self.directions[direct][1])

                if (0 <= next_x < self.height) and (0 <= next_y < self.width)\
                        and not visited[next_x][next_y]:

                    self.maze[x][y] &= ~(1 << direct)
                    self.maze[next_x][next_y] &= ~(1 << self.oposite[direct])
                    creat_path(next_x, next_y)

        creat_path(self.entry[0], self.entry[1])

    def re_import_with_new_maze(self):
        self.maze = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.generate_maze()
        self.import_maze()

    def solve_the_maze(self) -> str:
        visited = [[False for _
                    in range(self.width)] for _ in range(self.height)]

        queue = deque()
        queue.append((self.entry[0], self.entry[1], ""))
        visited[self.entry[0]][self.entry[1]] = True

        while (queue):
            x, y, path = queue.popleft()
            if (x, y) == self.exit_:
                return path
            for d, (d_x, d_y) in self.directions.items():
                next_x, next_y = x + d_x, y + d_y
                if 0 <= next_x < self.height and 0 <= next_y < self.width:
                    if (not self.maze[x][y] & (1 << d)) and\
                       (not visited[next_x][next_y]):

                        visited[next_x][next_y] = True
                        queue.append((next_x, next_y, path + "NESW"[d]))
        return ""

    def import_maze(self) -> None:
        solution = self.solve_the_maze()
        with open(self.output_file, "w") as f:
            for row in self.maze:
                line = "".join(f"{block:X}" for block in row) + "\n"
                f.write(line)
            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit_[0]},{self.exit_[1]}\n")
            f.write(solution + "\n")