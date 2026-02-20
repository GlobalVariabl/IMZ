# import random
# from collections import deque
# import time
# import os

# def clear_screen():
#     # Clears the terminal for a smooth animation frame update
#     os.system('cls' if os.name == 'nt' else 'clear')

# def create_maze_with_exact_pattern(width, height):
#     maze = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(width)] for _ in range(height)]
#     visited = [[False]*width for _ in range(height)]
    
#     # --- 1. Your Exact 42 Pattern Mask ---
#     pattern_str = [
#         ".......",
#         "X...XXX",
#         "X.....X",
#         "XXX.XXX",
#         "..X.X..",
#         "..X.XXX"
#     ]
    
#     # Center the pattern in the maze
#     mid_x = (width - len(pattern_str[0])) // 2
#     mid_y = (height - len(pattern_str)) // 2
    
#     obstacle_cells = set()
#     for r, row in enumerate(pattern_str):
#         for c, char in enumerate(row):
#             if char == 'X':
#                 ox, oy = mid_x + c, mid_y + r
#                 if 0 <= ox < width and 0 <= oy < height:
#                     obstacle_cells.add((ox, oy))
#                     visited[oy][ox] = True 

#     # --- 2. Maze Generation Logic ---
#     def carve(x, y):
#         visited[y][x] = True
#         directions = [('N', 0, -1), ('S', 0, 1), ('E', 1, 0), ('W', -1, 0)]
#         random.shuffle(directions)
#         for direction, dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
#                 maze[y][x][direction] = False
#                 maze[ny][nx][{'N':'S','S':'N','E':'W','W':'E'}[direction]] = False
#                 carve(nx, ny)

#     carve(0, 0)
#     return maze, obstacle_cells

# def print_live_maze(maze, obstacles, visited_search, current, path=None):
#     width, height = len(maze[0]), len(maze)
#     # Using box-drawing characters for a cleaner look
#     print("┏" + "━━━┳" * (width - 1) + "━━━┓")
    
#     for y in range(height):
#         row_top, row_bottom = "┃", "┣"
#         for x in range(width):
#             # Cell Content
#             if (x, y) in obstacles:
#                 cell = "███" # White block for pattern
#             elif path and (x, y) in path:
#                 cell = " * " # Final path
#             elif (x, y) == current:
#                 cell = " @ " # Search head
#             elif (x, y) in visited_search:
#                 cell = " . " # Scanned area
#             else:
#                 cell = "   "
            
#             row_top += cell + ("┃" if maze[y][x]['E'] else " ")
            
#             if y < height - 1:
#                 row_bottom += ("━━━" if maze[y][x]['S'] else "   ") + ("╋" if x < width - 1 else "┫")
        
#         print(row_top)
#         if y < height - 1:
#             print(row_bottom)
            
#     print("┗" + "━━━┻" * (width - 1) + "━━━┛")

# def solve_and_animate(maze, start, end, obstacles, delay =0):
#     width, height = len(maze[0]), len(maze)
#     queue = deque([start])
#     came_from = {start: None}
#     visited_search = {start}

#     while queue:
#         curr = queue.popleft()
        
#         clear_screen()
#         print(f"Traversing Graph... Current Step: {curr} | Interval: {delay}s")
#         print_live_maze(maze, obstacles, visited_search, curr)
#         time.sleep(delay)

#         if curr == end:
#             path = []
#             while curr:
#                 path.append(curr)
#                 curr = came_from[curr]
#             clear_screen()
#             print("SUCCESS: Exit Reached!")
#             print_live_maze(maze, obstacles, visited_search, None, path=path)
#             return

#         x, y = curr
#         for d, (dx, dy) in {'N':(0,-1), 'S':(0,1), 'E':(1,0), 'W':(-1,0)}.items():
#             if not maze[y][x][d]:
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < width and 0 <= ny < height:
#                     if (nx, ny) not in visited_search and (nx, ny) not in obstacles:
#                         visited_search.add((nx, ny))
#                         came_from[(nx, ny)] = curr
#                         queue.append((nx, ny))

# if __name__ == "__main__":
#     # Settings for your 15x14 maze
#     W, H = 15, 15
#     START, END = (0, 0), (W-1, H-1)
    
#     maze_data, obs = create_maze_with_exact_pattern(W, H)
    
#     try:
#         solve_and_animate(maze_data, START, END, obs, delay=0.1)
#     except KeyboardInterrupt:
#         print("\nVisualization stopped.")



import random
from collections import deque

# --------------------------------------------------
# MAZE GENERATION
# --------------------------------------------------

def create_maze(width, height):
    maze = [[{'N': True, 'S': True, 'E': True, 'W': True}
             for _ in range(width)] for _ in range(height)]
    visited = [[False]*width for _ in range(height)]

    def carve(x, y):
        visited[y][x] = True
        directions = [('N', 0, -1), ('S', 0, 1),
                      ('E', 1, 0), ('W', -1, 0)]
        random.shuffle(directions)

        for d, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                maze[y][x][d] = False
                opposite = {'N':'S','S':'N','E':'W','W':'E'}
                maze[ny][nx][opposite[d]] = False
                carve(nx, ny)

    carve(0, 0)
    return maze


# --------------------------------------------------
# ENCODING (N E S W, 1 = closed, 0 = open)
# --------------------------------------------------

def encode_cell(cell):
    bits = [
        '1' if cell['N'] else '0',
        '1' if cell['E'] else '0',
        '1' if cell['S'] else '0',
        '1' if cell['W'] else '0'
    ]
    binary_str = ''.join(bits)
    return format(int(binary_str, 2), 'X')  # single hex digit


# --------------------------------------------------
# SOLVER (BFS shortest path)
# --------------------------------------------------

def solve_maze(maze, start, end):
    width, height = len(maze[0]), len(maze)
    queue = deque([start])
    came_from = {start: None}

    directions = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            break

        for d, (dx, dy) in directions.items():
            if not maze[y][x][d]:  # wall open
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in came_from:
                        came_from[(nx, ny)] = (x, y, d)
                        queue.append((nx, ny))

    # Reconstruct path
    path_moves = []
    curr = end
    while curr != start:
        prev = came_from[curr]
        if prev is None:
            return ""  # no path
        px, py, move = prev
        path_moves.append(move)
        curr = (px, py)

    path_moves.reverse()
    return ''.join(path_moves)


# --------------------------------------------------
# WRITE OUTPUT FILE
# --------------------------------------------------

def write_output(filename, maze, start, end, path):
    height = len(maze)
    width = len(maze[0])

    with open(filename, 'w') as f:

        # Maze rows
        for y in range(height):
            row = ''.join(encode_cell(maze[y][x]) for x in range(width))
            f.write(row + "\n")

        # Empty line
        f.write("\n")

        # Entry
        f.write(f"{start[0]} {start[1]}\n")

        # Exit
        f.write(f"{end[0]} {end[1]}\n")

        # Path
        f.write(path + "\n")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    W, H = 15, 15
    START = (0, 0)
    END = (W-1, H-1)

    maze = create_maze(W, H)
    shortest_path = solve_maze(maze, START, END)

    write_output("output.txt", maze, START, END, shortest_path)

    print("Maze exported to output.txt")