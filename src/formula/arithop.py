from enum import StrEnum
from typing import Self
from .coloring import COLORING, color_level
from .types import ArithExpression, IntoArithExpression, into_arith_expr
from .variable import Variable


class ArithOpType(StrEnum):
    SUM = "+"
    SUB = "-"
    PROD = "×"
    # DIV = "/" # Division isn’t supported

    def __call__(self) -> Self:
        return self


class ArithOp(ArithExpression):
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

    def __repr_colored__(self, level: int) -> str:
        expr1 = self.expr1.__repr_colored__(level + 1)
        expr2 = self.expr2.__repr_colored__(level + 1)
        if isinstance(self.expr1, ArithOp) and self.expr1.arithop == ArithOpType.SUM:
            expr1 = f"{color_level(level + 1, '(')}{expr1}{color_level(level + 1, ')')}"
        if isinstance(self.expr2, ArithOp) and self.expr2.arithop == ArithOpType.SUM:
            expr2 = f"{color_level(level + 1, '(')}{expr2}{color_level(level + 1, ')')}"
        return f"{expr1} {color_level(level, self.arithop)} {expr2}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.expr1 or variable in self.expr2

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            expr1 = f"{self.expr1}"
            expr2 = f"{self.expr2}"
            if (
                isinstance(self.expr1, ArithOp)
                and self.expr1.arithop == ArithOpType.SUM
            ):
                expr1 = f"({expr1})"
            if (
                isinstance(self.expr2, ArithOp)
                and self.expr2.arithop == ArithOpType.SUM
            ):
                expr2 = f"({expr2})"
            return f"{expr1} {self.arithop} {expr2}"


class ArithOpBuilder:
    from .arithop import ArithOp, ArithOpType

    def __init__(self, op: ArithOpType) -> None:
        self.op = op

    def __call__(self, formula1: ArithExpression, formula2: ArithExpression) -> ArithOp:
        from .arithop import ArithOp

        return ArithOp(formula1, self.op, formula2)
