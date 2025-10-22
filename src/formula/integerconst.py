from typing import Self
from .coloring import COLORING, color_level
from .types import ArithExpression
from .variable import Variable


class IntegerConst(ArithExpression):
    def __init__(self, const: int) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_colored__(self, level: int):
        return color_level(level, str(self.const))

    def __contains__(self, variable: Variable) -> bool:
        return False

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return str(self.const)
