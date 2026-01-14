from enum import StrEnum
from itertools import chain
from typing import Any, Callable, Iterator, Self

from .coloring import COLORING, color_level
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
    def __init__(
        self, formula1: IntoLogicFormula, boolop: BoolOpType, formula2: IntoLogicFormula
    ) -> None:
        self.formula1 = into_canonical_logic_formula(formula1)
        self.boolop = boolop
        self.formula2 = into_canonical_logic_formula(formula2)

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
            return self.__repr_colored__(0)
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

    def __repr_colored__(self, level: int) -> str:
        from .quantifier import Quantifier

        formula1 = self.formula1.__repr_colored__(level + 1)
        formula2 = self.formula2.__repr_colored__(level + 1)
        if isinstance(self.formula1, BoolOp) or isinstance(self.formula1, Quantifier):
            formula1 = (
                f"{color_level(level + 1, '(')}{formula1}{color_level(level + 1, ')')}"
            )
        if isinstance(self.formula2, BoolOp) or isinstance(self.formula2, Quantifier):
            formula2 = (
                f"{color_level(level + 1, '(')}{formula2}{color_level(level + 1, ')')}"
            )
        return f"{formula1} {color_level(level, self.boolop)} {formula2}"

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
