from typing import Iterator, Self

from display import color, color_by_depth

from .types import ArithExpression, IntoArithExpression
from .variable import IntoVariable, Variable


class NumConst(ArithExpression):
    """
    Number constant (float or int).
    """

    col = 6

    def __init__(self, const: int | float) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_syntax__(self):
        return color(self.col, str(self.const))

    def __repr_depth__(self, level: int):
        return color_by_depth(level, str(self.const))

    def __iter__(self) -> Iterator[Variable]:
        return iter([])

    def replace(self, variable: IntoVariable, expr: IntoArithExpression) -> Self:
        return self
