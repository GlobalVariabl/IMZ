
def xpeort_output(output_file: str) -> dict:
    try:
        with open(output_file, 'r') as file:
            lines = [line.rstrip("\n") for line in file]
            # print(lines)

        end_maze = lines.index("")
        maze = lines[:end_maze]
        path = [lines[-1]]
        start = [int(x) for x in lines[end_maze+1].split(" ")]# .split(" ") to .split(",")
        end = [int(x) for x in lines[end_maze+2].split(" ")]# .split(" ") to .split(",")
        # print("\n",maze,"\n\n", path, "\n\n", start, "\n\n", end)

        return {
            "maze": maze,
            "path": path,
            "start": start,
            "end": end
        }
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)


def decode_cell(value):
    try:
        value_int = int(value, 16)
        bits = format(value_int, "04b")  # 4 bits: N E S W
        # print(bits)
        return {
            "N": bits[0] == "1",
            "E": bits[1] == "1",
            "S": bits[2] == "1",
            "W": bits[3] == "1",
        }
    except Exception as e:
        print(e)


def print_live_maze(data: dict) -> int:
    try:
        maze = data["maze"]
        entry = data["start"]
        exit_ = data["end"]
        path_cells = set()  # could fill with path coords later

        height = len(maze)
        width = len(maze[0])

        # Draw top border
        word = "A-Maze-ing"

        # Each cell is 3 characters wide in your maze display
        cell_width = 3
        total_width = width * cell_width + (width + 1)
        padding = (total_width - len(word)) // 2
        print(" " * padding + word)

        # Draw top border of maze
        print("┏" + "━━━┳" * (width - 1) + "━━━┓")

        for y in range(height):
            row_top = "┃"
            row_bottom = "┣"

            for x in range(width):
                cell_walls = decode_cell(maze[y][x])

                if (x, y) == entry:
                    cell_char = " E "
                elif (x, y) == exit_:
                    cell_char = " X "
                elif (x, y) in path_cells:
                    cell_char = " * "
                else:
                    cell_char = "   "

                # East wall
                row_top += cell_char + ("┃" if cell_walls["E"] else " ")

                # South wall
                row_bottom += ("━━━" if cell_walls["S"] else "   ")
                row_bottom += "╋" if x < width - 1 else "┫"

            print(row_top)
            if y < height - 1:
                print(row_bottom)

        # Draw bottom border
        print("┗" + "━━━┻" * (width - 1) + "━━━┛")
        print(f"\n=== {word} ===")
        print("1. Re-generato a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quiz")
        choice = int(input("Choice? (1-4):"))
        if choice > 4 or choice < 1:
            print(f"you choice {choice} not in list orde")
            exit(1)
        

    except Exception as e:
        print(e)


if __name__ == "__main__":
    display = xpeort_output("output.txt")
    print_live_maze(display)