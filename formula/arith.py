from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from formula.logic import BoolOpType, IncompleteFormula


type ArithExpression = Variable | Comp


@dataclass
class Variable:
    name: str

    def __repr__(self) -> str:
        return self.name

    def __or__(self, rhs: Self) -> IncompleteFormula:
        return IncompleteFormula(self, BoolOpType.DISJ, rhs)
    
    def __and__(self, rhs: Self) -> IncompleteFormula:
        return IncompleteFormula(self, BoolOpType.CONJ, rhs)


class CompType(StrEnum):
    LOWER_THAN = "<"
    EQUAL = "="

    def __repr__(self):
        return self


@dataclass
class Comp:
    expr1: ArithExpression
    comp: CompType
    expr2: ArithExpression

    def __repr__(self) -> str:
        return f"{self.expr1} {self.comp} {self.expr2}"


@dataclass
class CompBuilder:
    comp: CompType

    def __call__(self, expr1: ArithExpression, expr2: ArithExpression) -> Comp:
        return Comp(expr1, self.comp, expr2)
