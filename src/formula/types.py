from functools import reduce
from typing import Any, Callable, Iterator, Self

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

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError(f"__iter__ not implemented for {self}")

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        raise NotImplementedError(f"is_syntaxically_eq not implemented for {self}")


# Types which output a logic formula (usually LogicFormulas combined with logic operators)
class LogicFormula:
    from .variable import Variable

    def __rshift__(self, rhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(
            Not(into_canonical_logic_formula(self)),
            BoolOpType.DISJ,
            into_canonical_logic_formula(rhs),
        )

    def __lshift__(self, rhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(
            Not(into_canonical_logic_formula(rhs)),
            BoolOpType.DISJ,
            into_canonical_logic_formula(self),
        )

    def __rrshift__(self, lhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(
            Not(into_canonical_logic_formula(lhs)),
            BoolOpType.DISJ,
            into_canonical_logic_formula(self),
        )

    def __rlshift__(self, lhs: Any):
        from .boolop import BoolOp, BoolOpType
        from .notb import Not

        return BoolOp(
            Not(into_canonical_logic_formula(self)),
            BoolOpType.DISJ,
            into_canonical_logic_formula(lhs),
        )

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

        return BoolOp(
            into_canonical_logic_formula(self),
            BoolOpType.DISJ,
            into_canonical_logic_formula(rhs),
        )

    def __ror__(self, lhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(
            into_canonical_logic_formula(lhs),
            BoolOpType.DISJ,
            into_canonical_logic_formula(self),
        )

    def __and__(self, rhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(
            into_canonical_logic_formula(self),
            BoolOpType.CONJ,
            into_canonical_logic_formula(rhs),
        )

    def __rand__(self, lhs: IntoLogicFormula):
        from .boolop import BoolOp, BoolOpType

        return BoolOp(
            into_canonical_logic_formula(lhs),
            BoolOpType.CONJ,
            into_canonical_logic_formula(self),
        )

    def __repr_colored__(self, level: int) -> str:
        return into_canonical_logic_formula(self).__repr_colored__(level)

    def __iter__(self) -> Iterator[Variable]:
        return iter(into_canonical_logic_formula(self))

    def __getitem__(self, variable: Variable):
        from formula.variable_info import VariableInfo

        return VariableInfo(self, variable)

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        return into_canonical_logic_formula(self).is_syntaxically_eq(
            into_canonical_logic_formula(rhs)
        )

    def map_formula(self, fn: Callable[["LogicFormula"], Self]) -> "LogicFormula":
        return into_canonical_logic_formula(self).map_formula(fn)


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


def into_canonical_logic_formula(var: Any) -> LogicFormula:
    from formula.forms import CNF, DNF, NNF

    """
    Converts (almost) anything into a LogicFormula.

    This is useful to allow, for example `forall.a(True)` without having to type `forall.a(BoolConst(True))`.
    """
    from .boolconst import BoolConst

    if isinstance(var, bool):
        return BoolConst(var)
    elif isinstance(var, NNF):
        return var.formula
    elif isinstance(var, CNF):
        return reduce(
            LogicFormula.__and__,
            [
                reduce(LogicFormula.__or__, disj.iter_formulas())
                for disj in var.formulas.iter_formulas()
            ],
        )
    elif isinstance(var, DNF):
        return reduce(
            LogicFormula.__or__,
            [
                reduce(LogicFormula.__and__, conj.iter_formulas())
                for conj in var.formulas.iter_formulas()
            ],
        )
    else:
        if not isinstance(var, LogicFormula):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into LogicFormula"
            )
        return var
