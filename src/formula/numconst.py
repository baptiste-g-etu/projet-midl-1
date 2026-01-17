from typing import Iterator, Self

from .coloring import COLORING, color_level
from .types import ArithExpression, IntoArithExpression
from .variable import IntoVariable, Variable


class NumConst(ArithExpression):
    def __init__(self, const: int | float) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_colored__(self, level: int):
        return color_level(level, str(self.const))

    def __iter__(self) -> Iterator[Variable]:
        return iter([])

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return str(self.const)

    def replace(self, variable: IntoVariable, expr: IntoArithExpression) -> Self:
        return self
