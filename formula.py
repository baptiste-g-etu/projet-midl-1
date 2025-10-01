"""
Base types for the project.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Self


# Types which are arithmetic expressions (usually ArithExpressions combined with arithmetic operators)
type ArithExpression = Variable | IntegerConst | ArithOp
# Types which output a logic formula (usually LogicFormulas combined with logic operators)
type LogicFormula = Comp | Quantifier | BoolConst | BoolOp


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

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare booleans")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare booleans")


class ArithOpType(StrEnum):
    SUM = "+"
    SUB = "-"
    PROD = "×"
    # DIV = "/" # Division isn’t supported


@dataclass
class ArithOp:
    expr1: ArithExpression
    boolop: ArithOpType
    expr2: ArithExpression

    def __repr__(self) -> str:
        # TODO Add parenthesis
        return f"{self.expr1} {self.boolop} {self.expr2}"

    def __lt__(self, rhs: Any):
        return Comp(self, CompType.LOWER_THAN, rhs)
    
    def __add__(self, rhs: ArithExpression | int):
        return ArithOp(self, ArithOpType.SUM, into_arith_expr(rhs))
    
    def __radd__(self, lhs: ArithExpression | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUM, self)
    
    def __sub__(self, rhs: ArithExpression | int):
        return ArithOp(self, ArithOpType.SUB, into_arith_expr(rhs))
    
    def __rsub__(self, lhs: ArithExpression | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUB, self)
    
    def __mul__(self, rhs: ArithExpression | int):
        return ArithOp(self, ArithOpType.PROD, into_arith_expr(rhs))
    
    def __rmul__(self, lhs: ArithExpression | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.PROD, self)
    # TODO Define __or__ and __and__ for the special case where a < b + 1 | 1 + c < d


class CompType(StrEnum):
    LOWER_THAN = "<"
    EQUAL = "="

    def __repr__(self):
        return self

    def __call__(self) -> Self:
        return self


@dataclass
class Comp:
    expr1: ArithExpression
    comp: CompType
    expr2: ArithExpression

    def __init__(
        self, expr1: ArithExpression, comp: CompType, expr2: ArithExpression
    ) -> None:
        self.expr1 = into_arith_expr(expr1)
        self.comp = comp
        self.expr2 = into_arith_expr(expr2)

    def __repr__(self) -> str:
        return f"{self.expr1} {self.comp} {self.expr2}"

    # TODO Maybe implement a < b < c, for example as (a < b) and (b < c)
    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare comparisons")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare comparisons")

    def __or__(self, rhs: LogicFormula) -> BoolOp:
        return BoolOp(self, BoolOpType.DISJ, into_logic_formula(rhs))

    def __ror__(self, lhs: LogicFormula) -> BoolOp:
        return BoolOp(into_logic_formula(lhs), BoolOpType.DISJ, self)

    def __and__(self, rhs: LogicFormula) -> LogicFormula:
        return BoolOp(self, BoolOpType.CONJ, into_logic_formula(rhs))

    def __rand__(self, lhs: LogicFormula) -> LogicFormula:
        return BoolOp(into_logic_formula(lhs), BoolOpType.CONJ, self)


@dataclass
class Variable:
    name: str

    def __repr__(self) -> str:
        return self.name

    def __add__(self, rhs: ArithExpression | int):
        return ArithOp(self, ArithOpType.SUM, into_arith_expr(rhs))

    def __radd__(self, lhs: ArithExpression | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUM, self)

    def __sub__(self, rhs: ArithExpression | int):
        return ArithOp(self, ArithOpType.SUB, into_arith_expr(rhs))

    def __rsub__(self, lhs: ArithExpression | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUB, self)

    def __mul__(self, rhs: ArithExpression | int):
        return ArithOp(self, ArithOpType.PROD, into_arith_expr(rhs))

    def __rmul__(self, lhs: ArithExpression | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.PROD, self)

    def __lt__(self, rhs:  ArithExpression | int) -> Comp:
        return Comp(self, CompType.LOWER_THAN, into_arith_expr(rhs))

    def __gt__(self, rhs: ArithExpression | int) -> Comp:
        return Comp(into_arith_expr(rhs), CompType.LOWER_THAN, self)

    # TODO lower equal ?

    def __eq__(self, rhs: ArithExpression | int) -> Comp:  # type: ignore because __eq__ is supposed to always return a bool
        return Comp(self, CompType.EQUAL, into_arith_expr(rhs))


@dataclass
class BoolConst:
    const: bool

    def __repr__(self) -> str:
        return "⊤" if self.const else "⊥"

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot use comparison operators on boolean constants")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot use comparison operators on boolean constants")


@dataclass
class IntegerConst:
    const: int

    def __repr__(self) -> str:
        return str(self.const)

    def __lt__(self, rhs: Any):
        return Comp(self, CompType.LOWER_THAN, rhs)


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

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot use comparison operators on quantifiers")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot use comparison operators on quantifiers")


@dataclass
class Not:
    formula: LogicFormula

    def __repr__(self) -> str:
        return f"¬{self.formula}"


@dataclass
class BoolOpBuilder:
    op: BoolOpType

    def __call__(self, formula1: LogicFormula, formula2: LogicFormula) -> BoolOp:
        return BoolOp(formula1, self.op, formula2)


@dataclass
class ArithOpBuilder:
    op: ArithOpType

    def __call__(self, formula1: ArithExpression, formula2: ArithExpression) -> ArithOp:
        return ArithOp(formula1, self.op, formula2)


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
class CompBuilder:
    comp: CompType

    def __call__(self, expr1: ArithExpression, expr2: ArithExpression) -> Comp:
        return Comp(expr1, self.comp, expr2)


def into_arith_expr(var: Any) -> ArithExpression:
    """
    Converts (almost) anything into an ArithExpression.

    This is useful to allow, for example `Variable("a") < 1` without having to type `Variable("a") < IntegerConst(1)`.
    """
    if isinstance(var, int):
        return IntegerConst(var)
    elif isinstance(var, str):
        return Variable(var)
    else:
        if not isinstance(var, ArithExpression.__value__):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into ArithExpression"
            )
        return var


def into_logic_formula(var: Any) -> LogicFormula:
    """
    Converts (almost) anything into a LogicFormula.

    This is useful to allow, for example `forall.a(True)` without having to type `forall.a(BoolConst(True))`.
    """
    if isinstance(var, bool):
        return BoolConst(var)
    else:
        if not isinstance(var, LogicFormula.__value__):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into LogicFormula"
            )
        return var
