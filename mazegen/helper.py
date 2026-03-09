import os

decor = "─" * 70

# ANSI colors for professional look


class Colors:
    """ANSI color codes used by the terminal UI."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DARK_GRAY = '\033[90m'
    ORANGE = '\033[38;5;208m'
    WHITE = '\033[97m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear')


def clear_menu() -> None:
    """Clear terminal output from the cursor to the end."""
    print("\033[J", end="")


def print_main_menu(show_solved: bool = False, has_maze: bool = False) -> None:
    """Print the main menu.

    Args:
        show_solved: Whether solved mode is currently shown.
        has_maze: If `True`, clear only the menu area.
    """
    if has_maze:
        clear_menu()
    else:
        clear_screen()
        print(f"""{Colors.RED}
 ▄▄▄       ███▄ ▄███▓ ▄▄▄      ▒███████▒▓█████  ██▓ ███▄    █   ▄████
▒████▄    ▓██▒▀█▀ ██▒▒████▄    ▒ ▒ ▒ ▄▀░▓█   ▀ ▓██▒ ██ ▀█   █  ██▒ ▀█▒
▒██  ▀█▄  ▓██    ▓██░▒██  ▀█▄  ░ ▒ ▄▀▒░ ▒███   ▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
░██▄▄▄▄██ ▒██    ▒██ ░██▄▄▄▄██   ▄▀▒   ░▒▓█  ▄ ░██░▓██▒  ▐▌██▒░▓█  ██▓
 ▓█   ▓██▒▒██▒   ░██▒ ▓█   ▓██▒▒███████▒░▒████▒░██░▒██░   ▓██░░▒▓███▀▒
 ▒▒   ▓▒█░░ ▒░   ░  ░ ▒▒   ▓▒█░░▒▒ ▓░▒░▒░░ ▒░ ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒
  ▒   ▒▒ ░░  ░      ░  ▒   ▒▒ ░░░▒ ▒ ░ ▒ ░ ░  ░ ▒ ░░ ░░   ░ ▒░  ░   ░
  ░   ▒   ░      ░     ░   ▒   ░ ░ ░ ░ ░   ░    ▒ ░   ░   ░ ░ ░ ░   ░
      ░  ░       ░         ░  ░  ░ ░       ░  ░ ░           ░       ░
                               ░{Colors.DARK_GRAY}
╔╗ ╦ ╦  ╔╦╗┌─┐┌─┐┬  ┬  ┌─┐┬┌─       ╔╦╗┌─┐┬   ┬ ┬┌─┐┬ ┬┌┬┐
╠╩╗╚╦╝   ║ └─┐├┤ │  │  ├─┤├┴┐  ───  ║║║├┤ │───│││├─┤├─┤│││
╚═╝ ╩    ╩ └─┘└─┘┴─┘┴─┘┴ ┴┴ ┴       ╩ ╩└─┘┴─┘ └┴┘┴ ┴┴ ┴┴ ┴{Colors.END}""")
    print(
        f"\n{Colors.BOLD}{Colors.RED}Main Menu:{Colors.END}"
    )
    print()
    print("   1 - Generate New Maze")
    print("   2 - Settings")
    print("   3 - Change Maze Color")
    print(f"   4 - {'Hide' if show_solved else 'Show'} Solved")
    print("   0 - Exit")
    print()
    print(f"{Colors.DARK_GRAY}{decor}{Colors.END}")


def print_settings_menu(
        config: dict[str, str],
        algo: str, has_maze: bool = False) -> None:
    """Print the settings menu.

    Args:
        config: Current maze configuration values.
        algo: Active algorithm name.
        has_maze: If `True`, clear only the menu area.
    """
    if has_maze:
        clear_menu()
    else:
        clear_screen()
        print(f"""{Colors.BLUE}
 ▄▄▄       ███▄ ▄███▓ ▄▄▄      ▒███████▒▓█████  ██▓ ███▄    █   ▄████
▒████▄    ▓██▒▀█▀ ██▒▒████▄    ▒ ▒ ▒ ▄▀░▓█   ▀ ▓██▒ ██ ▀█   █  ██▒ ▀█▒
▒██  ▀█▄  ▓██    ▓██░▒██  ▀█▄  ░ ▒ ▄▀▒░ ▒███   ▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
░██▄▄▄▄██ ▒██    ▒██ ░██▄▄▄▄██   ▄▀▒   ░▒▓█  ▄ ░██░▓██▒  ▐▌██▒░▓█  ██▓
 ▓█   ▓██▒▒██▒   ░██▒ ▓█   ▓██▒▒███████▒░▒████▒░██░▒██░   ▓██░░▒▓███▀▒
 ▒▒   ▓▒█░░ ▒░   ░  ░ ▒▒   ▓▒█░░▒▒ ▓░▒░▒░░ ▒░ ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒
  ▒   ▒▒ ░░  ░      ░  ▒   ▒▒ ░░░▒ ▒ ░ ▒ ░ ░  ░ ▒ ░░ ░░   ░ ▒░  ░   ░
  ░   ▒   ░      ░     ░   ▒   ░ ░ ░ ░ ░   ░    ▒ ░   ░   ░ ░ ░ ░   ░
      ░  ░       ░         ░  ░  ░ ░       ░  ░ ░           ░       ░
                               ░{Colors.DARK_GRAY}
╔╗ ╦ ╦  ╔╦╗┌─┐┌─┐┬  ┬  ┌─┐┬┌─       ╔╦╗┌─┐┬   ┬ ┬┌─┐┬ ┬┌┬┐
╠╩╗╚╦╝   ║ └─┐├┤ │  │  ├─┤├┴┐  ───  ║║║├┤ │───│││├─┤├─┤│││
╚═╝ ╩    ╩ └─┘└─┘┴─┘┴─┘┴ ┴┴ ┴       ╩ ╩└─┘┴─┘ └┴┘┴ ┴┴ ┴┴ ┴{Colors.END}""")
    print(
        f"\n{Colors.BOLD}{Colors.BLUE}Settings:{Colors.END}"
    )
    print()
    perfect_status = f"{Colors.GREEN}YES{Colors.END}" if str(config.get(
        "PERFECT", "True")).strip().lower() == "true"\
        else f"{Colors.RED}NO{Colors.END}"

    print(f"   1 - Algorithm: {Colors.YELLOW}{algo.upper()}{Colors.END}")
    print(
        f"   2 - Width:     {Colors.YELLOW}{config.get('WIDTH')}{Colors.END}")
    print(
        f"   3 - Height:    {Colors.YELLOW}{config.get('HEIGHT')}{Colors.END}")
    print(
        f"   4 - Entry:     {Colors.YELLOW}{config.get('ENTRY')}{Colors.END}")
    print(f"   5 - Exit:      {Colors.YELLOW}{config.get('EXIT')}{Colors.END}")
    print(f"   6 - Perfect:   {perfect_status}")
    print("   0 - Back")
    print()
    print(f"{Colors.DARK_GRAY}{decor}{Colors.END}")
