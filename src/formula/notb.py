from typing import Callable, Iterator

from display import color, color_by_depth

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

    def __repr_syntax__(self) -> str:
        formula = repr(self.formula)
        if not (isinstance(self.formula, Not) or isinstance(self.formula, BoolConst)):
            formula = (
                f"{color(self.formula.col, '(')}{formula}{color(self.formula.col, ')')}"
            )
        return f"¬{formula}"

    def __repr_depth__(self, level: int):
        if isinstance(self.formula, Not) or isinstance(self.formula, BoolConst):
            return f"{color_by_depth(level, '¬')}{self.formula.__repr_depth__(level)}"
        else:
            return f"{color_by_depth(level + 1, '¬(')}{self.formula.__repr_depth__(level + 1)}{color(level + 1, ')')}"

    def __iter__(self) -> Iterator[Variable]:
        return iter(self.formula)

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(Not(self.formula.map_formula(fn)))
