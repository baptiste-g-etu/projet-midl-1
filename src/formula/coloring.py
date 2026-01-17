# Colors for colorful printing of formulas (from user's terminal)
COLORS = [35, 36, 34, 32, 33, 31, 95, 96, 94, 92, 93, 91]
COLOR_RESET = "\x1b[39m"
COLORING = True


def color_level(level: int, text: str):
    """
    Colors the text with the appropriate colors for different levels of nested formulas.
    """
    return f"\x1b[{COLORS[level % len(COLORS)]}m{text}{COLOR_RESET}"
