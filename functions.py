"""
Temporary file to try recursive functions over all nodes in a tree.
"""

# TODO : decide where to put all these functions : into formula.py, setup.py, or here ?
from formula import (
    LogicFormula,
    BoolOp,
    Quantifier,
    BoolOpType,
    QuantifierType,
)
from setup import *


# Function to dualize a formula by swapping AND and OR operators
def dual(formula: LogicFormula) -> LogicFormula:
    def swap_and_or(node: LogicFormula):
        if isinstance(node, BoolOp):
            new_op = (
                BoolOpType.DISJ if node.boolop == BoolOpType.CONJ else BoolOpType.CONJ
            )

            return BoolOp(node.formula1, new_op, node.formula2)
        elif isinstance(node, Quantifier):
            raise ValueError("Cannot dualize a formula with quantifiers")
        return node

    return formula.logical_map(swap_and_or)


def swap_quantifiers(formula: LogicFormula) -> LogicFormula:
    """
    Swap all quantifiers in the formula: FORALL <-> EXISTS
    """

    def swap_q(node: LogicFormula):
        if isinstance(node, Quantifier):
            new_q = (
                QuantifierType.EXISTS
                if node.quantifier == QuantifierType.FORALL
                else QuantifierType.FORALL
            )
            return Quantifier(new_q, node.variable, node.formula)
        return node

    return formula.logical_map(swap_q)
