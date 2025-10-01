"""
Base types for the project.
"""

from enum import StrEnum
from typing import Any, Self


# Types which are arithmetic expressions (usually ArithExpressions combined with arithmetic operators)
class ArithExpression:
    def __lt__(self, rhs: Any):
        return Comp(self, CompType.LOWER_THAN, rhs)

    def __gt__(self, rhs: Self | int):
        return Comp(into_arith_expr(rhs), CompType.LOWER_THAN, self)

    # TODO lower equal ?

    def __eq__(self, rhs: Self | int):  # type: ignore because __eq__ is supposed to always return a bool
        return Comp(self, CompType.EQUAL, into_arith_expr(rhs))

    def __add__(self, rhs: Self | int):
        return ArithOp(self, ArithOpType.SUM, into_arith_expr(rhs))

    def __radd__(self, lhs: Self | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUM, self)

    def __sub__(self, rhs: Self | int):
        return ArithOp(self, ArithOpType.SUB, into_arith_expr(rhs))

    def __rsub__(self, lhs: Self | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUB, self)

    def __mul__(self, rhs: Self | int):
        return ArithOp(self, ArithOpType.PROD, into_arith_expr(rhs))

    def __rmul__(self, lhs: Self | int):
        return ArithOp(into_arith_expr(lhs), ArithOpType.PROD, self)


# Types which output a logic formula (usually LogicFormulas combined with logic operators)
class LogicFormula:
    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __eq__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __or__(self, rhs: Self):
        return BoolOp(self, BoolOpType.DISJ, into_logic_formula(rhs))

    def __ror__(self, lhs: Self):
        return BoolOp(into_logic_formula(lhs), BoolOpType.DISJ, self)

    def __and__(self, rhs: Self):
        return BoolOp(self, BoolOpType.CONJ, into_logic_formula(rhs))

    def __rand__(self, lhs: Self):
        return BoolOp(into_logic_formula(lhs), BoolOpType.CONJ, self)


class BoolOpType(StrEnum):
    CONJ = "∧"
    DISJ = "∨"


class BoolOp(LogicFormula):
    def __init__(
        self, formula1: LogicFormula, boolop: BoolOpType, formula2: LogicFormula
    ) -> None:
        self.formula1 = into_logic_formula(formula1)
        self.boolop = boolop
        self.formula2 = into_logic_formula(formula2)

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


class ArithOp(ArithExpression):
    def __init__(
        self,
        expr1: ArithExpression,
        boolop: ArithOpType,
        expr2: ArithExpression,
    ):
        self.expr1 = into_arith_expr(expr1)
        self.boolop = boolop
        self.expr2 = into_arith_expr(expr2)

    def __repr__(self) -> str:
        # TODO Add parenthesis
        return f"{self.expr1} {self.boolop} {self.expr2}"


class CompType(StrEnum):
    LOWER_THAN = "<"
    EQUAL = "="

    def __repr__(self):
        return self

    def __call__(self) -> Self:
        return self


class Comp(ArithExpression):
    def __init__(
        self, expr1: ArithExpression, comp: CompType, expr2: ArithExpression
    ) -> None:
        self.expr1 = into_arith_expr(expr1)
        self.comp = comp
        self.expr2 = into_arith_expr(expr2)

    def __repr__(self) -> str:
        return f"{self.expr1} {self.comp} {self.expr2}"

    # TODO Maybe implement a < b < c, for example as (a < b) and (b < c)


class Variable(ArithExpression):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


class BoolConst(LogicFormula):
    def __init__(self, const: bool) -> None:
        self.const = const

    def __repr__(self) -> str:
        return "⊤" if self.const else "⊥"


class IntegerConst(ArithExpression):
    def __init__(self, const: int) -> None:
        self.const = const

    def __repr__(self) -> str:
        return str(self.const)


class QuantifierType(StrEnum):
    FORALL = "∀"
    EXISTS = "∃"

    def __repr__(self):
        return self


class Quantifier(LogicFormula):
    def __init__(
        self,
        quantifier: QuantifierType,
        variable: Variable,
        formula: LogicFormula,
    ) -> None:
        self.quantifier = quantifier
        self.variable = variable
        self.formula = into_logic_formula(formula)

    def __repr__(self) -> str:
        inner_is_quantif = isinstance(self.formula, Quantifier)
        return f"{self.quantifier}{self.variable}.{'' if inner_is_quantif else '('}{self.formula}{'' if inner_is_quantif else ')'}"


class Not(LogicFormula):
    def __init__(self, formula: LogicFormula) -> None:
        self.formula = into_logic_formula(formula)

    def __repr__(self) -> str:
        return f"¬{self.formula}"


class BoolOpBuilder:
    def __init__(self, op: BoolOpType) -> None:
        self.op = op

    def __call__(self, formula1: LogicFormula, formula2: LogicFormula) -> BoolOp:
        return BoolOp(formula1, self.op, formula2)


class ArithOpBuilder:
    def __init__(self, op: ArithOpType) -> None:
        self.op = op

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


class CompBuilder:
    def __init__(self, comp: CompType) -> None:
        self.comp = comp

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
        if not isinstance(var, ArithExpression):
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
        if not isinstance(var, LogicFormula):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into LogicFormula"
            )
        return var
