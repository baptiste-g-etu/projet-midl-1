from typing import Any, Callable, Self


# Types that can be converted into an ArithExpression
type IntoArithExpression = ArithExpression | int | str

# Types that can be converted into a LogicFormula
type IntoLogicFormula = LogicFormula | bool


# Types which are arithmetic expressions (usually ArithExpressions combined with arithmetic operators)
class ArithExpression:
    def __lt__(self, rhs: IntoArithExpression):
        from .comp import Comp, CompType

        return Comp(self, CompType.LOWER_THAN, into_arith_expr(rhs))

    def __gt__(self, rhs: IntoArithExpression):
        from .comp import Comp, CompType

        return Comp(into_arith_expr(rhs), CompType.LOWER_THAN, self)

    def __le__(self, rhs: IntoArithExpression):
        from .comp import Comp, CompType

        return Comp(self, CompType.LOWER_THAN, into_arith_expr(rhs)) | Comp(
            self, CompType.EQUAL, into_arith_expr(rhs)
        )

    def __ge__(self, rhs: IntoArithExpression):
        from .comp import Comp, CompType

        return Comp(into_arith_expr(rhs), CompType.LOWER_THAN, self) | Comp(
            self, CompType.EQUAL, into_arith_expr(rhs)
        )

    def __eq__(self, rhs: IntoArithExpression):  # type: ignore because __eq__ is supposed to always return a bool
        from .comp import Comp, CompType

        return Comp(self, CompType.EQUAL, into_arith_expr(rhs))

    def __ne__(self, rhs: IntoArithExpression):  # type: ignore because __ne__ is supposed to always return a bool
        from .comp import Comp, CompType

        return ~(Comp(self, CompType.EQUAL, into_arith_expr(rhs)))

    def __add__(self, rhs: IntoArithExpression):
        from .arithop import ArithOp, ArithOpType

        return ArithOp(self, ArithOpType.SUM, into_arith_expr(rhs))

    def __radd__(self, lhs: IntoArithExpression):
        from .arithop import ArithOp, ArithOpType

        return ArithOp(into_arith_expr(lhs), ArithOpType.SUM, self)

    def __sub__(self, rhs: IntoArithExpression):
        from .arithop import ArithOp, ArithOpType

        return ArithOp(self, ArithOpType.SUB, into_arith_expr(rhs))

    def __rsub__(self, lhs: IntoArithExpression):
        from .arithop import ArithOp, ArithOpType

        return ArithOp(into_arith_expr(lhs), ArithOpType.SUB, self)

    def __mul__(self, rhs: IntoArithExpression):
        from .arithop import ArithOp, ArithOpType

        return ArithOp(self, ArithOpType.PROD, into_arith_expr(rhs))

    def __rmul__(self, lhs: IntoArithExpression):
        from .arithop import ArithOp, ArithOpType

        return ArithOp(into_arith_expr(lhs), ArithOpType.PROD, self)

    def __repr_colored__(self, level: int) -> str:
        raise NotImplementedError(f"__repr_colored__ not implemented for {self}")

    def __contains__(self, variable: Any) -> bool:
        raise NotImplementedError(f"__contains__ not implemented for {self}")

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        raise NotImplementedError(f"is_syntaxically_eq not implemented for {self}")


# Types which output a logic formula (usually LogicFormulas combined with logic operators)
class LogicFormula:
    from .variable import Variable

    def __rshift__(self, rhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(Not(self), BoolOpType.DISJ, into_logic_formula(rhs))

    def __lshift__(self, rhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(Not(into_logic_formula(rhs)), BoolOpType.DISJ, self)

    def __rrshift__(self, lhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(Not(into_logic_formula(lhs)), BoolOpType.DISJ, self)

    def __rlshift__(self, lhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(Not(self), BoolOpType.DISJ, into_logic_formula(lhs))

    def __lt__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __gt__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __le__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __ge__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __eq__(self, rhs: Any):
        raise SyntaxError("Cannot compare logical formulas")

    def __invert__(self):
        from .notb import Not

        return Not(self)

    def __or__(self, rhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(self, BoolOpType.DISJ, into_logic_formula(rhs))

    def __ror__(self, lhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(into_logic_formula(lhs), BoolOpType.DISJ, self)

    def __and__(self, rhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(self, BoolOpType.CONJ, into_logic_formula(rhs))

    def __rand__(self, lhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(into_logic_formula(lhs), BoolOpType.CONJ, self)

    def __repr_colored__(self, level: int) -> str:
        raise NotImplementedError(f"__repr_colored__ not implemented for {self}")

    def __contains__(self, variable: Variable) -> bool:
        raise NotImplementedError(f"__contains__ not implemented for {self}")

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        raise NotImplementedError(f"is_syntaxically_eq not implemented for {self}")

    def map_formula(self, fn: Callable[[Self], Self]) -> Self:
        raise NotImplementedError(f"map_formula not implemented for {self}")


def into_arith_expr(var: Any) -> ArithExpression:
    """
    Converts (almost) anything into an ArithExpression.

    This is useful to allow, for example `Variable("a") < 1` without having to type `Variable("a") < IntegerConst(1)`.
    """
    from .integerconst import IntegerConst
    from .variable import Variable

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
    from .boolconst import BoolConst
    from .forms import NNF

    if isinstance(var, bool):
        return BoolConst(var)
    else:
        if not isinstance(var, LogicFormula):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into LogicFormula"
            )
        if isinstance(var, NNF):
            return var.formula
        # TODO Add DNF and CNF
        return var
