from formula.coloring import color_level, COLORING
from formula.notb import Not
from formula.types import LogicFormula
from formula.boolop import BoolOp, BoolOpType


class NNF(LogicFormula):
    def __init__(self, formula: LogicFormula) -> None:
        self.formula = nnf(formula)

    def __repr_colored__(self, level: int) -> str:
        return f"{color_level(level, 'NNF(')}{self.formula.__repr_colored__(level + 1)}{color_level(level, ')')}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"NNF({self.formula})"


def nnf(formula: LogicFormula) -> LogicFormula:
    """
    Converts the given formula into a Negative Normal Form
    """

    def nnf_inner(node: LogicFormula):
        if isinstance(node, Not):
            if isinstance(node.formula, Not):
                return node.formula.formula
            elif isinstance(node.formula, BoolOp):
                match node.formula.boolop:
                    case BoolOpType.CONJ:
                        return nnf(~node.formula.formula1 | ~node.formula.formula2)
                    case BoolOpType.DISJ:
                        return nnf(~node.formula.formula1 & ~node.formula.formula2)            
        return node

    return formula.map_formula(nnf_inner)
