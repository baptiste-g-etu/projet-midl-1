from enum import StrEnum
from typing import Callable, Iterator, Self

from .coloring import COLORING, color_level
from .types import (
    IntoLogicFormula,
    LogicFormula,
    into_logic_formula,
)
from .variable import IntoVariable, Variable, into_variable


class QuantifierType(StrEnum):
    FORALL = "∀"
    EXISTS = "∃"

    def __repr__(self):
        return self

    def __call__(self) -> Self:
        return self


class Quantifier(LogicFormula):
    def __init__(
        self,
        quantifier: QuantifierType,
        variable: IntoVariable,
        formula: IntoLogicFormula,
    ) -> None:
        self.quantifier = quantifier
        self.variable = into_variable(variable)
        self.formula = into_logic_formula(formula)

    def __repr_colored__(self, level: int):
        formula = self.formula.__repr_colored__(
            level + (1 if not isinstance(self.formula, Quantifier) else 0)
        )
        if not isinstance(self.formula, Quantifier):
            formula = f"{color_level(level, '(')}{formula}{color_level(level, ')')}"
        return f"{color_level(level, self.quantifier)}{self.variable.__repr_colored__(level)}{color_level(level, '.')}{formula}"

    def __iter__(self) -> Iterator[Variable]:
        # TODO self.variable is in the formula ???
        return iter(self.formula)

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            formula = str(self.formula)
            if not isinstance(self.formula, Quantifier):
                formula = f"({formula})"
            return f"{self.quantifier}{self.variable}.{formula}"

    def map_formula(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(
            Quantifier(self.quantifier, self.variable, self.formula.map_formula(fn))
        )


class QuantifierBuilder:
    def __init__(self, quantif: QuantifierType) -> None:
        self.quantifier = quantif
        self.variables: list[Variable] = []

    def __call__(self, formula: LogicFormula) -> Quantifier:
        match len(self.variables):
            case 0:
                raise ValueError(
                    "Tried to call a Quantifier to create a formula without any variable"
                )

            case 1:
                return Quantifier(self.quantifier, self.variables.pop(0), formula)

            # If there are multiple variables, we perform a recursive formula containing each quantifier + variable
            case _:
                return Quantifier(self.quantifier, self.variables.pop(0), self(formula))

    def __getattr__(self, name: str) -> "QuantifierBuilder":
        # Forced to clone the class so builders can be reused (else they would be polluted by older or parallel uses)
        new = QuantifierBuilder(self.quantifier)
        new.variables = self.variables.copy()
        variable = Variable(name)
        if variable in self.variables:
            raise ValueError(
                f'A variable named "{name}" is already defined in this quantifier chain'
            )
        new.variables.append(variable)
        return new
