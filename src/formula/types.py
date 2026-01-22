# Compatibility with Python 3.12 and 3.13
from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING, Any, Callable, Iterator, Self, overload

import display

# Types that can be converted into an ArithExpression
type IntoArithExpression = ArithExpression | int | float | str


# Types that can be converted into a LogicFormula
type IntoLogicFormula = LogicFormula | bool


class ArithExpression:
    """
    Base class for all arithmetic expressions.
    """

    col: int

    if TYPE_CHECKING:
        from .variable import IntoVariable

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

    def __repr_syntax__(self) -> str:
        raise NotImplementedError(f"__repr_syntax__ not implemented for {self}")

    def __repr_depth__(self, level: int) -> str:
        raise NotImplementedError(f"__repr_depth__ not implemented for {self}")

    def __repr__(self) -> str:
        match display.COLORING:
            case (
                display.Coloring.NOT_COLORED | display.Coloring.SYNTAX  # type: ignore
            ):
                return self.__repr_syntax__()
            case display.Coloring.DEPTH:  # type: ignore
                return self.__repr_depth__(0)

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError(f"__iter__ not implemented for {self}")

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        raise NotImplementedError(f"is_syntaxically_eq not implemented for {self}")

    def replace(self, variable: IntoVariable, expr: IntoArithExpression) -> Self:
        raise NotImplementedError(f"replace not implemented for {self}")


class LogicFormula:
    """
    Base class for logical formulas.
    """

    col: int

    if TYPE_CHECKING:
        from .variable import IntoVariable, Variable
        from .variable_info import VariableInfo

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
        return isinstance(rhs, self.__class__) and self.is_syntaxically_eq(rhs)

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

    def __repr_syntax__(self) -> str:
        f = into_canonical_logic_formula(self)
        if f == self:
            raise NotImplementedError(f"__repr_syntax__ is not implemented for {self}")
        else:
            return into_canonical_logic_formula(self).__repr_syntax__()

    def __repr_depth__(self, level: int) -> str:
        f = into_canonical_logic_formula(self)
        if f == self:
            raise NotImplementedError(f"__repr_depth__ is not implemented for {self}")
        else:
            return into_canonical_logic_formula(self).__repr_depth__(level)

    def __repr__(self) -> str:
        match display.COLORING:
            case (
                display.Coloring.NOT_COLORED | display.Coloring.SYNTAX  # type: ignore
            ):
                return self.__repr_syntax__()
            case display.Coloring.DEPTH:  # type: ignore
                return self.__repr_depth__(0)

    def __iter__(self) -> Iterator[Variable]:
        return iter(into_canonical_logic_formula(self))

    @overload
    def __getitem__(
        self,
        arg: slice[IntoVariable, IntoArithExpression, None]
        | tuple[slice[IntoVariable, IntoArithExpression, None], ...],
    ) -> Self: ...

    @overload
    def __getitem__(self, arg: IntoVariable) -> VariableInfo: ...

    def __getitem__(
        self,
        arg: IntoVariable
        | slice[IntoVariable, IntoArithExpression, None]
        | tuple[slice[IntoVariable, IntoArithExpression, None], ...],
    ):
        from .comp import Comp
        from .quantifier import Quantifier
        from .variable import Variable, into_variable

        if isinstance(arg, slice):
            # f[v:a]
            arg = (arg,)
        if isinstance(arg, tuple):
            # f[v:a, x:b, ...]
            replacements = [
                (into_variable(sli.start), into_arith_expr(sli.stop)) for sli in arg
            ]

            # Replace the first variable with a placeholder name

            for i, (old, _) in enumerate(replacements):

                def replace(node: LogicFormula):
                    if isinstance(node, Comp):
                        node = Comp(
                            node.expr1.replace(old, into_variable(f"__temp{i}")),
                            node.comp,
                            node.expr2.replace(old, into_variable(f"__temp{i}")),
                        )
                    elif isinstance(node, Quantifier):
                        if node.variable.is_syntaxically_eq(old):
                            node = Quantifier(
                                node.quantifier,
                                into_variable(f"__temp{i}"),
                                node.formula,
                            )
                    return node

                self = into_canonical_logic_formula(self).map_formula(replace)

            for i, (old, new) in enumerate(replacements):

                def replace(node: LogicFormula):
                    if isinstance(node, Comp):
                        node = Comp(
                            node.expr1.replace(into_variable(f"__temp{i}"), new),
                            node.comp,
                            node.expr2.replace(into_variable(f"__temp{i}"), new),
                        )
                    elif isinstance(node, Quantifier):
                        if node.variable.is_syntaxically_eq(
                            into_variable(f"__temp{i}")
                        ):
                            if isinstance(new, Variable):
                                node = Quantifier(node.quantifier, new, node.formula)
                            else:
                                node = Quantifier(node.quantifier, old, node.formula)
                    return node

                self = into_canonical_logic_formula(self).map_formula(replace)
            return self

        else:
            # f[v]
            from .variable_info import VariableInfo

            return VariableInfo(self, into_variable(arg))

    def is_syntaxically_eq(self, rhs: Any) -> bool:
        return into_canonical_logic_formula(self).is_syntaxically_eq(
            into_canonical_logic_formula(rhs)
        )

    def map_formula(self, fn: Callable[["LogicFormula"], Self]) -> "LogicFormula":
        return into_canonical_logic_formula(self).map_formula(fn)

    def __hash__(self) -> int:
        return hash(repr(self))


def into_arith_expr(var: Any) -> ArithExpression:
    """
    Converts (almost) anything into an ArithExpression.

    This is useful to allow, for example `Variable("a") < 1` without having to type `Variable("a") < IntegerConst(1)`.
    """
    from .numconst import NumConst
    from .variable import Variable

    if isinstance(var, int) or isinstance(var, float):
        return NumConst(var)
    elif isinstance(var, str):
        return Variable(var)
    else:
        if not isinstance(var, ArithExpression):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into ArithExpression"
            )
        return var


def into_canonical_logic_formula(var: Any) -> LogicFormula:
    """
    Converts (almost) anything into a LogicFormula.

    This is useful to allow, for example `forall.a(True)` without having to type `forall.a(BoolConst(True))`.
    """
    from .boolconst import BoolConst
    from .boolop import BoolOpType
    from .forms import CNF, DNF, NNF, PNF
    from .formula_set import FormulaSet

    if isinstance(var, bool):
        return BoolConst(var)
    elif isinstance(var, NNF):
        return var.formula
    elif isinstance(var, PNF):
        return var.formula
    elif isinstance(var, CNF):
        return into_canonical_logic_formula(var.formula)
    elif isinstance(var, DNF):
        return into_canonical_logic_formula(var.formula)

    elif isinstance(var, FormulaSet):
        if var.boolop == BoolOpType.CONJ:
            if len(var.formulas) == 0:
                return BoolConst(True)
            return reduce(LogicFormula.__and__, var.iter_formulas())
        else:
            if len(var.formulas) == 0:
                return BoolConst(False)
            return reduce(LogicFormula.__or__, var.iter_formulas())

    else:
        if not isinstance(var, LogicFormula):
            raise TypeError(
                f"Cannot convert value of type {type(var)} into LogicFormula"
            )
        return var
