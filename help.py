import time
import os
import shutil


def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80 


def center_text(text: str) -> str:
    term_width = get_terminal_width()
    padding = max((term_width - len(text)) // 2, 0)
    return " " * padding + text

def loading(tmie: float = 0, file_name : str ="ami-ascii.txt") -> None:
    data = None
    try:
        tmie = float(tmie)
    except ValueError as e:
        tmie = 0
    
    try:
        with open(file_name, 'r') as file:
            data = [ line.rstrip('\n')  for line in file]
    except Exception as e:
        print(e)
    if not data:
        print()
    else:
        print('\n\n\n\n\n\n')
        print("\033[38;2;0;255;0m")  # Green
        for line in data:
            print(center_text(line))
            time.sleep(tmie)
        print("\033[0m")
    time.sleep(tmie)
        

def decode_cell(value :str) -> dict:
    """Decode hex cell value into wall directions."""
    try:
        int_value =  int(value, 16)
        bits = format(int_value, "04b")
        
        return {
            'N' : bits[3] == '1',
            'E' : bits[2] == '1',
            'S' : bits[1] == '1',
            'W' : bits[0] == '1',
        }
    except Exception as e:
        print(e) 


COLORS = {
    "wall": {
        1: "\033[91m",  # Bright red
        2: "\033[92m",  # Bright green
        3: "\033[95m"   # Bright magenta
    },
    "space": {
        1: "\033[108m",  # Bright white space
        2: "\033[107m",
        3: "\033[107m"
    },
    "solve": {
        1: "\033[44m",  # Blue
        2: "\033[43m",  # Yellow
        3: "\033[42m"   # Green
    },
    "reset": "\033[0m"
}

WALL = {
    0: {"corner_tl": "╔", "corner_tr": "━━━╗", "corner_bl": "╚", "corner_br": "╝", "h": "━━━", "v": "┃", "h+1": "━━━━"},
    1: {"corner_tl": "+", "corner_tr": "===+", "corner_bl": "+", "corner_br": "+", "h": "===", "v": "║", "h+1": "===="},
    2: {"corner_tl": "╔", "corner_tr": "━━━╗", "corner_bl": "╚", "corner_br": "╝", "h": "━━━", "v": "┃", "h+1": "━━━━" },
    3: {"corner_tl": "╔", "corner_tr": "━━━╗", "corner_bl": "╚", "corner_br": "╝", "h": "━━━", "v": "┃", "h+1": "━━━━"}
}

COLOR_MENU = {
    0:{ 
        "wall_color": "\033[37m",   # White background for walls
        "space_color": "\033[47m",  # Black background for empty space
        "solve_color": "\033[67m",  # Blue background for path / arrows
    },
    1: {
        "wall_color": COLORS["wall"][1],
        "space_color": COLORS["space"][1],
        "solve_color": COLORS["solve"][1],
    },
    2: {
        "wall_color": COLORS["wall"][2],
        "space_color": COLORS["space"][2],
        "solve_color": COLORS["solve"][2],
    },
    3: {
        "wall_color": COLORS["wall"][3],
        "space_color": COLORS["space"][3],
        "solve_color": COLORS["solve"][3],
    }
}
FORTY_TWO_COLORS = [
    "\033[40m",
    "\033[48;5;196m",  # Intense red
    "\033[48;5;202m",  # Bright orange
    "\033[48;5;46m",   # Neon green
    "\033[48;5;51m",   # Bright cyan
    "\033[48;5;226m",  # Electric yellow
    "\033[48;5;201m",  # Hot pink
]

ARROWS = {
    "N": "⟰",
    "S":"⟱",
    "E": "⭆",
    "W": "⭅",
}



if __name__ == "__main__":
    loading()









# # Draw top border of maze
        # print(center_text(wall_color+ "┏" + "━━━━" * (width - 1) + "━━━┓"+ COLORS["reset"]))

        # for y in range(height):
        #     row_top = wall_color + "┃" +  COLORS["reset"]
        #     row_bottom = f'{wall_color + ("┣" if y < height - 1 else "┗") + COLORS["reset"]}'

        #     for x in range(width):
        #         cell_walls = decode_cell(maze[y][x])
                
        #         # 1. Cell Content
        #         if (y, x) == start:
        #             cell_char = solve_color + " S " + COLORS["reset"]
        #         elif (y, x) == end:
        #             cell_char = solve_color + " X " + COLORS["reset"]
        #         elif show and (y, x) in path_solve:
        #             cell_char = solve_color + " * " + COLORS["reset"]
        #         else:
        #             cell_char = space_color + "   " + COLORS["reset"]

        #         # 2. East Wall (Vertical)
        #         # If it's the last column, we always draw a border
        #         row_top += cell_char + (wall_color + "┃" + COLORS["reset"] if cell_walls['E'] or x == width - 1 else " ")

        #         # 3. South Wall (Horizontal)
        #         # If it's the last row, we always draw a border
        #         row_bottom += wall_color + ("━━━" if cell_walls['S'] or y == height - 1 else "   ") + COLORS["reset"]

        #         # 4. The Junction (The "???" logic)
        #         if x < width - 1:
        #             if y < height - 1:
        #                 # Inside the maze: Use a cross-junction
        #                 row_bottom += "┃" 
        #             else:
        #                 # Bottom edge: Use a T-junction pointing up
        #                 row_bottom += "━"
        #         else:
        #             if y < height - 1:
        #                 # Right edge: Use a T-junction pointing left
        #                 row_bottom += "┫"
        #             else:
        #                 # Final bottom-right corner
        #                 row_bottom += "┛"
            
        #     print(center_text(row_top))
        #     print(center_text(row_bottom))
