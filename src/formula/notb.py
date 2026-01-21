from typing import Callable, Iterator

from display.coloring import COLORING, color

from .boolconst import BoolConst
from .types import (
    IntoLogicFormula,
    LogicFormula,
    into_canonical_logic_formula,
)
from .variable import Variable


class Not(LogicFormula):
    """
    Logical negation.
    """

    col = 9

    def __init__(self, formula: IntoLogicFormula) -> None:
        self.formula = into_canonical_logic_formula(formula)

    def __repr_colored__(self) -> str:
        formula = repr(self.formula)
        if not (isinstance(self.formula, Not) or isinstance(self.formula, BoolConst)):
            formula = (
                f"{color(self.formula.col, '(')}{formula}{color(self.formula.col, ')')}"
            )
        return f"¬{formula}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__()

        formula = repr(self.formula)
        if not (isinstance(self.formula, Not) or isinstance(self.formula, BoolConst)):
            formula = f"({self.formula})"
        return f"¬{formula}"

    def __iter__(self) -> Iterator[Variable]:
        return iter(self.formula)

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(Not(self.formula.map_formula(fn)))
