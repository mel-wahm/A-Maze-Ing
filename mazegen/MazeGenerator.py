import random
import time
import sys
import os
from typing import Any
from collections import deque
from .helper import Colors


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear')


sys.setrecursionlimit(10**6)


class MazeGenerator:
    """Generate, solve, render, and export mazes."""
    BLOCK = "██"

    def __init__(
            self, width: int, height: int, _exit: tuple[int, int],
            _entry: tuple[int, int],
            seed: int | None = None) -> None:
        """Initialize maze state and validate entry and exit.

        Parameters:
            width: Maze width.
            height: Maze height.
            _exit: Exit coordinates `(x, y)`.
            _entry: Entry coordinates `(x, y)`.
            seed: Random seed for reproducible generation.
        """
        random.seed(seed)
        self.width = width
        self.height = height
        self.exit_ = _exit
        self.entry_ = _entry
        self.solved = False
        self.visited_paths_global: list[tuple[int, int]] = []
        self.wall_color = Colors.RED

        # Initialize maze
        self.class_cell = self._create_cell_class()
        self.maze = [
            [self.class_cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self._42cords = self.get_forty_two_coords()
        for cell in self._42cords:
            cell.is_visited = True

        en_x, en_y = self.entry_
        if self.maze[en_y][en_x] in self._42cords:
            raise Exception("The entry cordinates cannot be inside 42 logo")
        ex_x, ex_y = self.exit_
        if self.maze[ex_y][ex_x] in self._42cords:
            raise Exception("The exit cordinates cannot be inside 42 logo")

    def _create_cell_class(self) -> Any:
        """Create the internal `Cell` class used by the maze grid."""
        class Cell:
            def __init__(self) -> None:
                """Initialize a maze cell."""
                self.walls = 15
                self.is_visited = False
        return Cell

    def get_forty_two_coords(self) -> list[Any]:
        """Return cells reserved for the centered 42 logo."""
        coords = [
            self.maze[self.height // 2][(self.width // 2 + 1)],
            self.maze[self.height // 2][(self.width // 2 + 2)],
            self.maze[self.height // 2][(self.width // 2 + 3)],
            self.maze[self.height // 2 - 1][(self.width // 2 + 3)],
            self.maze[self.height // 2 - 2][(self.width // 2 + 3)],
            self.maze[self.height // 2 - 2][(self.width // 2 + 2)],
            self.maze[self.height // 2 - 2][(self.width // 2 + 1)],
            self.maze[self.height // 2 + 1][(self.width // 2 + 1)],
            self.maze[self.height // 2 + 2][(self.width // 2 + 1)],
            self.maze[self.height // 2 + 2][(self.width // 2 + 2)],
            self.maze[self.height // 2 + 2][(self.width // 2 + 3)],

            self.maze[self.height // 2][(self.width // 2 - 1)],
            self.maze[(self.height // 2) + 1][(self.width // 2 - 1)],
            self.maze[(self.height // 2) + 2][(self.width // 2 - 1)],
            self.maze[self.height // 2][self.width // 2 - 2],
            self.maze[self.height // 2][self.width // 2 - 3],
            self.maze[(self.height // 2) - 1][self.width // 2 - 3],
            self.maze[(self.height // 2) - 2][self.width // 2 - 3],
            self.maze[self.height // 2 - 1][(self.width // 2 - 1)],
            self.maze[self.height // 2 - 2][(self.width // 2 - 1)],
        ]
        return coords

    def print_maze(self) -> None:
        """Render the current maze in the terminal."""
        os.system('clear')
        wall = f"{self.wall_color}{self.BLOCK}{Colors.END}"
        space = f"{Colors.GREEN}  {Colors.END}"

        upper_line = ""

        for c in range(len(self.maze[0])):
            upper_line += wall
            if self.maze[0][c].walls & 1:
                upper_line += wall
            else:
                upper_line += space
        upper_line += wall

        print(upper_line)

        for r in range(len(self.maze)):
            cell_line = ""
            bottom_line = ""

            # Cell line
            for c in range(len(self.maze[r])):
                if self.maze[r][c].walls & 8:
                    cell_line += wall
                else:
                    cell_line += space

                entry_x, entry_y = self.entry_
                if r == entry_y and c == entry_x:
                    cell_line += f"{Colors.YELLOW}{self.BLOCK}{Colors.END}"

                elif (c, r) == self.exit_:
                    cell_line += f"{Colors.GREEN}{self.BLOCK}{Colors.END}"
                elif self.maze[r][c] in self._42cords:
                    cell_line += f"{self.wall_color}💥{Colors.END}"
                else:
                    cell_line += space

            # Rightmost wall
            if self.maze[r][-1].walls & 2:
                cell_line += wall
            else:
                cell_line += space

            # Bottom line
            for c in range(len(self.maze[r])):
                bottom_line += wall
                if self.maze[r][c].walls & 4:
                    bottom_line += wall
                else:
                    bottom_line += space
            bottom_line += wall

            print(cell_line)
            print(bottom_line)

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return orthogonal neighbors of a cell.

        Parameters:
            x: Cell x-coordinate.
            y: Cell y-coordinate.
        """
        neighbors = []

        if x - 1 >= 0:
            neighbors += [(x - 1, y)]

        if y - 1 >= 0:
            neighbors += [(x, y - 1)]

        if x + 1 < self.width:
            neighbors += [(x + 1, y)]

        if y + 1 < self.height:
            neighbors += [(x, y + 1)]

        return neighbors

    def break_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        """Remove the wall between two adjacent cells.

        Parameters:
            x: First cell x-coordinate.
            y: First cell y-coordinate.
            nx: Neighbor cell x-coordinate.
            ny: Neighbor cell y-coordinate.
        """
        if y < ny:
            self.maze[y][x].walls -= 4
            self.maze[ny][nx].walls -= 1
        elif y > ny:
            self.maze[y][x].walls -= 1
            self.maze[ny][nx].walls -= 4

        if x < nx:
            self.maze[y][x].walls -= 2
            self.maze[ny][nx].walls -= 8
        if x > nx:
            self.maze[y][x].walls -= 8
            self.maze[ny][nx].walls -= 2

    def dfs(self, x: int, y: int) -> None:
        """Carve maze passages with depth-first search.

        Parameters:
            x: Starting x-coordinate.
            y: Starting y-coordinate.
        """
        flash = 0
        neighbors = self.get_neighbors(x, y)
        random.shuffle(neighbors)
        self.maze[y][x].is_visited = True
        for neighbor in neighbors:
            nx, ny = neighbor
            if not self.maze[ny][nx].is_visited:
                self.break_wall(x, y, nx, ny)
                if flash % 10 == 0:
                    time.sleep(0.02)
                    self.print_maze()
                self.dfs(nx, ny)
            flash += 1

    def prims(self, start_x: int, start_y: int) -> None:
        """Carve maze passages with Prim's algorithm.

        Parameters:
            start_x: Starting x-coordinate.
            start_y: Starting y-coordinate.
        """
        clear_screen()
        flash = 0
        self.maze[start_y][start_x].is_visited = True
        pool = []

        for nx, ny in self.get_neighbors(start_x, start_y):
            pool.append((nx, ny))

        while pool:
            idx = random.randrange(len(pool))
            cx, cy = pool.pop(idx)

            if self.maze[cy][cx].is_visited:
                continue

            visited_neighbors = [
                (vx, vy) for (vx, vy) in self.get_neighbors(cx, cy)
                if self.maze[vy][vx].is_visited
                and self.maze[vy][vx] not in self._42cords
            ]

            sx, sy = random.choice(visited_neighbors)
            self.break_wall(cx, cy, sx, sy)

            self.maze[cy][cx].is_visited = True

            for nx, ny in self.get_neighbors(cx, cy):
                if not self.maze[ny][nx].is_visited:
                    pool.append((nx, ny))
            if flash % 10 == 0:
                time.sleep(0.02)
                self.print_maze()
            flash += 1

    def imperfect(self) -> None:
        """Remove extra walls to create an imperfect maze."""
        frame = 0
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):

                if self.maze[r][c] not in self._42cords\
                        and r % 2 == 0 and c % 2 == 0:
                    if self.maze[r][c].walls & 1 and r - 1 >= 0\
                            and self.maze[r - 1][c] not in self._42cords:
                        self.maze[r][c].walls -= 1
                        self.maze[r - 1][c].walls -= 4

                    elif self.maze[r][c].walls & 8 and c - 1 >= 0\
                            and self.maze[r][c - 1] not in self._42cords:
                        self.maze[r][c].walls -= 8
                        self.maze[r][c - 1].walls -= 2

                    elif self.maze[r][c].walls & 2 and c + 1 < self.width\
                            and self.maze[r][c + 1] not in self._42cords:
                        self.maze[r][c].walls -= 2
                        self.maze[r][c + 1].walls -= 8

                    elif self.maze[r][c].walls & 4 and r + 1 < self.height\
                            and self.maze[r + 1][c] not in self._42cords:
                        self.maze[r][c].walls -= 4
                        self.maze[r + 1][c].walls -= 1
            if frame % 5 == 0:
                self.print_maze()
                time.sleep(0.01)
            frame += 1

    def get_path(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return reachable coordinates from a cell.

        Parameters:
            x: Cell x-coordinate.
            y: Cell y-coordinate.
        """
        wall = self.maze[y][x].walls
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

    def print_solved(
            self, paths: set[tuple[int, int]] | list[tuple[int, int]]) -> None:
        """Render the maze with a highlighted path.

        Parameters:
            paths: Coordinates to highlight.
        """
        clear_screen()

        wall = f"{self.wall_color}{self.BLOCK}{Colors.END}"
        space = f"{Colors.GREEN}  {Colors.END}"
        solution_wall = f"{Colors.WHITE}{self.BLOCK}{Colors.END}"

        upper_line = ""

        for c in range(len(self.maze[0])):
            upper_line += wall
            if self.maze[0][c].walls & 1:
                upper_line += wall
            else:
                upper_line += space
        upper_line += wall

        print(upper_line)

        for r in range(len(self.maze)):
            cell_line = ""
            bottom_line = ""

            # Cell line

            # This part is for corners
            for c in range(len(self.maze[r])):
                if self.maze[r][c].walls & 8:
                    cell_line += wall

                elif (c, r) in paths and (c - 1, r) in paths:
                    cell_line += solution_wall
                else:
                    cell_line += space

            # This part if for inside the cell
                entry_x, entry_y = self.entry_
                if r == entry_y and c == entry_x:
                    cell_line += f"{Colors.YELLOW}{self.BLOCK}{Colors.END}"
                elif (c, r) == self.exit_:
                    cell_line += f"{Colors.GREEN}{self.BLOCK}{Colors.END}"
                elif self.maze[r][c] in self._42cords:
                    cell_line += f"{self.wall_color}💥{Colors.END}"
                elif (c, r) in paths:
                    cell_line += solution_wall
                else:
                    cell_line += space

            # Rightmost wall
            if self.maze[r][-1].walls & 2:
                cell_line += wall
            else:
                cell_line += space

            # Bottom line
            for c in range(len(self.maze[r])):
                bottom_line += wall
                if self.maze[r][c].walls & 4:
                    bottom_line += wall
                elif (c, r) in paths and (c, r + 1) in paths:
                    bottom_line += solution_wall
                else:
                    bottom_line += space
            bottom_line += wall
            print(cell_line)
            print(bottom_line)

    def get_open_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return accessible neighbors of a cell.

        Parameters:
            x: Current cell x-coordinate.
            y: Current cell y-coordinate.
        """
        open_neighbors = []
        if not self.maze[y][x].walls & 8:
            open_neighbors += [(x - 1, y)]
        if not self.maze[y][x].walls & 4:
            open_neighbors += [(x, y + 1)]
        if not self.maze[y][x].walls & 2:
            open_neighbors += [(x + 1, y)]
        if not self.maze[y][x].walls & 1:
            open_neighbors += [(x, y - 1)]
        return open_neighbors

    @staticmethod
    def construct_path(came_from: dict[tuple[int, int],
                                       tuple[int, int]],
                       start: tuple[int, int],
                       end: tuple[int, int]) -> list[tuple[int, int]]:
        """Reconstruct a path from `start` to `end`.

        Parameters:
            came_from: Map of node to its previous node.
            start: Start coordinates.
            end: End coordinates.
        """
        result = []
        current = end

        while current != start:
            result.append(current)
            current = came_from[current]

        result.append(start)
        result.reverse()
        return result

    def bfs(self, flag: bool = False) -> None:
        """Find a shortest path from entry to exit with BFS.

        Parameters:
            flag: If `True`, animate search progress in the terminal.
        """
        start_x, start_y = self.entry_
        exit_x, exit_y = self.exit_

        queue: deque[tuple[int, int]] = deque()
        visited = set()
        came_from = {}

        queue.append((start_x, start_y))
        visited.add((start_x, start_y))

        frame_counter = 0
        while queue:
            current = queue.popleft()
            neighbors = self.get_open_neighbors(*current)

            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                queue.append(neighbor)
                came_from[neighbor] = current
                visited.add(neighbor)

                if neighbor == (exit_x, exit_y):
                    self.visited_paths_global = self.construct_path(
                        came_from, (start_x, start_y), neighbor)
                    return

            frame_counter += 1
            if flag and frame_counter % 5 == 0:
                self.print_solved(visited)
                time.sleep(0.03)

    @staticmethod
    def get_path_string(paths: list[tuple[int, int]]) -> str:
        """Convert coordinates into `N/S/E/W` directions.

        Parameters:
            paths: Ordered path coordinates.
        """
        i = 0
        final_path = ""
        while i < len(paths) - 1:

            current_coordinates = paths[i]
            next_coordinates = paths[i + 1]
            cx, cy = current_coordinates
            nx, ny = next_coordinates
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

    def output_maze(self) -> str:
        """Serialize maze walls as hexadecimal rows.

        Returns:
            Maze wall values separated by newlines.
        """
        output = ""
        for r in range(len(self.maze)):
            for c in range(len(self.maze[r])):
                output += (hex(self.maze[r][c].walls)[2:]).upper()
            output += "\n"
        return output

    def output_file(self, file_name: str) -> None:
        """Write maze data and solution path to a file.

        Parameters:
            file_name: Output file path.
        """
        try:
            with open(f"{file_name}", "w") as f:
                f.write(f"""{self.output_maze()}
{self.entry_[0]},{self.entry_[1]}
{self.exit_[0]},{self.exit_[1]}
{self.get_path_string(self.visited_paths_global)}
""")

        except Exception:
            raise
