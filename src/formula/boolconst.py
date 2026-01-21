from typing import Callable, Iterator, Self

from display.coloring import COLORING, color

from .types import LogicFormula
from .variable import Variable


class BoolConst(LogicFormula):
    """
    Boolean constants (True or False).
    """

    col = 3

    def __init__(self, const: bool) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_colored__(self):
        return color(self.col, "⊤" if self.const else "⊥")

    def __iter__(self) -> Iterator[Variable]:
        return iter([])

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__()
        else:
            return "⊤" if self.const else "⊥"

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(self)
