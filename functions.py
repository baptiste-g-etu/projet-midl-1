"""
Temporary file to try recursive functions over all nodes in a tree.
"""
# TODO : decide where to put all these functions : into formula.py, setup.py, or here ?
from formula import LogicFormula, BoolOp, Not, Quantifier, Comp, BoolConst, BoolOpType, QuantifierType
from setup import *
from typing import Callable # For type hinting of map_formula

def map_formula(formula: LogicFormula, fn: Callable[[LogicFormula], LogicFormula]) -> LogicFormula:
    """
    Recursively applies fn function to every node in the formula tree.
    fn should take a LogicFormula and return a LogicFormula.
    """
    # Apply recursively to children first (post-order traversal)
    if isinstance(formula, BoolOp):
        left = map_formula(formula.formula1, fn)
        right = map_formula(formula.formula2, fn)
        new_node = BoolOp(left, formula.boolop, right)
    elif isinstance(formula, Not):
        sub = map_formula(formula.formula, fn)
        new_node = Not(sub)
    elif isinstance(formula, Quantifier):
        sub = map_formula(formula.formula, fn)
        new_node = Quantifier(formula.quantifier, formula.variable, sub)
    elif isinstance(formula, Comp):
        # Comparisons are leaves (their children are ArithExpressions, not LogicFormulas)
        new_node = formula
    elif isinstance(formula, BoolConst):
        new_node = formula
    else:
        raise TypeError(f"Unknown formula type: {type(formula)}")
    # Apply the function to the current node
    return fn(new_node)
    
    
# Function to dualize a formula by swapping AND and OR operators
# Used to debug map_formula
def dual(formula: LogicFormula) -> LogicFormula:
    # function sent to map_formula
    def swap_and_or(node : LogicFormula):
        if isinstance(node, BoolOp):
            new_op = BoolOpType.DISJ if node.boolop == BoolOpType.CONJ else BoolOpType.CONJ
            
            return BoolOp(node.formula1, new_op, node.formula2)
        elif isinstance(node, Quantifier):
            raise ValueError("Cannot dualize a formula with quantifiers")
        return node
    return map_formula(formula, swap_and_or)


def swap_quantifiers(formula: LogicFormula) -> LogicFormula:
    """
    Swap all quantifiers in the formula: FORALL <-> EXISTS
    """
    def swap_q(node : LogicFormula):
        if isinstance(node, Quantifier):
            new_q = QuantifierType.EXISTS if node.quantifier == QuantifierType.FORALL else QuantifierType.FORALL
            return Quantifier(new_q, node.variable, node.formula)
        return node
    return map_formula(formula, swap_q)


