#!/usr/bin/python3
import random
import time


try:
    width = int(input("Enter Width of the Maze: "))
    height = int(input("Enter Height of the Maze: "))
    if width <= 6 or height <= 6:
        print("The given numbers are to small to be able to print 42")
        exit()
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
        maze[height // 2][((width // 2 - 1)) - 1],
        maze[height // 2][((width // 2 - 1)) - 2],
        maze[(height // 2) - 1][((width // 2 - 1)) - 2],
        maze[(height // 2) - 2][((width // 2 - 1)) - 2]
    ]
    return coords


_42cords = get_forty_two_coords(width, height)
for cord in _42cords:
    cord.is_visited = True


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
                cell_line += "\033[34m▢▢\033[0m"
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
            break_wall(x, y, nx, ny)
            time.sleep(0.07)
            print_maze(maze)
            dfs(nx, ny)


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
visited_paths = []


def print_solved(maze, paths):
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

            elif (c, r) in paths and (c - 1, r) in paths:
                cell_line += "██"
            else:
                cell_line += space

            if r == 0 and c == 0:
                cell_line += "\033[32m██\033[0m"

            elif r == height - 1 and c == width - 1:
                cell_line += "\033[31m██\033[0m"
            elif maze[r][c] in _42cords:
                cell_line += "\033[31m██\033[0m"
            elif (c, r) in paths:
                cell_line += "██"
            else:
                cell_line += space

        # Rightmost wall
        if maze[r][-1].walls & 2:
            cell_line += wall
        elif (c, r) in paths:
            cell_line += "██"
        else:
            cell_line += space

        # Bottom line
        for c in range(len(maze[r])):
            bottom_line += wall
            if maze[r][c].walls & 4:
                bottom_line += wall

            elif (c, r) in paths and (c, r + 1) in paths:
                bottom_line += "██"
            else:
                bottom_line += space
        bottom_line += wall
        print(cell_line)
        print(bottom_line)


solved = False


def solve(start, visited_paths_):
    x, y = start
    maze[y][x].is_visited = True
    paths = get_path(x, y)
    random.shuffle(paths)
    global solved

    if start == exit_:
        visited_paths_ += [start]
        visited_paths.append(visited_paths_.copy())
        solved = True
        return

    if solved:
        return
    for path in paths:
        xx, yy = path
        if not maze[yy][xx].is_visited:
            visited_paths_ += [start]
            if not solved:
                time.sleep(0.07)
                print_solved(maze, visited_paths_)
            solve(path, visited_paths_)

            visited_paths_.pop()


try:
    dfs(0, 0)

    for cells in maze:
        for cell in cells:
            if cell not in _42cords:
                cell.is_visited = False
    solve((0, 0), [])
    print_solved(maze, visited_paths[0])
    pass

except KeyboardInterrupt:
    print("\nThe program was stopped by the user")
finally:
    print("\033[?25h", end="")
