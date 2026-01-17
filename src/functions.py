"""
Temporary file to try recursive functions over all nodes in a tree.
"""

# TODO : decide where to put all these functions : into formula.py, setup.py, or here ?

# Function to dualize a formula by swapping AND and OR operators
from formula.boolconst import BoolConst
from formula.boolop import BoolOp, BoolOpType
from formula.comp import Comp
from formula.notb import Not
from formula.quantifier import Quantifier, QuantifierBuilder, QuantifierType
from formula.types import IntoLogicFormula, LogicFormula, into_canonical_logic_formula
from formula.variable import Variable


def dual(formula: IntoLogicFormula) -> LogicFormula:
    """
    Useless function to swap conjunctions and disjunctions.
    """

    def swap_and_or(node: LogicFormula):
        if isinstance(node, BoolOp):
            new_op = (
                BoolOpType.DISJ if node.boolop == BoolOpType.CONJ else BoolOpType.CONJ
            )

            return BoolOp(node.formula1, new_op, node.formula2)
        elif isinstance(node, Quantifier):
            raise ValueError("Cannot dualize a formula with quantifiers")
        return node

    return into_canonical_logic_formula(formula).map_formula(swap_and_or)


def negation(formula: IntoLogicFormula) -> LogicFormula:
    """
    Computes the negation of a formula (without just adding one `Not`).
    """

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
            return BoolConst(False) if node.const else BoolConst(True)
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

    return into_canonical_logic_formula(formula).map_formula(negation_inner)


def swap_quantifiers_old(formula: IntoLogicFormula) -> LogicFormula:
    """
    Swap all quantifiers in the formula: FORALL <-> EXISTS
    """

    def swap_q(node: LogicFormula):
        if isinstance(node, Quantifier):
            new_q_type = (
                QuantifierType.EXISTS
                if node.quantifier == QuantifierType.FORALL
                else QuantifierType.FORALL
            )
            return Quantifier(new_q_type, node.variable, node.formula)
        return node

    return into_canonical_logic_formula(formula).map_formula(swap_q)


def swap_quantifiers(formula: IntoLogicFormula) -> LogicFormula:
    """
    Swap all quantifiers in the formula: FORALL <-> EXISTS, while preserving logic.

    Simplifies some negations in quantifier chains.
    """

    def swap_q(node: LogicFormula):
        if isinstance(node, Quantifier):
            new_q_type = (
                QuantifierType.EXISTS
                if node.quantifier == QuantifierType.FORALL
                else QuantifierType.FORALL
            )
            return Quantifier(new_q_type, node.variable, node.formula)
        return node

    return into_canonical_logic_formula(formula).map_formula(swap_q)


def close(f: IntoLogicFormula) -> LogicFormula:
    """
    Closes the formula with universal quantifiers.
    """
    f = into_canonical_logic_formula(f)
    quantifier_builder = QuantifierBuilder(QuantifierType.FORALL)
    quantifier_builder.variables = free_variables(f)

    return quantifier_builder(f)


def free_variables(f: IntoLogicFormula) -> list[Variable]:
    """
    Lists all free variables of the formula.
    """
    f = into_canonical_logic_formula(f)
    return [variable for variable in f if f[variable].is_free()]
