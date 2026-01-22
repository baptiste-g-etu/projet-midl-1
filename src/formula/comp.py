from enum import StrEnum
from itertools import chain
from typing import Callable, Iterator, Self

from display import color, color_by_depth

from .types import IntoArithExpression, LogicFormula, into_arith_expr
from .variable import Variable


class CompType(StrEnum):
    LOWER_THAN = "<"
    EQUAL = "="

    def __repr__(self):
        return self

    def __call__(self) -> Self:
        return self


class Comp(LogicFormula):
    """
    Comparison (equality and lower-than).
    """

    col = 3

    def __init__(
        self, expr1: IntoArithExpression, comp: CompType, expr2: IntoArithExpression
    ) -> None:
        self.expr1 = into_arith_expr(expr1)
        self.comp = comp
        self.expr2 = into_arith_expr(expr2)

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return (
            self.expr1.is_syntaxically_eq(rhs.expr1)
            and self.comp == rhs.comp
            and self.expr2.is_syntaxically_eq(rhs.expr2)
        )

    def __repr_syntax__(self) -> str:
        return f"{self.expr1} {color(self.col, self.comp)} {self.expr2}"

    def __repr_depth__(self, level: int) -> str:
        return f"{self.expr1.__repr_depth__(level)} {color_by_depth(level, self.comp)} {self.expr2.__repr_depth__(level)}"

    def __iter__(self) -> Iterator[Variable]:
        variable_list = list(set(chain(iter(self.expr1), iter(self.expr2))))
        variable_list.sort(key=lambda v: v.name)
        return iter(variable_list)

    def __bool__(self):
        """
        Bool implementation so Python isn’t messed up with eq mismatch.
        """
        return self.expr1.is_syntaxically_eq(self.expr2)

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(self)

    # TODO Maybe implement a < b < c, for example as (a < b) and (b < c)


class CompBuilder:
    def __init__(self, comp: CompType) -> None:
        self.comp = comp

    def __call__(self, expr1: IntoArithExpression, expr2: IntoArithExpression) -> Comp:
        return Comp(into_arith_expr(expr1), self.comp, into_arith_expr(expr2))
