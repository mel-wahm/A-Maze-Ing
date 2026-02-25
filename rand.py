#!/usr/bin/python3
import random
import time
import sys
import os
from collections import deque

os.system('clear')
sys.setrecursionlimit(2147483647)
SEED = 42
# random.seed(SEED)

try:
    width = int(input("Enter Width of the Maze: "))
    height = int(input("Enter Height of the Maze: "))
    if width < 9 or height < 7:
        print("The given numbers are too small to be able to print 42")
        exit()
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


maze = [[Cell() for _ in range(width)] for _ in range(height)]


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
    print("Exit coordinates are out of the maze's bounds")
    exit()

if (entry_y, entry_x) == (exit_y, exit_x):
    print("Entry and exit coordinates cannot be the same")
    exit()

if maze[exit_y][exit_x] in _42cords:
    print("The exit coordinates cannot be inside 42 logo")
    exit()

if maze[entry_y][entry_x] in _42cords:
    print("The entry coordinates cannot be inside 42 logo")
    exit()


def print_maze(maze, highlight_cells=None):
    print("\033[H", end="")
    
    wall = "\033[93m██\033[0m"
    space = "\033[32m  \033[0m"
    solution_wall = "██"
    
    if highlight_cells is None:
        highlight_cells = set()

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

        for c in range(len(maze[r])):
            if maze[r][c].walls & 8:
                cell_line += wall
            elif (r, c) in highlight_cells and (r, c - 1) in highlight_cells:
                cell_line += solution_wall
            else:
                cell_line += space

            if (r, c) == entry_:
                cell_line += "\033[32m██\033[0m"
            elif (r, c) == exit_:
                cell_line += "\033[31m██\033[0m"
            elif maze[r][c] in _42cords:
                cell_line += "\033[31m██\033[0m"
            elif (r, c) in highlight_cells:
                cell_line += solution_wall
            else:
                cell_line += space

        if maze[r][-1].walls & 2:
            cell_line += wall
        else:
            cell_line += space

        for c in range(len(maze[r])):
            bottom_line += wall
            if maze[r][c].walls & 4:
                bottom_line += wall
            elif (r, c) in highlight_cells and (r + 1, c) in highlight_cells:
                bottom_line += solution_wall
            else:
                bottom_line += space
        bottom_line += wall

        print(cell_line)
        print(bottom_line)


def get_neighbors(x, y):
    neighbors = []
    if x - 1 >= 0:
        neighbors.append((x - 1, y))
    if y - 1 >= 0:
        neighbors.append((x, y - 1))
    if x + 1 < width:
        neighbors.append((x + 1, y))
    if y + 1 < height:
        neighbors.append((x, y + 1))
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
            break_wall(x, y, nx, ny)
            time.sleep(0.005)
            print_maze(maze)
            dfs(nx, ny)


def prims(start_x, start_y):
    _42_cells = get_forty_two_coords(width, height)

    maze[start_y][start_x].is_visited = True
    pool = []

    for nx, ny in get_neighbors(start_x, start_y):
        pool.append((nx, ny))

    frame_counter = 0
    while pool:
        idx = random.randrange(len(pool))
        cx, cy = pool.pop(idx)

        if maze[cy][cx].is_visited:
            continue

        visited_neighbors = [
            (vx, vy) for (vx, vy) in get_neighbors(cx, cy)
            if maze[vy][vx].is_visited and maze[vy][vx] not in _42_cells
        ]

        if not visited_neighbors:
            continue

        sx, sy = random.choice(visited_neighbors)
        break_wall(cx, cy, sx, sy)

        maze[cy][cx].is_visited = True

        for nx, ny in get_neighbors(cx, cy):
            if not maze[ny][nx].is_visited:
                pool.append((nx, ny))

        frame_counter += 1
        if frame_counter % 10 == 0:
            print_maze(maze)
            time.sleep(0.01)


def imperfect(maze):
    frame_counter = 0
    for r in range(len(maze)):
        for c in range(len(maze[0])):

            if maze[r][c] not in _42cords and r % 2 == 0 and c % 2 == 0:
                if maze[r][c].walls & 1 and r - 1 >= 0 and maze[r - 1][c] not in _42cords:
                    maze[r][c].walls -= 1
                    maze[r - 1][c].walls -= 4
                elif maze[r][c].walls & 8 and c - 1 >= 0 and maze[r][c - 1] not in _42cords:
                    maze[r][c].walls -= 8
                    maze[r][c - 1].walls -= 2
                elif maze[r][c].walls & 2 and c + 1 < width and maze[r][c + 1] not in _42cords:
                    maze[r][c].walls -= 2
                    maze[r][c + 1].walls -= 8
                elif maze[r][c].walls & 4 and r + 1 < height and maze[r + 1][c] not in _42cords:
                    maze[r][c].walls -= 4
                    maze[r + 1][c].walls -= 1

            frame_counter += 1
            if frame_counter % 20 == 0:
                print_maze(maze)
                time.sleep(0.01)


def get_open_neighbors(y, x):
    open_neighbors = []
    if not maze[y][x].walls & 1:
        open_neighbors.append((y - 1, x))
    if not maze[y][x].walls & 2:
        open_neighbors.append((y, x + 1))
    if not maze[y][x].walls & 4:
        open_neighbors.append((y + 1, x))
    if not maze[y][x].walls & 8:
        open_neighbors.append((y, x - 1))
    return open_neighbors


def bfs(startx, starty, exitx, exity):
    queue = deque()
    visited = set()
    came_from = {}

    queue.append((startx, starty))
    visited.add((startx, starty))

    frame_counter = 0
    while queue:
        current = queue.popleft()
        neighbors = get_open_neighbors(*current)

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            queue.append(neighbor)
            came_from[neighbor] = current
            visited.add(neighbor)

            if neighbor == (exitx, exity):
                return construct_path(came_from, (startx, starty), neighbor)

        frame_counter += 1
        if frame_counter % 5 == 0:
            print_maze(maze, visited)
            time.sleep(0.03)

    return None


def construct_path(came_from, start, end):
    result = []
    current = end

    while current != start:
        result.append(current)
        current = came_from[current]

    result.append(start)
    result.reverse()
    return result


def animate_solved(maze, final_path):
    current_path = []
    for path in final_path:
        print_maze(maze, current_path)
        time.sleep(0.01)
        current_path.append(path)
    print_maze(maze, current_path)


#dfs(0,0)
prims(0, 0)

# Reset visited flags
for cells in maze:
    for cell in cells:
        if cell not in _42cords:
            cell.is_visited = False


#imperfect(maze)


entry_y, entry_x = entry_
bfs_path = bfs(entry_y, entry_x, exit_y, exit_x)


animate_solved(maze, bfs_path)


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


def output_maze(maze):
    output = ""
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            output += hex(maze[r][c].walls)[2:]
        output += "\n"
    return output

with open("output_file.txt", "w") as f:
    f.write(output_maze(maze))
    f.write("\n")
    f.write(get_path_string(bfs_path))
    f.write("\n")
    f.write(f"{entry_x},{entry_y}\n")
    f.write(f"{exit_x},{exit_y}\n")
