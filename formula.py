"""
Base types for the project.
"""

from enum import StrEnum
from typing import Any, Callable, Self

# Colors for colorful printing of formulas (from user's terminal)
NORMAL = [35, 36, 34, 32, 33, 31]
COLOR_RESET = "\x1b[39m"
COLORING = True

# Types that can be converted into an ArithExpression
type IntoArithExpression = ArithExpression | int | str

# Types that can be converted into a LogicFormula
type IntoLogicFormula = LogicFormula | bool

# Types that can be converted into a Variable
type IntoVariable = Variable | str


# Types which are arithmetic expressions (usually ArithExpressions combined with arithmetic operators)
class ArithExpression:
    def __lt__(self, rhs: Any):
        return Comp(self, CompType.LOWER_THAN, rhs)

    def __gt__(self, rhs: IntoArithExpression):
        return Comp(into_arith_expr(rhs), CompType.LOWER_THAN, self)

    # TODO lower equal ?

    def __eq__(self, rhs: IntoArithExpression):  # type: ignore because __eq__ is supposed to always return a bool
        return Comp(self, CompType.EQUAL, into_arith_expr(rhs))

    def __add__(self, rhs: IntoArithExpression):
        return ArithOp(self, ArithOpType.SUM, into_arith_expr(rhs))

    def __radd__(self, lhs: IntoArithExpression):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUM, self)

    def __sub__(self, rhs: IntoArithExpression):
        return ArithOp(self, ArithOpType.SUB, into_arith_expr(rhs))

    def __rsub__(self, lhs: IntoArithExpression):
        return ArithOp(into_arith_expr(lhs), ArithOpType.SUB, self)

    def __mul__(self, rhs: IntoArithExpression):
        return ArithOp(self, ArithOpType.PROD, into_arith_expr(rhs))

    def __rmul__(self, lhs: IntoArithExpression):
        return ArithOp(into_arith_expr(lhs), ArithOpType.PROD, self)

    def __repr_parenthesis__(self):
        return f"({self})"

    def __repr_colored_parenthesis__(self, level: int) -> str:
        raise NotImplementedError(
            f"__repr_colored_parenthesis__ not implemented for {self}"
        )

    def __contains__(self, variable: "Variable") -> bool:
        raise NotImplementedError(f"__contains__ not implemented for {self}")

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        raise NotImplementedError(f"is_syntaxically_eq not implemented for {self}")


# Types which output a logic formula (usually LogicFormulas combined with logic operators)
class LogicFormula:
    def __rshift__(self, rhs: Any):
        return BoolOp(Not(self), BoolOpType.DISJ, into_logic_formula(rhs))

    def __lshift__(self, rhs: Any):
        return BoolOp(Not(into_logic_formula(rhs)), BoolOpType.DISJ, self)

    def __rrshift__(self, lhs: Any):
        return BoolOp(Not(into_logic_formula(lhs)), BoolOpType.DISJ, self)

    def __rlshift__(self, lhs: Any):
        return BoolOp(Not(self), BoolOpType.DISJ, into_logic_formula(lhs))

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __eq__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __invert__(self):
        return Not(self)

    def __or__(self, rhs: IntoLogicFormula):
        return BoolOp(self, BoolOpType.DISJ, into_logic_formula(rhs))

    def __ror__(self, lhs: IntoLogicFormula):
        return BoolOp(into_logic_formula(lhs), BoolOpType.DISJ, self)

    def __and__(self, rhs: IntoLogicFormula):
        return BoolOp(self, BoolOpType.CONJ, into_logic_formula(rhs))

    def __rand__(self, lhs: IntoLogicFormula):
        return BoolOp(into_logic_formula(lhs), BoolOpType.CONJ, self)

    def __repr_parenthesis__(self):
        return f"({self})"

    def __repr_colored_parenthesis__(self, level: int) -> str:
        raise NotImplementedError(
            f"__repr_colored_parenthesis__ not implemented for {self}"
        )

    def __contains__(self, variable: "Variable") -> bool:
        raise NotImplementedError(f"__contains__ not implemented for {self}")

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        raise NotImplementedError(f"is_syntaxically_eq not implemented for {self}")

    def logical_map(self, fn: Callable[[Self], Self]) -> Self:
        raise NotImplementedError(f"map not implemented for {self}")


class BoolOpType(StrEnum):
    CONJ = "∧"
    DISJ = "∨"

    def __call__(self) -> Self:
        return self


class BoolOp(LogicFormula):
    def __init__(
        self, formula1: IntoLogicFormula, boolop: BoolOpType, formula2: IntoLogicFormula
    ) -> None:
        self.formula1 = into_logic_formula(formula1)
        self.boolop = boolop
        self.formula2 = into_logic_formula(formula2)

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return (
            self.formula1.is_syntaxically_eq(rhs.formula1)
            and self.boolop == rhs.boolop
            and self.formula2.is_syntaxically_eq(rhs.formula2)
        )

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return f"{self.formula1.__repr_parenthesis__()} {self.boolop} {self.formula2.__repr_parenthesis__()}"

    def __repr_colored_parenthesis__(self, level: int) -> str:
        return f"{color_level(level)}({COLOR_RESET}{self.formula1.__repr_colored_parenthesis__(level + 1)} {color_level(level)}{self.boolop}{COLOR_RESET} {self.formula2.__repr_colored_parenthesis__(level + 1)}{color_level(level)}){COLOR_RESET}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.formula1 or variable in self.formula2

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare booleans")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare booleans")

    def logical_map(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(
            BoolOp(
                self.formula1.logical_map(fn),
                self.boolop,
                self.formula2.logical_map(fn),
            )
        )


class ArithOpType(StrEnum):
    SUM = "+"
    SUB = "-"
    PROD = "×"
    # DIV = "/" # Division isn’t supported

    def __call__(self) -> Self:
        return self


class ArithOp(ArithExpression):
    def __init__(
        self,
        expr1: IntoArithExpression,
        arithop: ArithOpType,
        expr2: IntoArithExpression,
    ):
        self.expr1 = into_arith_expr(expr1)
        self.arithop = arithop
        self.expr2 = into_arith_expr(expr2)

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return (
            self.expr1.is_syntaxically_eq(rhs.expr1)
            and self.arithop == rhs.arithop
            and self.expr2.is_syntaxically_eq(rhs.expr2)
        )

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int) -> str:
        return f"{self.expr1.__repr_colored_parenthesis__(level)} {color_level(level)}{self.arithop}{COLOR_RESET} {self.expr2.__repr_colored_parenthesis__(level)}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.expr1 or variable in self.expr2

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return f"{self.expr1.__repr_parenthesis__()} {self.arithop} {self.expr2.__repr_parenthesis__()}"


class CompType(StrEnum):
    LOWER_THAN = "<"
    EQUAL = "="

    def __repr__(self):
        return self

    def __call__(self) -> Self:
        return self


class Comp(LogicFormula):
    def __init__(
        self, expr1: IntoArithExpression, comp: CompType, expr2: IntoArithExpression
    ) -> None:
        self.expr1 = into_arith_expr(expr1)
        self.comp = comp
        self.expr2 = into_arith_expr(expr2)

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return (
            self.expr1.is_syntaxically_eq(rhs.expr1)
            and self.comp == rhs.comp
            and self.expr2.is_syntaxically_eq(rhs.expr2)
        )

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int) -> str:
        return f"{self.expr1.__repr_colored_parenthesis__(level)} {color_level(level)}{self.comp}{COLOR_RESET} {self.expr2.__repr_colored_parenthesis__(level)}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return f"{self.expr1.__repr_parenthesis__()} {self.comp} {self.expr2.__repr_parenthesis__()}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.expr1 or variable in self.expr2

    def __bool__(self):
        """
        Bool implementation so Python isn’t messed up with eq mismatch.
        """
        return self.expr1.is_syntaxically_eq(self.expr2)

    def logical_map(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(self)

    # TODO Maybe implement a < b < c, for example as (a < b) and (b < c)


class Variable(ArithExpression):
    def __init__(self, name: str) -> None:
        self.name = name

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.name == rhs.name

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int):
        return f"{color_level(level)}{self.name}{COLOR_RESET}"

    def __contains__(self, variable: Self) -> bool:
        return variable.name == self.name

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return self.name


class BoolConst(LogicFormula):
    def __init__(self, const: bool) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int):
        return f"{color_level(level)}{'⊤' if self.const else '⊥'}{COLOR_RESET}"

    def __contains__(self, variable: Variable) -> bool:
        return False

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return "⊤" if self.const else "⊥"

    def logical_map(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(self)


class IntegerConst(ArithExpression):
    def __init__(self, const: int) -> None:
        self.const = const

    def is_syntaxically_eq(self, rhs: Self) -> bool:
        return self.const == rhs.const

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int):
        return f"{color_level(level)}{self.const}{COLOR_RESET}"

    def __contains__(self, variable: Variable) -> bool:
        return False

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return str(self.const)


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

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int):
        return f"{color_level(level)}{self.quantifier}{COLOR_RESET}{self.variable.__repr_colored_parenthesis__(level)}{color_level(level)}.{COLOR_RESET}{self.formula.__repr_colored_parenthesis__(level)}"

    def __contains__(self, variable: Variable) -> bool:
        # TODO self.variable is in the formula ???
        return variable in self.formula

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return f"{self.quantifier}{self.variable}.{self.formula.__repr_parenthesis__()}"

    def logical_map(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(
            Quantifier(self.quantifier, self.variable, self.formula.logical_map(fn))
        )


class Not(LogicFormula):
    def __init__(self, formula: IntoLogicFormula) -> None:
        self.formula = into_logic_formula(formula)

    def __repr_parenthesis__(self) -> str:
        return self.__repr__()

    def __repr_colored_parenthesis__(self, level: int):
        return f"{color_level(level)}¬({COLOR_RESET}{self.formula.__repr_colored_parenthesis__(level + 1)}{color_level(level)}){COLOR_RESET}"

    def __contains__(self, variable: "Variable") -> bool:
        return variable in self.formula

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored_parenthesis__(0)
        else:
            return f"¬({self.formula.__repr_parenthesis__()})"

    def logical_map(self, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
        return fn(Not(self.formula.logical_map(fn)))


class BoolOpBuilder:
    def __init__(self, op: BoolOpType) -> None:
        self.op = op

    def __call__(
        self, formula1: IntoLogicFormula, formula2: IntoLogicFormula
    ) -> BoolOp:
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

    def __call__(self, expr1: IntoArithExpression, expr2: IntoArithExpression) -> Comp:
        return Comp(into_arith_expr(expr1), self.comp, into_arith_expr(expr2))


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


def into_variable(var: Any) -> Variable:
    """
    Converts a str into a Variable if needed. Also reject to cast a number as a variable
    """
    if isinstance(var, Variable):
        return var
    elif isinstance(var, str):
        if var.isdigit():
            # Should we keep that ?
            raise TypeError(f"You should not use the number : {var} as a variable name")
        return Variable(var)
    else:
        raise TypeError(f"Cannot convert value of type {type(var)} into Variable")


def color_level(level: int):
    """
    Returns the appropriate colors for different levels of nested formulas.
    """
    return f"\x1b[{NORMAL[level % len(NORMAL)]}m"
