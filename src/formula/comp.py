from enum import StrEnum
from typing import Callable, Self
from .coloring import COLORING, color_level
from .types import LogicFormula, IntoArithExpression, into_arith_expr
from .variable import Variable


class CompType(StrEnum):
    LOWER_THAN = "<"
    EQUAL = "="

    def __repr__(self):
        return self

    def __call__(self) -> Self:
        return self


class Comp(LogicFormula):
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

    def __repr_colored__(self, level: int) -> str:
        return f"{self.expr1.__repr_colored__(level)} {color_level(level, self.comp)} {self.expr2.__repr_colored__(level)}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"{self.expr1} {self.comp} {self.expr2}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.expr1 or variable in self.expr2

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
