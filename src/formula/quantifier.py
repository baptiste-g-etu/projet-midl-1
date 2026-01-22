from enum import StrEnum
from typing import Callable, Iterator, Self

from display import color, color_by_depth

from .types import (
    IntoLogicFormula,
    LogicFormula,
    into_canonical_logic_formula,
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
    """
    Logical quantifier (universal and existential).
    """

    col = 5

    def __init__(
        self,
        quantifier: QuantifierType,
        variable: IntoVariable,
        formula: IntoLogicFormula,
    ) -> None:
        self.quantifier = quantifier
        self.variable = into_variable(variable)
        self.formula = into_canonical_logic_formula(formula)

    def __repr_syntax__(self):
        formula = repr(self.formula)
        if not isinstance(self.formula, Quantifier):
            formula = (
                f"{color(self.formula.col, '(')}{formula}{color(self.formula.col, ')')}"
            )
        return f"{color(self.col, self.quantifier)}{self.variable}{color(self.col, '.')}{formula}"

    def __repr_depth__(self, level: int):
        formula = self.formula.__repr_depth__(
            level + (1 if not isinstance(self.formula, Quantifier) else 0)
        )
        if not isinstance(self.formula, Quantifier):
            formula = (
                f"{color_by_depth(level, '(')}{formula}{color_by_depth(level, ')')}"
            )
        return f"{color_by_depth(level, self.quantifier)}{self.variable.__repr_depth__(level)}{color_by_depth(level, '.')}{formula}"

    def __iter__(self) -> Iterator[Variable]:
        # TODO self.variable is in the formula ???
        return iter(self.formula)

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
