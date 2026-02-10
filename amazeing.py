#!/usr/bin/python3
print("\033[2J\033[H", end="")
import random
import time
import sys

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


print("\033[H\033[J", end="")


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


def print_maze(maze):
    print("\033[H")
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

            if r == 0 and c == 0:
                cell_line += "\033[32m██\033[0m"

            elif r == height - 1 and c == width - 1:
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
    print("\033[2J\033[H", end="")
    neighbors = get_neighbors(x, y)
    random.shuffle(neighbors)
    maze[y][x].is_visited = True
    for neighbor in neighbors:
        nx, ny = neighbor
        if not maze[ny][nx].is_visited:
            break_wall(x, y, nx, ny)
            time.sleep(0.001)
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
        time.sleep(0.5)


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


exit_ = (width - 1, height - 1)


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
            if r == 0 and c == 0:
                cell_line += "\033[32m██\033[0m"
            elif r == height - 1 and c == width - 1:
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


def bfs(start_y, start_x):
    global visited_paths_global
    queue = []
    paths = {}
    paths2 = [(start_y, start_x)]

    queue += [(start_y, start_x)]
    while queue:
        current_cell = queue.pop(0)
        
        neighbors = get_open_neighbors(*current_cell)
        for neighbor in neighbors:
            if not neighbor in paths2:
                queue += [neighbor]
                paths[neighbor] = current_cell
                paths2 += [neighbor]
        print_solved(maze, paths2)
        time.sleep(0.007)
        if exit_ in neighbors:
            break
    current = exit_
    while current != (0, 0):
        visited_paths_global.append(current)
        current = paths[current]
    visited_paths_global.append((0, 0))

    visited_paths_global = visited_paths_global[::-1]


def solve(start, visited_paths_local):
    print("\033[2J\033[H", end="")
    x, y = start
    maze[y][x].is_visited = True
    visited_paths_local += [start]

    if start == exit_:
        global solved
        solved = True

        global visited_paths_global
        visited_paths_global = visited_paths_local.copy()
    
    if solved:
        visited_paths_local.pop()
        return
    
    paths = get_path(x, y)
    random.shuffle(paths)
    for path in paths:
        new_x, new_y = path
        if not maze[new_y][new_x].is_visited:
            if not solved:
                time.sleep(0.001)
                print_solved(maze, visited_paths_local)
            solve(path, visited_paths_local)
    visited_paths_local.pop()

# try:
#     prims(0, 0)
   
#     time.sleep(1)
#     # dfs(0, 0)
#     for cells in maze:
#         for cell in cells:
#             if cell not in _42cords:
#                 cell.is_visited = False

#     local_path = []
#     solve((0, 0), local_path)
#     print_solved(maze, visited_paths_global)
# except KeyboardInterrupt:
#     print("\nThe program was stopped by the user")
# except Exception:
#     print("Error\n")
# finally:
#     pass


prims(0, 0)
for cells in maze:
        for cell in cells:
            if cell not in _42cords:
                cell.is_visited = False

imperfect(maze)
print_maze(maze)
# solve((0, 0), [])
bfs(0, 0)
print_solved(maze, visited_paths_global)
