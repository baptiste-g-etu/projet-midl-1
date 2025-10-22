from typing import Callable, Self
from .coloring import COLORING, color_level
from .types import LogicFormula
from .variable import Variable


class BoolConst(LogicFormula):
    def __init__(self, const: bool) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_colored__(self, level: int):
        return color_level(level, "⊤" if self.const else "⊥")

    def __contains__(self, variable: Variable) -> bool:
        return False

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return "⊤" if self.const else "⊥"

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(self)
