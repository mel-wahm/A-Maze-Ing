import sys
import time
from mazegen import (
    Colors, clear_screen, clear_menu,
    print_main_menu, print_settings_menu,
    main, read_config
)
from mazegen.MazeGenerator import MazeGenerator


def get_input(prompt: str) -> str:
    """Return user input from a green-formatted prompt."""
    return input(f"{Colors.GREEN}{prompt}: {Colors.END}")


def settings_loop(config: dict[str, str],
                  current_algo: str, logic: MazeGenerator | None = None,
                  show_solved: bool = False) -> tuple[dict[str, str],
                                                      str]:
    """Updated config and active algorithm.

    Parameters:
        config: Current maze configuration.
        current_algo: Active algorithm (`"prims"` or `"dfs"`).
        logic: Current maze instance, if available.
        show_solved: Whether solved view is currently shown.
    """
    while True:
        if logic:
            redraw_maze(logic, show_solved)
        print_settings_menu(config, current_algo, has_maze=(logic is not None))

        try:
            choice = get_input("Enter choice")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.YELLOW}Closing!...{Colors.END}")
            exit()

        if choice == "1":
            if current_algo == "prims":
                current_algo = "dfs"
            else:
                current_algo = "prims"
        elif choice == "2":
            try:
                val = get_input("Enter new WIDTH (9-45)")
                if val.isdigit() and 9 <= int(val) <= 45:
                    config["WIDTH"] = val
                else:
                    print(
                        f"{Colors.RED}Invalid width! "
                        f"Must be between 9 and 45.{Colors.END}")
                    time.sleep(1)
            except ValueError:
                pass
        elif choice == "3":
            try:
                val = get_input("Enter new HEIGHT (7-45)")
                if val.isdigit() and 7 <= int(val) <= 45:
                    config["HEIGHT"] = val
                else:
                    print(
                        f"{Colors.RED}Invalid height! "
                        f"Must be between 7 and 45.{Colors.END}")
                    time.sleep(1)
            except ValueError:
                pass
        elif choice == "4":
            val = get_input("Enter Entry coordinates (x,y)")
            try:
                parts = val.split(',')
                if (len(parts) == 2 and parts[0].isdigit() and
                        parts[1].isdigit()):
                    config["ENTRY"] = val
                else:
                    print(f"{Colors.RED}Invalid format. Use x,y{Colors.END}")
                    time.sleep(1)
            except ValueError:
                pass
        elif choice == "5":
            val = get_input("Enter Exit coordinates (x,y)")
            try:
                parts = val.split(',')
                if (len(parts) == 2 and parts[0].isdigit() and
                        parts[1].isdigit()):
                    config["EXIT"] = val
                else:
                    print(
                        f"{Colors.RED}Invalid format. Use x,y "
                        f"(e.g. 10,9){Colors.END}")
                    time.sleep(1)
            except ValueError:
                pass
        elif choice == "6":
            current = str(config.get("PERFECT", "True")).lower() == "true"
            config["PERFECT"] = str(not current)
        elif choice == "0":
            return config, current_algo
        else:
            print(f"{Colors.RED}Invalid selection.{Colors.END}")
            time.sleep(0.5)


def redraw_maze(logic: MazeGenerator, show_solved: bool) -> None:
    """Redraw the maze in normal or solved mode.

    Parameters:
        logic: Maze generator instance.
        show_solved: If `True`, draw the solved path; otherwise draw base maze.
    """
    if show_solved:
        logic.print_solved(logic.visited_paths_global)
    else:
        logic.print_maze()


def generate_maze(config_file: str, current_algo: str,
                  current_config: dict[str, str]) -> tuple[MazeGenerator, str]:
    """Generate and render a maze from the current settings.

    Parameters:
        config_file: Base config file path.
        current_algo: Maze generation algorithm.
        current_config: Runtime config overrides.
    """
    try:
        logic, file_name = main(
            config_file, current_algo, config_overrides=current_config
        )
        clear_screen()
        logic.print_maze()
        return logic, file_name
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    first_time = True
    clear_screen()
    if len(sys.argv) > 2:
        clear_screen()
        print(f"{Colors.RED}[ERROR] Configuration file missing!{Colors.END}")
        print(f"{Colors.BOLD}Usage:{Colors.END}")
        print("    python3 a_maze_ing.py config.txt\n")
        exit(1)

    try:
        config_file = sys.argv[1]
    except IndexError:
        config_file = "config.txt"

    try:
        current_config = read_config(config_file)
    except Exception as e:
        print(f"{Colors.RED}Failed to read initial config: {e}{Colors.END}")
        exit(1)

    current_algo = "prims"
    show_solved = False
    logic = None
    file_name = None

    # Auto-generate maze on startup
    try:
        logic, file_name = generate_maze(
            config_file, current_algo, current_config
        )
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colors.YELLOW}[Interrupted]{Colors.END}")
    except Exception as e:
        print(f"""{Colors.RED}[Error running maze] {e}{Colors.END}
        {Colors.YELLOW}--Please change settings below--{Colors.END}""")
        try:
            input("Press Enter to continue...")
        except (KeyboardInterrupt, EOFError, AttributeError):
            exit()
    try:
        while True:
            print_main_menu(show_solved, has_maze=(logic is not None))
            try:
                choice = get_input("Enter choice")
            except (KeyboardInterrupt, EOFError):
                choice = "0"

            if choice == "1":
                first_time = True
                # Generate new maze
                show_solved = False
                try:
                    logic, file_name = generate_maze(
                        config_file, current_algo, current_config
                    )
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colors.YELLOW}[Interrupted]{Colors.END}")
                except Exception as e:
                    print(f"""{Colors.RED}[Error running maze] {e}{Colors.END}
            {Colors.YELLOW}--Please change it in the settings--{Colors.END}""")
                    try:
                        input("Press Enter to continue...")
                    except (KeyboardInterrupt, EOFError, AttributeError):
                        exit()

            elif choice == "2":
                # Settings
                current_config, current_algo = settings_loop(
                    current_config, current_algo, logic, show_solved
                )
                if logic:
                    redraw_maze(logic, show_solved)

            elif choice == "3":
                # Change maze color
                if logic is None:
                    print(f"{Colors.RED}No maze generated yet!{Colors.END}")
                    time.sleep(1)
                    continue
                clear_menu()
                print("""
        1) Yellow
        2) Red
        3) Green
        4) Blue
        5) Cyan
        6) Orange
        7) Dark Gray
    """)
                c_choice = get_input("Choose color (1-5)")
                colors = {
                    "1": f"{Colors.YELLOW}",
                    "2": f"{Colors.RED}",
                    "3": f"{Colors.GREEN}",
                    "4": f"{Colors.BLUE}",
                    "5": f"{Colors.CYAN}",
                    "6": f"{Colors.ORANGE}",
                    "7": f"{Colors.DARK_GRAY}"
                }
                if c_choice in colors:
                    logic.wall_color = colors[c_choice]
                redraw_maze(logic, show_solved)

            elif choice == "4":
                # Hide/Show solved
                if logic is None:
                    print(f"{Colors.RED}No maze generated yet!{Colors.END}")
                    time.sleep(1)
                    continue
                show_solved = not show_solved
                if show_solved:
                    try:
                        if first_time:
                            first_time = False
                            logic.bfs(flag=True)
                        logic.print_solved(logic.visited_paths_global)
                    except (KeyboardInterrupt, EOFError):
                        print(f"\n{Colors.YELLOW}[Interrupted]{Colors.END}")
                else:
                    redraw_maze(logic, show_solved)

            elif choice == "0":
                print(f"\n{Colors.YELLOW}Closing!...{Colors.END}")
                exit(0)

            else:
                print(f"{Colors.RED}Invalid selection.{Colors.END}")
                time.sleep(0.7)
                clear_screen()
                if logic is not None:
                    redraw_maze(logic, show_solved=False)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colors.YELLOW}Closing!...{Colors.END}")
        exit(0)
    except Exception as e:
        print(f"{Colors.RED}An error occurred: {e}{Colors.END}")
        exit(1)
