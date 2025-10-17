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

    return formula.map_formula(swap_and_or)


# Function to find the logical negation of a formula (without adding `Not`s)
def negation(formula: LogicFormula) -> LogicFormula:
    def negation_inner(node: LogicFormula):
        if isinstance(node, BoolOp):
            new_op = (
                BoolOpType.DISJ if node.boolop == BoolOpType.CONJ else BoolOpType.CONJ
            )

            # negation is already appplied to node.formula1 aaaand node.formula2
            return BoolOp(node.formula1, new_op, node.formula2)
        elif isinstance(node, Comp):
            return ~node
        elif isinstance(node, BoolConst):
            return false if node.const else true
        elif isinstance(node, Quantifier):
            new_q = (
                QuantifierType.EXISTS
                if node.quantifier == QuantifierType.FORALL
                else QuantifierType.FORALL
            )
            # negation is already appplied to node.formula
            return Quantifier(new_q, node.variable, node.formula)
        elif isinstance(node, Not):
            # We don’t do anything (except for simplifying formulas),
            # because the additional negation is already applied to the inner formula
            if isinstance(node.formula, Not):
                return node.formula.formula
        return node

    return formula.map_formula(negation_inner)


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

    return formula.map_formula(swap_q)
