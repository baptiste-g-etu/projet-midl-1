from enum import StrEnum
from itertools import chain
from typing import Iterator, Self

from display import color, color_by_depth

from .types import ArithExpression, IntoArithExpression, into_arith_expr
from .variable import IntoVariable, Variable, into_variable


class ArithOpType(StrEnum):
    SUM = "+"
    SUB = "-"
    PROD = "×"
    # DIV = "/" # Division isn’t supported

    def __call__(self) -> Self:
        return self


class ArithOp(ArithExpression):
    """
    Arithmetic operations (addition, substraction and product).
    """

    col = 4

    def __init__(
        self,
        expr1: IntoArithExpression,
        arithop: ArithOpType,
        expr2: IntoArithExpression,
    ):
        self.expr1 = into_arith_expr(expr1)
        self.arithop = arithop
        self.expr2 = into_arith_expr(expr2)

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return (
            self.expr1.is_syntaxically_eq(rhs.expr1)
            and self.arithop == rhs.arithop
            and self.expr2.is_syntaxically_eq(rhs.expr2)
        )

    def __repr_syntax__(self) -> str:
        expr1 = repr(self.expr1)
        expr2 = repr(self.expr2)
        if isinstance(self.expr1, ArithOp) and self.expr1.arithop in [
            ArithOpType.SUM,
            ArithOpType.SUB,
        ]:
            expr1 = f"{color(self.col, '(')}{expr1}{color(self.col, ')')}"
        if isinstance(self.expr2, ArithOp) and self.expr2.arithop in [
            ArithOpType.SUM,
            ArithOpType.SUB,
        ]:
            expr2 = f"{color(self.col, '(')}{expr2}{color(self.col, ')')}"
        if self.arithop == ArithOpType.PROD:
            return f"{expr1}{expr2}"
        else:
            return f"{expr1} {color(self.col, self.arithop)} {expr2}"

    def __repr_depth__(self, level: int) -> str:
        expr1 = self.expr1.__repr_depth__(level)
        expr2 = self.expr2.__repr_depth__(level)
        if isinstance(self.expr1, ArithOp) and self.expr1.arithop in [
            ArithOpType.SUM,
            ArithOpType.SUB,
        ]:
            expr1 = f"{color_by_depth(level, '(')}{expr1}{color_by_depth(level, ')')}"
        if isinstance(self.expr2, ArithOp) and self.expr2.arithop in [
            ArithOpType.SUM,
            ArithOpType.SUB,
        ]:
            expr2 = f"{color_by_depth(level, '(')}{expr2}{color_by_depth(level, ')')}"
        if self.arithop == ArithOpType.PROD:
            return f"{expr1}{expr2}"
        else:
            return f"{expr1} {color_by_depth(level, self.arithop)} {expr2}"

    def __iter__(self) -> Iterator[Variable]:
        variable_list = list(set(chain(iter(self.expr1), iter(self.expr2))))
        variable_list.sort(key=lambda v: v.name)
        return iter(variable_list)

    def replace(self, variable: IntoVariable, expr: IntoArithExpression) -> "ArithOp":
        return ArithOp(
            self.expr1.replace(into_variable(variable), expr),
            self.arithop,
            self.expr2.replace(into_variable(variable), expr),
        )


class ArithOpBuilder:
    from .arithop import ArithOp, ArithOpType

    def __init__(self, op: ArithOpType) -> None:
        self.op = op

    def __call__(self, formula1: ArithExpression, formula2: ArithExpression) -> ArithOp:
        from .arithop import ArithOp

        return ArithOp(formula1, self.op, formula2)
