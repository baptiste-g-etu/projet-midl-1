# Colors for colorful printing of formulas (from user's terminal)
COLORS = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
COLOR_RESET = "\x1b[39m"
COLORING = True
PRINTING = True


def color(level: int, text: str):
    """
    Colors the text with the appropriate colors for different levels of nested formulas.
    """
    return f"\x1b[{COLORS[level % len(COLORS)]}m{text}{COLOR_RESET}"


def show(string: str):
    if PRINTING:
        print(string)
