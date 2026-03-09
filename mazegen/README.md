**Reusable Module:**

The `mazegen` package can be imported and used in other projects. The main reusable components are:

- **`MazeGenerator` class**: Generates, solves, and displays mazes. Core methods include `dfs()`, `prims()` (generation), `bfs()` (solving), `print_maze()` (display), and `output_file()` (export).
- **`read_config()` function**: Parses configuration files with validation.
- **`Colors` class**: ANSI color codes for terminal output.

**Example Usage:**

```python
from mazegen import MazeGenerator, read_config

# Create a maze
maze = MazeGenerator(width=20, height=15, _entry=(0, 0), _exit=(19, 14))

# Generate using DFS or Prim's
maze.dfs(0, 0)

# Solve with BFS
maze.bfs()

# Display and export
maze.print_solved(maze.visited_paths_global)
maze.output_file("maze.txt")
```
