*This project has been created as part of the 42 curriculum by mel-wahm, tsellak*

**DESCRIPTION:**
- A-Maze-ing is a Python-based maze generator and visualizer built as part of the 42 curriculum. This project's goal is to create a maze and display it, using certain algorithms, and depending on a simple configuration file.

- To generate the maze, our program reads from a configuration file, to know the dimensions of our maze, the entry and exit coordinates... we will get back to this in details in a later chapter, from this our program create a grid of cells, each cell has a number, showing the details of its wall (open or closed), the way to know if a wall in a cell exist or not, you check the digit in the binary corresponding to each wall (North --> 0001, East --> 0010, South --> 0100, West --> 1000), north corresponding to the least significant bit and east being second least significant bit and so on... we will get back to how we generate this grid using algorithms in later chapters.

**INSTRUCTIONS:**

We added a makefile to make it easier for users to run the program.

First, you should run:
bash
make install

This will install all the needed dependencies to run the program.

After this, we run:
bash
make run

This will launch the program and generate the maze, just make sure to have your configuration file in the root of your repository.

We also have some other tools inside makefile like **make lint**, which checks mypy and flake8, and **make clean** which clean our repository (removes folders like .mypy_cache, \_\_pycache\_\_...)

You might as well run the program directly using:
bash
python3 a_maze_ing.py config_file.txt


**Configuration File Format:**

The configuration file should be in this format:

| Key         | Description              | Example                |
|-------------|--------------------------|------------------------|
| `WIDTH`     | Maze width in cells      | `WIDTH=20`             |
| `HEIGHT`    | Maze height in cells     | `HEIGHT=15`            |
| `ENTRY`     | Entry coordinates (x,y)  | `ENTRY=0,0`            |
| `EXIT`      | Exit coordinates (x,y)   | `EXIT=19,14`           |
| `OUTPUT_FILE` | Output filename        | `OUTPUT_FILE=maze.txt` |
| `PERFECT`   | Generate a perfect maze  | `PERFECT=True`         |
| `SEED`      | Seed for reproducibility | `SEED=42`              |


Any missing key will cause the program to not run.

**Chosen Algorithms:**

For this project we used three algorithms in total, two for the creation of the maze and one for the solving.

-- **DFS:**
- We chose dfs for two simple reasons, it is easy to implement, and it looks cool. The way that dfs works (recursion and backtracking) make the shape look like a real puzzle, and as big as the maze gets it makes it a really hard maze to implement.
- How does DFS work:
  The logic of **dfs** is pretty straight forward, we give it a cell, it looks at its adjacent neighbors that aren't already visited, and choose one of them randomly, and we do the same for the chosen neighbor, we do this until we encounter a dead-end, meaning choosing a cell with no adjacent unvisited neighbors, here we do the backtracking, each cell represents a function call
  and when the we get to the deadend, we skip the 'if condition' which skips the recursion call,
  this pops the current function frame and goes back to the previous one, going back until we have multiple choice, and we go from there again, this pattern will make sure that we visited all the maze cells only once, making sure it is a  perfect maze and that we do not have 3x3 open areas which will need to open a cell more than once.

-- **PRIM'S:**
- We chose this algorithm for its simple implementation, it is easy to understand as well, even though it doesn't produce appealing mazes like the dfs algorithm.
- To create a full perfect maze using prim's, we start from the beginning cell, we add all its unvisited neighbors to a list (usually called frontier or a pool), and choose a random one between them. Then we loop through this cell's neighbors, choose one unvisited cell, and break the wall between them. Since we choose randomly from a random list of cells, we could be digging a wall in the up-right of the maze and then another wall in the bottom-left.

-- **BFS:**
- We chose this algorithm because it is the perfect choice for solving, as it gets us the shortest path between entry and exit. The way it works is that it checks the maze level by level. For instance, we add the entry as our search beginning and check for the exit in all its adjacent neighbors. Then we add all the cell's neighbors to a queue so we can check them in order. The moment we find the exit, we stop the search and construct the path from the end to the start, then reverse the list.
- By saving each cell and its parent cell in a dictionary of form ('cell':'parent'), we guarantee to have the full and shortest path without any additional cells.


**Reusable Module:**

The `mazegen` package can be imported and used in other projects. The main reusable components are:

- **`MazeGenerator` class**: Generates, solves, and displays mazes. Core methods include `dfs()`, `prims()` (generation), `bfs()` (solving), `print_maze()` (display), and `output_file()` (export).
- **`read_config()` function**: Parses configuration files with validation.
- **`Colors` class**: ANSI color codes for terminal output.

**Example Usage:**

```python
from mazegen import MazeGenerator, read_config

# Create a maze
maze = MazeGenerator(width=20, height=15, _entry=(0, 0), _exit=(19, 14), SEED=42)

# Generate using DFS or Prim's
maze.dfs(0, 0)

# Solve with BFS
maze.bfs()

# Display and export
maze.print_solved(maze.visited_paths_global)
maze.output_file("maze.txt")
```

**Team and Project Management:**

**Roles:**
- **Mohamed (mel-wahm)**: Algorithms (DFS, Prim's, BFS) and maze generation/solving
- **Taha (tsellak)**: Configuration parsing, validation, and CLI interface

**What Worked Well:**
- We divided the work correctly, saving time and keeping the work straightforward. We discussed every choice to ensure we agreed on how things should work.

**Challenges:**
- We could have saved time by focusing on this project alone, but we were juggling too many things at once, which slowed progress.
- We actually anticipated this project to be done almost a week ago, but the amount of edge cases that people test on the evaluation session made it harder to finish on time.

**Tools:** Python 3.10+, Mypy, Flake8, Git, Make

**Resources**

Documentation & Articles

- [Maze Generation Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-First Search - Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Prim's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Breadth-First Search - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Maze Generation: Recursive Backtracker (DFS) - jamisbuck.org](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Maze Generation: Prim's Algorithm - jamisbuck.org](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
- [Pathfinding: BFS explained - redblobgames.com](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

**Video References**

- [Depth First Search in 4 minutes - YouTube](https://www.youtube.com/watch?v=Urx87-NMm6c)
- [Breadth First Search in 4 minutes - YouTube](https://www.youtube.com/watch?v=HZ5YTanv5QE)
- [Prim's Minimum Spanning Tree - YouTube](https://www.youtube.com/watch?v=cplfcGZmX7I)
- [Maze Generation Algorithms - YouTube](https://www.youtube.com/watch?v=Y37-gB83HKE)

**AI Usage**

We used AI primarily for this project to understand algorithm logic better, help with making the docstrings, and as a tool to improve code readability and structure.
