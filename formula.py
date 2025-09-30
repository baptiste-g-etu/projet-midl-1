"""
Base types for the project.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Self


# Types which are arithmetic expressions (usually ArithExpressions combined with arithmetic operators)
type ArithExpression = Variable | Comp | IntegerConst
# Types which output a logic formula (usually LogicFormulas combined with logic operators)
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
class IncompleteFormula:
    """
    Because the Python bitwise OR has higher priority than the comparison operators,
    we need to invert the operator priority afterwards.

    For example :
    `a < b | c < d` is evaluated as `a < (b | c) < d` (because of Python),
    then `(b | c)` is translated into `IncompleteFormula(b, |, c)`,
    then `a < (b | c)` is translated into `IncompleteFormula(a < b, |, c)`,
    then `IncompleteFormula(a < b, |, c) < d` is translated into `a < b | c < d`
    (except because of Python comparison that transform `a < b < c` into `a < b` and `b < c`,
    only returning the result of `b < c`, it’s actually even more complicated).
    """

    expr1: ArithExpression | LogicFormula
    op: BoolOpType
    expr2: ArithExpression | LogicFormula

    def __repr__(self) -> str:
        return f"INCOMPLETE({{}} {self.expr1} {self.op} {self.expr2} {{}})"

    def __gt__(self, lhs: Self | ArithExpression | int):
        """
        Should only be called with `self` as the right-hand side
        (this is more like a « reverse lower than » than an actual « greater than »).
        """
        if isinstance(lhs, Self):
            # The > operator is used because it’s the only way to come into this branch
            # (python wouldn’t replace the < if it was called between two instances of IncompleteFormula)
            raise SyntaxError("Cannot use the > operator, use < instead")
        elif isinstance(lhs, ArithExpression.__value__ | int):
            self.expr1 = into_arith_expr(lhs) < self.expr1

    def __lt__(self, rhs: Self | ArithExpression | int):
        pass


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

    # TODO Maybe implement a < b < c, for example as (a < b) and (b < c)
    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot use comparison operators on boolean constants")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot use comparison operators on boolean constants")


@dataclass
class Variable:
    name: str

    def __repr__(self) -> str:
        return self.name

    # Logical operators - they build an IncompleteFormula
    # (logical operators do not operate directly onto variables,
    # instead they wait for a comparison to operate onto it)
    def __or__(self, rhs: ArithExpression | int) -> IncompleteFormula:
        return IncompleteFormula(self, BoolOpType.DISJ, into_arith_expr(rhs))

    def __ror__(self, lhs: ArithExpression | int) -> IncompleteFormula:
        return IncompleteFormula(into_arith_expr(lhs), BoolOpType.DISJ, self)

    def __and__(self, rhs: ArithExpression | int) -> IncompleteFormula:
        return IncompleteFormula(self, BoolOpType.CONJ, into_arith_expr(rhs))

    def __rand__(self, lhs: ArithExpression | int) -> IncompleteFormula:
        return IncompleteFormula(into_arith_expr(lhs), BoolOpType.CONJ, self)

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

    def __lt__(self, rhs: IncompleteFormula | ArithExpression | int) -> Comp:
        if isinstance(rhs, IncompleteFormula):
            # If we compare with an IncompleteFormula, we need to call it instead
            # (so it can add the comparison to the existing IncompleteFormula).
            # To call it, we simply mark the comparison as NotImplemented,
            # so Python can go search for IncompleteFormula.__gt__.
            return NotImplemented
        return Comp(self, CompType.LOWER_THAN, into_arith_expr(rhs))

    def __le__(self, rhs: Self) -> IncompleteFormula:
        raise NotImplementedError("Called Variable::__le__")

    def __rlt__(self, rhs: Self) -> IncompleteFormula:
        raise NotImplementedError("Called Variable::__rlt__")

    def __eq__(self, rhs: Self) -> IncompleteFormula:  # type: ignore because __eq__ is supposed to always return a bool
        raise NotImplementedError("Called Variable::__eq__")


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
