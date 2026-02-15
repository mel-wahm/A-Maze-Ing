#!/usr/bin/python3
import random
import time
import sys
import os

print("\033[1;1H", end="")
os.system('clear')
sys.setrecursionlimit(10**6)
SEED = 42

# random.seed(42)

try:
    width = int(input("Enter Width of the Maze: "))
    height = int(input("Enter Height of the Maze: "))
    if width < 9 or height < 7:
        print("The given numbers are to small to be able to print 42")
        exit()
    # if width > 35 or height > 35:
    #     print("Numbers are too high, please choose lower values")
    #     exit()
except Exception:
    print("Only numbers are allowed.")
    exit()

exit_ = (height - 1, width - 1)
entry_y = 0
entry_x = 0
entry_ = (entry_y, entry_x)


class Cell:
    def __init__(self):
        self.walls = 15
        self.is_visited = False


maze = [
    [Cell() for _ in range(width)] for _ in range(height)
]
def get_forty_two_coords(width, height):

    coords = [
        maze[height // 2][(width // 2 + 1)],
        maze[height // 2][(width // 2 + 2)],
        maze[height // 2][(width // 2 + 3)],
        maze[height // 2 - 1][(width // 2 + 3)],
        maze[height // 2 - 2][(width // 2 + 3)],
        maze[height // 2 - 2][(width // 2 + 2)],
        maze[height // 2 - 2][(width // 2 + 1)],
        maze[height // 2 + 1][(width // 2 + 1)],
        maze[height // 2 + 2][(width // 2 + 1)],
        maze[height // 2 + 2][(width // 2 + 2)],
        maze[height // 2 + 2][(width // 2 + 3)],

        maze[height // 2][(width // 2 - 1)],
        maze[(height // 2) + 1][(width // 2 - 1)],
        maze[(height // 2) + 2][(width // 2 - 1)],
        maze[height // 2][width // 2 - 2],
        maze[height // 2][width // 2 - 3],
        maze[(height // 2) - 1][width // 2 - 3],
        maze[(height // 2) - 2][width // 2 - 3],
        maze[height // 2 - 1][(width // 2 - 1)],
        maze[height // 2 - 2][(width // 2 - 1)],
    ]
    return coords


_42cords = get_forty_two_coords(width, height)
for cell in _42cords:
    cell.is_visited = True

exit_y, exit_x = exit_
if exit_x > width or exit_y > height:
    print("Exit coordinates are out of the maze's boundes")
    exit()


if (entry_y, entry_x) == (exit_y, exit_x):
    print("Entry and exit coordinates cannot be the same")
    exit()


if maze[exit_y][exit_x] in _42cords:
    print("The exit cordinates cannot be inside 42 logo")
    exit()

if maze[entry_y][entry_x] in _42cords:
    print("The exit cordinates cannot be inside 42 logo")
    exit()

def print_maze(maze):
    print("\033[1;1H", end="")
    wall = "\033[93m██\033[0m"
    space = "\033[32m  \033[0m"

    upper_line = ""

    for c in range(len(maze[0])):
        upper_line += wall
        if maze[0][c].walls & 1:
            upper_line += wall
        else:
            upper_line += space
    upper_line += wall

    print(upper_line)

    for r in range(len(maze)):
        cell_line = ""
        bottom_line = ""

        # Cell line
        for c in range(len(maze[r])):
            if maze[r][c].walls & 8:
                cell_line += wall
            else:
                cell_line += space

            if (r, c) == entry_:
                cell_line += "\033[32m██\033[0m"

            elif (r, c) == exit_:
                cell_line += "\033[31m██\033[0m"
            elif maze[r][c] in _42cords:
                cell_line += "\033[31m██\033[0m"
            else:
                cell_line += space

        # Rightmost wall
        if maze[r][-1].walls & 2:
            cell_line += wall
        else:
            cell_line += space

        # Bottom line
        for c in range(len(maze[r])):
            bottom_line += wall
            if maze[r][c].walls & 4:
                bottom_line += wall
            else:
                bottom_line += space
        bottom_line += wall

        print(cell_line)
        print(bottom_line)




def get_neighbors(x, y):
    neighbors = []

    if x - 1 >= 0:
        neighbors += [(x - 1, y)]

    if y - 1 >= 0:
        neighbors += [(x, y - 1)]

    if x + 1 < width:
        neighbors += [(x + 1, y)]

    if y + 1 < height:
        neighbors += [(x, y + 1)]

    return neighbors


def break_wall(x, y, nx, ny):
    if y < ny:
        maze[y][x].walls -= 4
        maze[ny][nx].walls -= 1
    elif y > ny:
        maze[y][x].walls -= 1
        maze[ny][nx].walls -= 4

    if x < nx:
        maze[y][x].walls -= 2
        maze[ny][nx].walls -= 8
    if x > nx:
        maze[y][x].walls -= 8
        maze[ny][nx].walls -= 2

def dfs(x, y):
    neighbors = get_neighbors(x, y)
    random.shuffle(neighbors)
    maze[y][x].is_visited = True
    for neighbor in neighbors:
        nx, ny = neighbor
        if not maze[ny][nx].is_visited:
            # print("\033[2J\033[H", end="")
            break_wall(x, y, nx, ny)
            time.sleep(0.01)
            print_maze(maze)
            dfs(nx, ny)


def prims(start_x, start_y):
    print("\033[2J\033[H", end="")
    _42_cells = get_forty_two_coords(width, height)

    maze[start_y][start_x].is_visited = True
    pool = []
    
    for nx, ny in get_neighbors(start_x, start_y):
        pool.append((nx, ny))

    while pool:
        idx = random.randrange(len(pool))
        cx, cy = pool.pop(idx)

        if maze[cy][cx].is_visited:
            continue

        visited_neighbors = [
            (vx, vy) for (vx, vy) in get_neighbors(cx, cy)
            if maze[vy][vx].is_visited and maze[vy][vx] not in _42_cells
        ]


        sx, sy = random.choice(visited_neighbors)
        break_wall(cx, cy, sx, sy)
        # print_maze(maze)
        # time.sleep(0.001)

        maze[cy][cx].is_visited = True

        for nx, ny in get_neighbors(cx, cy):
            if not maze[ny][nx].is_visited:
                pool.append((nx, ny))
        print_maze(maze)
        time.sleep(0.001)

def output_maze(maze):
    output = ""
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            output += hex(maze[r][c].walls)[2:]
        output += "\n"
    return output

def imperfect(maze):
    
    for r in range(len(maze)):
        
        for c in range(len(maze[0])):
            print_maze(maze)
            time.sleep(0.001)
            idx = random.randrange(10)
            
            if idx > 1 and maze[r][c] not in _42cords\
                and r % 2 == 0 and c % 2 == 0:
                if maze[r][c].walls & 1 and r - 1 >= 0\
                    and maze[r - 1][c] not in _42cords:
                    maze[r][c].walls -= 1
                    maze[r - 1][c].walls -= 4

                elif maze[r][c].walls & 8 and c - 1 >= 0\
                    and maze[r][c - 1] not in _42cords:
                    maze[r][c].walls -= 8
                    maze[r][c - 1].walls -= 2

                elif maze[r][c].walls & 2 and c + 1 < width\
                    and maze[r][c + 1] not in _42cords:
                    maze[r][c].walls -= 2
                    maze[r][c + 1].walls -= 8

                elif maze[r][c].walls & 4 and r + 1 < height\
                    and maze[r + 1][c] not in _42cords:
                    maze[r][c].walls -= 4
                    maze[r + 1][c].walls -= 1
        print_maze(maze)
        time.sleep(0.00005)


def get_path(x, y):
    wall = maze[y][x].walls
    paths = []

    if not wall & 1:
        paths += [(x, y - 1)]
    if not wall & 2:
        paths += [(x + 1, y)]
    if not wall & 4:
        paths += [(x, y + 1)]
    if not wall & 8:
        paths += [(x - 1, y)]
    return paths


def print_solved(maze, paths):
    print("\033[H")

    wall = "\033[93m██\033[0m"
    space = "\033[32m  \033[0m"
    solution_wall = "██"

    upper_line = ""

    for c in range(len(maze[0])):
        upper_line += wall
        if maze[0][c].walls & 1:
            upper_line += wall
        else:
            upper_line += space
    upper_line += wall

    print(upper_line)

    for r in range(len(maze)):
        cell_line = ""
        bottom_line = ""

        # Cell line

        # This part is for corners
        for c in range(len(maze[r])):
            if maze[r][c].walls & 8:
                cell_line += wall

            elif (r, c) in paths and (r, c - 1) in paths:
                cell_line += solution_wall
            else:
                cell_line += space

        # This part if for inside the cell
            if (r, c) == entry_:
                cell_line += "\033[32m██\033[0m"
            elif (r, c) == exit_:
                cell_line += "\033[31m██\033[0m"
            elif maze[r][c] in _42cords:
                cell_line +=  "\033[31m██\033[0m"
            elif (r, c) in paths:
                cell_line += solution_wall
            else:
                cell_line += space

        # Rightmost wall
        if maze[r][-1].walls & 2:
            cell_line += wall
        else:
            cell_line += space

        # Bottom line
        for c in range(len(maze[r])):
            bottom_line += wall
            if maze[r][c].walls & 4:
                bottom_line += wall
            elif (r, c) in paths and (r + 1, c) in paths:
                bottom_line += solution_wall
            else:
                bottom_line += space
        bottom_line += wall
        print(cell_line)
        print(bottom_line)

solved = False

visited_paths_global = []

def get_open_neighbors(y, x):
    open_neighbors = []
    if not maze[y][x].walls & 1:
        open_neighbors += [(y - 1, x)]
    if not maze[y][x].walls & 2:
        open_neighbors += [(y, x + 1)]
    if not maze[y][x].walls & 4:
        open_neighbors += [(y + 1, x)]
    if not maze[y][x].walls & 8:
        open_neighbors += [(y, x - 1)]
    return open_neighbors


from collections import deque


def bfs(start_y, start_x):
    global visited_paths_global
    queue = deque()
    paths = {}
    final_path = set()
    final_path.add((start_y, start_x))
    
    queue += [(start_y, start_x)]
    while queue:
        current_cell = queue.popleft()
        
        neighbors = get_open_neighbors(*current_cell)
        for neighbor in neighbors:
            if not neighbor in final_path:
                queue.append(neighbor)
                paths[neighbor] = current_cell
                final_path.add(neighbor)
        print_solved(maze, final_path)
        time.sleep(0.000000001)
        if exit_ in neighbors:
            break
    current = exit_
    while current != (entry_y, entry_x):
        visited_paths_global.append(current)
        current = paths[current]
    visited_paths_global.append((start_y, start_x))

    visited_paths_global = visited_paths_global[::-1]

def get_path_string(paths):
    i = 0
    final_path = ""
    while i < len(paths) - 1:
        
        current_coordinates = paths[i]
        next_coordinates = paths[i + 1]
        cy, cx = current_coordinates
        ny, nx = next_coordinates
        if cy > ny:
            final_path += "N"
        elif ny > cy:
            final_path += "S"
        elif cx > nx:
            final_path += "W"
        elif nx > cx:
            final_path += "E"
        
        i += 1
    
    return final_path


def animate_solved(maze, final_path):
    os.system("clear")
    current_path = []
    for path in final_path:
        print("\033[1;1H", end="")
        print_solved(maze, current_path)
        time.sleep(0.00003)
        current_path.append(path)

dfs(0, 0)
prims(0, 0)
for cells in maze:
        for cell in cells:
            if cell not in _42cords:
                cell.is_visited = False

# imperfect(maze)
print_maze(maze)
entry_y, entry_x = entry_
bfs(entry_y, entry_x)
animate_solved(maze, visited_paths_global)
print_solved(maze, visited_paths_global)
with open("output_file.txt", "w") as f:
    f.write(output_maze(maze))
    f.write("\n")
    f.write(get_path_string(visited_paths_global))
    f.write("\n")
    f.write(f"{entry_x},{entry_y}\n")
    f.write(f"{exit_x},{exit_y}\n")
