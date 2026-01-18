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


def swap_quantifiers(formula: IntoLogicFormula) -> LogicFormula:
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


def all_exists(formula: IntoLogicFormula) -> LogicFormula:
    """
    Swap all universal quantifiers in the formula for existential quantifiers, while preserving logic.

    Simplifies some negations in quantifier chains.
    """

    def swap_q(node: LogicFormula):
        if isinstance(node, Quantifier) and node.quantifier == QuantifierType.FORALL:
            if isinstance(node.formula, Not):
                return ~Quantifier(
                    QuantifierType.EXISTS, node.variable, node.formula.formula
                )
            else:
                return ~Quantifier(QuantifierType.EXISTS, node.variable, ~node.formula)
        return node

    return into_canonical_logic_formula(formula).map_formula(swap_q)


def close(f: IntoLogicFormula) -> LogicFormula:
    """
    Closes the formula with universal quantifiers.
    """
    f = into_canonical_logic_formula(f)

    quantifier_builder = QuantifierBuilder(QuantifierType.FORALL)
    quantifier_builder.variables = free_variables(f)

    if len(quantifier_builder.variables) == 0:
        return f
    else:
        return quantifier_builder(f)


def free_variables(f: IntoLogicFormula) -> list[Variable]:
    """
    Lists all free variables of the formula.
    """
    f = into_canonical_logic_formula(f)
    return [variable for variable in f if f[variable].is_free()]


def separate_quantifiers(
    f: IntoLogicFormula,
) -> tuple[list[tuple[bool, QuantifierType, Variable]], LogicFormula]:
    """
    Separates the quantifiers of a formula from the inner formula.

    This formula is almost prenex, but it can also have `Not`s before or after the quantifiers.

    It returns a list of tuples of boolean (that indicates if a `Not` was placed before the quantifier), quantifier type and variable, and the inner formula.
    """
    formula = into_canonical_logic_formula(f)
    quantifiers: list[tuple[bool, QuantifierType, Variable]] = []

    invert = False
    while isinstance(formula, Quantifier) or isinstance(formula, Not):
        if isinstance(formula, Quantifier):
            quantifiers.append((invert, formula.quantifier, formula.variable))
            invert = False
        else:
            invert = not invert
        formula = formula.formula

    if invert:
        formula = Not(formula)
    quantifiers.reverse()

    return (quantifiers, formula)


def join_quantifiers(
    quantifiers: list[tuple[bool, QuantifierType, Variable]],
    f: IntoLogicFormula,
) -> LogicFormula:
    """
    Applies a quantifier list to a formula.
    """
    f = into_canonical_logic_formula(f)
    for invert, qt, var in quantifiers:
        if invert:
            f = Not(Quantifier(qt, var, f))
        else:
            f = Quantifier(qt, var, f)
    return f


def compute_formula_only_constants(f: IntoLogicFormula) -> bool:
    """
    Computes the result of a formula made of only constants
    """
    f = into_canonical_logic_formula(f)

    def compute_formula_only_constants_inner(node: LogicFormula):
        if isinstance(node, Quantifier):
            return node.formula.map_formula(compute_formula_only_constants_inner)
        elif isinstance(node, BoolConst):
            return node
        elif isinstance(node, BoolOp):
            lhs = node.formula1.map_formula(compute_formula_only_constants_inner)
            assert isinstance(lhs, BoolConst)
            rhs = node.formula2.map_formula(compute_formula_only_constants_inner)
            assert isinstance(rhs, BoolConst)
            if node.boolop == BoolOpType.DISJ:
                return BoolConst(lhs.const or rhs.const)
            else:
                return BoolConst(lhs.const and rhs.const)
        elif isinstance(node, Not):
            inner = node.formula.map_formula(compute_formula_only_constants_inner)
            assert isinstance(inner, BoolConst)
            return BoolConst(not inner.const)
        else:
            raise ValueError(
                f"Unknown node type for compute_formula_only_constants : {node}"
            )

    res = f.map_formula(compute_formula_only_constants_inner)
    assert isinstance(res, BoolConst)
    return res.const
