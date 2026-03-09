from .MazeGenerator import MazeGenerator, clear_screen
from .helper import Colors


def read_config(path: str) -> dict[str, str]:
    """Load maze config values from a text file.

    Parameters:
        path: Path to the config file.

    Returns:
        Parsed config keys and values.
    """
    config = {}
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line {line}: no '=' found")
                key, value = line.split("=", 1)
                config[key.upper().strip()] = value
    except FileNotFoundError:
        print(f"No such file or directory: '{path}'")
        raise
    except ValueError as e:
        print(f"[ERROR] Config syntax error: {e}")
        raise

    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(
            f"[ERROR] Missing keys in config: {', '.join(missing)}")

    return config


def check_config(config: dict[str, str]) -> tuple[int, int, int, int, int, int,
                                                  int | None, str, str]:
    """Validate and normalize maze configuration values.

    Parameters:
        config: Raw config mapping.

    Returns:
        Parsed values as `(entry_x, entry_y, exit_x, exit_y, width, height,
        seed, perfect, output_file)`.
    """
    # --- Validate WIDTH ---
    raw_width = config.get("WIDTH", "").strip()
    if not raw_width:
        raise ValueError("Error: WIDTH is empty in config.")
    try:
        width = int(raw_width)
    except ValueError:
        raise ValueError(f"Error: WIDTH '{raw_width}' is not a valid integer.")

    # --- Validate HEIGHT ---
    raw_height = config.get("HEIGHT", "").strip()
    if not raw_height:
        raise ValueError("Error: HEIGHT is empty in config.")
    try:
        height = int(raw_height)
    except ValueError:
        raise ValueError(
            f"Error: HEIGHT '{raw_height}' is not a valid integer.")

    # --- Validate WIDTH/HEIGHT range ---
    if width < 9 or height < 7:
        raise ValueError(
            "Error: To properly show the '42' logo, minimum size is 9x7."
        )
    if width > 45 or height > 45:
        raise ValueError(
            f"Error: Maze too large ({width}x{height}). Maximum is 45x45."
        )

    # --- Validate ENTRY format ---
    raw_entry = config.get("ENTRY", "").strip()
    if not raw_entry or "," not in raw_entry:
        raise ValueError(
            f"Error: ENTRY '{raw_entry}' is not valid. Expected format: x,y"
        )
    try:
        entry_parts = raw_entry.split(",")
        if len(entry_parts) != 2:
            raise ValueError("Expected exactly two values")
        entry_x, entry_y = int(entry_parts[0]), int(entry_parts[1])
    except ValueError:
        raise ValueError(
            f"Error: ENTRY '{raw_entry}' contains non-integer "
            f"values. Expected format: x,y"
        )

    # --- Validate EXIT format ---
    raw_exit = config.get("EXIT", "").strip()
    if not raw_exit or "," not in raw_exit:
        raise ValueError(
            f"Error: EXIT '{raw_exit}' is not valid. Expected format: x,y"
        )
    try:
        exit_parts = raw_exit.split(",")
        if len(exit_parts) != 2:
            raise ValueError("Expected exactly two values")
        exit_x, exit_y = int(exit_parts[0]), int(exit_parts[1])
    except ValueError:
        raise ValueError(
            f"Error: EXIT '{raw_exit}' contains non-integer "
            f"values. Expected format: x,y"
        )

    # --- Validate ENTRY != EXIT ---
    if (entry_x, entry_y) == (exit_x, exit_y):
        raise ValueError(
            "Error: ENTRY and EXIT must be different coordinates."
        )

    # --- Validate ENTRY bounds ---
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ValueError(
            f"Error: ENTRY ({entry_x},{entry_y}) is out of "
            f"maze bounds ({width}x{height})."
        )

    # --- Validate EXIT bounds ---
    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ValueError(
            f"Error: EXIT ({exit_x},{exit_y}) is out of "
            f"maze bounds ({width}x{height})."
        )

    # --- Validate PERFECT ---
    perfect = config.get("PERFECT", "").strip()
    if perfect.lower() not in ("true", "false"):
        raise ValueError(
            f"Error: PERFECT '{perfect}' is not valid. "
            f"Expected 'true' or 'false'."
        )

    # --- Validate OUTPUT_FILE ---
    output_file = config.get("OUTPUT_FILE", "").strip()
    if not output_file:
        print(
            f"{Colors.RED}Error: OUTPUT_FILE is empty in config."
            )
        exit()

    # --- Validate SEED (optional) ---
    seed = None
    if "SEED" in config and config["SEED"].strip():
        try:
            seed = int(config["SEED"].strip())
        except ValueError:
            print(
                f"{Colors.RED}Error: SEED '{config['SEED']}' is "
                f"not a valid integer.{Colors.END}")
            exit()
    return (entry_x, entry_y, exit_x, exit_y,
            width, height, seed, perfect, output_file)


def main(
        file: str, algo: str,
        config_overrides: dict[str, str] | None = None
) -> tuple[MazeGenerator, str]:
    """Build, solve, and export a maze from config.

    Parameters:
        file: Config file path.
        algo: Generation algorithm (`"prims"` or `"dfs"`).
        config_overrides: Values that override file config.
    """
    config = read_config(file)

    if config_overrides:
        config.update(config_overrides)

    entry_x, entry_y, exit_x, exit_y, width, height, seed, \
        perfect, file_name = check_config(config)

    logic = MazeGenerator(
        width, height, (exit_x, exit_y),
        (entry_x, entry_y),
        seed)

    if algo == "prims":
        logic.prims(entry_x, entry_y)
        for cells in logic.maze:
            for cell in cells:
                if cell not in logic._42cords:
                    cell.is_visited = False

    elif algo == "dfs":
        clear_screen()
        logic.dfs(entry_x, entry_y)
        for cells in logic.maze:
            for cell in cells:
                if cell not in logic._42cords:
                    cell.is_visited = False

    if isinstance(perfect, str):
        is_perfect = perfect.lower() == "true"
    if not is_perfect:
        logic.imperfect()
    logic.bfs()
    logic.print_solved(logic.visited_paths_global)
    logic.output_file(file_name)

    return logic, file_name
