from enum import StrEnum
from itertools import chain
from typing import Any, Callable, Iterator, Self

from display.coloring import COLORING, color

from .types import (
    IntoLogicFormula,
    LogicFormula,
    into_canonical_logic_formula,
)
from .variable import Variable


class BoolOpType(StrEnum):
    CONJ = "∧"
    DISJ = "∨"

    def __call__(self) -> Self:
        return self


class BoolOp(LogicFormula):
    """
    Boolean operations (conjunctions and disjunctions).
    """

    def __init__(
        self, formula1: IntoLogicFormula, boolop: BoolOpType, formula2: IntoLogicFormula
    ) -> None:
        self.formula1 = into_canonical_logic_formula(formula1)
        self.boolop = boolop
        self.formula2 = into_canonical_logic_formula(formula2)

        match self.boolop:
            case BoolOpType.DISJ:
                self.col = 2
            case BoolOpType.CONJ:
                self.col = 1

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return (
            self.formula1.is_syntaxically_eq(rhs.formula1)
            and self.boolop == rhs.boolop
            and self.formula2.is_syntaxically_eq(rhs.formula2)
        )

    # TODO Find a way to factor the code of __repr__ and __repr_colored__ on all types
    def __repr__(self) -> str:
        from .quantifier import Quantifier

        if COLORING:
            return self.__repr_colored__()
        else:
            formula1 = str(self.formula1)
            formula2 = str(self.formula2)
            if isinstance(self.formula1, BoolOp) or isinstance(
                self.formula1, Quantifier
            ):
                formula1 = f"({formula1})"
            if isinstance(self.formula2, BoolOp) or isinstance(
                self.formula1, Quantifier
            ):
                formula2 = f"({formula2})"
            return f"{formula1} {self.boolop} {formula2}"

    def __repr_colored__(self) -> str:
        from .quantifier import Quantifier

        formula1 = repr(self.formula1)
        formula2 = repr(self.formula2)
        if isinstance(self.formula1, BoolOp) or isinstance(self.formula1, Quantifier):
            formula1 = f"{color(self.formula1.col, '(')}{formula1}{color(self.formula1.col, ')')}"
        if isinstance(self.formula2, BoolOp) or isinstance(self.formula2, Quantifier):
            formula2 = f"{color(self.formula2.col, '(')}{formula2}{color(self.formula2.col, ')')}"
        return f"{formula1} {color(self.col, self.boolop)} {formula2}"

    def __iter__(self) -> Iterator[Variable]:
        variable_list = list(set(chain(iter(self.formula1), iter(self.formula2))))
        variable_list.sort(key=lambda v: v.name)
        return iter(variable_list)

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare booleans")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare booleans")

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(
            BoolOp(
                self.formula1.map_formula(fn),
                self.boolop,
                self.formula2.map_formula(fn),
            )
        )


class BoolOpBuilder:
    def __init__(self, op: BoolOpType) -> None:
        self.op = op

    def __call__(
        self, formula1: IntoLogicFormula, formula2: IntoLogicFormula
    ) -> BoolOp:
        return BoolOp(formula1, self.op, formula2)
