from typing import Callable, Iterator, Self

from display import color, color_by_depth

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

    def __repr_syntax__(self):
        return color(self.col, "⊤" if self.const else "⊥")

    def __repr_depth__(self, level: int):
        return color_by_depth(level, "⊤" if self.const else "⊥")

    def __iter__(self) -> Iterator[Variable]:
        return iter([])

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(self)
