from dataclasses import dataclass
from enum import StrEnum
from typing import Self


type ArithExpression = Variable | Comp
type LogicFormula = Quantifier | BoolConst


class BoolOpType(StrEnum):
    CONJ = "∧"
    DISJ = "∨"


@dataclass
class BoolOp:
    formula1: LogicFormula
    boolop: BoolOpType
    formula2: LogicFormula

    def __repr__(self) -> str:
        # TODO Add parenthesis
        return f"{self.formula1} {self.boolop} {self.formula2}"


@dataclass
class BoolOpBuilder:
    comp: BoolOpType

    def __call__(self, formula1: LogicFormula, formula2: LogicFormula) -> BoolOp:
        return BoolOp(formula1, self.comp, formula2)


# Because the Python bitwise OR has higher priority than the comparison operators,
# we need to invert the operator priority afterwards.
#
# For example :
# a > b | c > d is evaluated as a > (b | c) > d (because of Python),
# then (b | c) is translated into IncompleteFormula(b, |, c),
# then a > (b | c) is translated into IncompleteFormula(a > b, |, c),
# then IncompleteFormula(a > b, |, c) > d is translated into a > b | c > d
#
# a > b | c > d | e > f = a > (b | c) > (d | e) > f = ((a > b) | c) > (d | e) > f = ((a > b) | c > d) ( | e) > f
@dataclass
class IncompleteFormula:
    expr1: ArithExpression
    op: BoolOpType
    expr2: ArithExpression

    def __repr__(self) -> str:
        return f"INCOMPLETE({{}} {self.expr1} {self.op} {self.expr2} {{}})"


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


@dataclass
class BoolConst:
    const: bool

    def __repr__(self) -> str:
        return "⊤" if self.const else "⊥"


class QuantifierType(StrEnum):
    FORALL = "∀"
    EXISTS = "∃"

    def __repr__(self):
        return self


@dataclass
class Quantifier:
    quantifier: QuantifierType
    variable: Variable
    formula: LogicFormula

    def __repr__(self) -> str:
        inner_is_quantif = isinstance(self.formula, Quantifier)
        return f"{self.quantifier}{self.variable}.{'' if inner_is_quantif else '('}{self.formula}{'' if inner_is_quantif else ')'}"


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


@dataclass
class Not:
    formula: LogicFormula

    def __repr__(self) -> str:
        return f"¬{self.formula}"
