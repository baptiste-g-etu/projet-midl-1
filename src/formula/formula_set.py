from itertools import chain
from typing import Iterator, Self

from display import color, color_by_depth

from .boolop import BoolOp, BoolOpType
from .types import LogicFormula
from .variable import Variable

LONG_FORMULA = 100


class FormulaSet(LogicFormula):
    """
    A set of formulas.
    """

    def __init__(
        self,
        formulas: set[LogicFormula | Self],
        boolop: BoolOpType,
    ) -> None:
        self.formulas = formulas
        self.boolop = boolop

        match self.boolop:
            case BoolOpType.DISJ:
                self.col = 2
            case BoolOpType.CONJ:
                self.col = 1

    def __repr_syntax__(self) -> str:
        return f"{color(self.col, f'{self.boolop}{{')}{color(self.col, ',\n    ' if len(self.formulas) >= LONG_FORMULA else ', ').join([repr(formula) for formula in self.formulas])}{color(self.col, '}')}"

    def __repr_depth__(self, level: int) -> str:
        return f"{color_by_depth(level, f'{self.boolop}{{')}{color_by_depth(level, ',\n    ' if len(self.formulas) >= LONG_FORMULA else ', ').join([formula.__repr_depth__(level + 1) for formula in self.formulas])}{color_by_depth(level, '}')}"

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
        assert self.boolop == other.boolop
        return FormulaSet(set(chain(self.formulas, other.formulas)), self.boolop)


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
