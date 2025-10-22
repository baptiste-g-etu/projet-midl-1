from typing import Callable
from .coloring import COLORING, color_level
from .types import (
    IntoLogicFormula,
    LogicFormula,
    into_logic_formula,
)
from .variable import Variable


class Not(LogicFormula):
    def __init__(self, formula: IntoLogicFormula) -> None:
        self.formula = into_logic_formula(formula)

    def __repr_colored__(self, level: int):
        return f"{color_level(level, '¬(')}{self.formula.__repr_colored__(level + 1)}{color_level(level, ')')}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.formula

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"¬({self.formula})"

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(Not(self.formula.map_formula(fn)))
