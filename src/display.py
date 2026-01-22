# Colors for colorful printing of formulas (from user's terminal)
from enum import Enum

COLORS = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
COLORS_DEPTH = [35, 36, 34, 32, 33, 31, 95, 96, 94, 92, 93, 91]
COLOR_RESET = "\x1b[39m"


# Coloring for formulas
class Coloring(Enum):
    # Disable coloring
    NOT_COLORED = 0
    # Color by syntax
    SYNTAX = 1
    # Color by depth of formula
    DEPTH = 2


COLORING = Coloring.SYNTAX
PRINTING = True


def color(color: int, text: str):
    """
    Colors the text with the associated color from the user terminal.
    """
    if "COLORING" not in globals():
        globals()["COLORING"] = Coloring.SYNTAX
    coloring: Coloring = globals()["COLORING"]
    if coloring == Coloring.NOT_COLORED:
        return text
    else:
        return f"\x1b[{COLORS[color % len(COLORS)]}m{text}{COLOR_RESET}"


def color_by_depth(level: int, text: str):
    """
    Colors the text with the appropriate colors for different levels of nested formulas.
    """
    return f"\x1b[{COLORS_DEPTH[level % len(COLORS_DEPTH)]}m{text}{COLOR_RESET}"


def show(string: str):
    if PRINTING:
        print(string)
