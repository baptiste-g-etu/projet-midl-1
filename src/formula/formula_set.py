from itertools import chain
from typing import Iterator, Self

from formula.boolop import BoolOp, BoolOpType
from formula.coloring import COLORING, color_level
from formula.types import LogicFormula
from formula.variable import Variable

LONG_FORMULA = 100


class FormulaSet(LogicFormula):
    """
    A set of formulas.
    """

    def __init__(
        self,
        formulas: set[LogicFormula | Self],
        op: BoolOpType,
    ) -> None:
        self.formulas = formulas
        self.op = op

    def __repr_colored__(self, level: int) -> str:
        return f"{color_level(level, '{')}{color_level(level, ',\n    ' if len(self.formulas) >= LONG_FORMULA else ', ').join([formula.__repr_colored__(level + 1) for formula in self.formulas])}{color_level(level, '}')}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"{{{(',\n    ' if len(self.formulas) >= LONG_FORMULA else ', ').join(str(formula) for formula in self.formulas)}}}"

    def iter_formulas(self):
        return iter(self.formulas)

    def __iter__(self) -> Iterator[Variable]:
        variable_list = list(set(chain.from_iterable(self.formulas)))
        variable_list.sort(key=lambda v: v.name)
        return iter(variable_list)

    def __add__(self, other: Self) -> "FormulaSet":
        """
        Adds two sets.

        They should be of the same type of formulas and of the same type of operator.
        """
        assert self.op == other.op
        return FormulaSet(set(chain(self.formulas, other.formulas)), self.op)


def flatten_disj(
    formula: LogicFormula,
) -> FormulaSet:
    """
    Flattens a disjunctive `BoolOp` into a `FormulaSet`
    """

    if isinstance(formula, BoolOp) and formula.boolop == BoolOpType.DISJ:
        return flatten_disj(formula.formula1) + flatten_disj(formula.formula2)
    return FormulaSet(set([formula]), BoolOpType.DISJ)


def flatten_conj(
    formula: LogicFormula,
) -> FormulaSet:
    """
    Flattens a conjunctive `BoolOp` into a `FormulaSet`
    """

    if isinstance(formula, BoolOp) and formula.boolop == BoolOpType.CONJ:
        return flatten_conj(formula.formula1) + flatten_conj(formula.formula2)
    return FormulaSet(set([formula]), BoolOpType.CONJ)
