from typing import Iterator

from formula.boolconst import BoolConst
from formula.boolop import BoolOp, BoolOpType
from formula.coloring import COLORING, color_level
from formula.comp import Comp, CompType
from formula.formula_set import FormulaSet, flatten_conj, flatten_disj
from formula.notb import Not
from formula.quantifier import Quantifier
from formula.types import IntoLogicFormula, LogicFormula, into_canonical_logic_formula
from formula.variable import Variable


# TODO Factor these into a Form subclass ?
class PNF(LogicFormula):
    """
    Prenex Normal Form.

    # Invariant

    This class must always contain a formula in it’s Prenex Normal Form.
    This invariant is ensured by the constructor.
    """

    def __init__(self, formula: LogicFormula) -> None:
        formula = into_canonical_logic_formula(formula)
        after_quantif = formula
        while isinstance(after_quantif, Quantifier):
            after_quantif = after_quantif.formula

        # TODO Convert the formula into it’s prenex normal form instead of raising an AssertionError
        def pnf_inner(node: LogicFormula):
            assert not isinstance(node, Quantifier), (
                "Cannot create a prenex formula from a non-prenex formula"
            )
            return node

        after_quantif.map_formula(pnf_inner)
        self.formula = formula

    def __repr_colored__(self, level: int) -> str:
        return f"{color_level(level, 'PNF(')}{self.formula.__repr_colored__(level + 1)}{color_level(level, ')')}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"PNF({self.formula})"


class NNF(LogicFormula):
    """
    Negation Normal Form.

    # Invariant

    This class must always contain a formula in it’s Negation Normal Form.
    This invariant is ensured by the constructor.
    """

    def __init__(self, formula: PNF) -> None:
        from functions import join_quantifiers, separate_quantifiers

        quantifiers, f = separate_quantifiers(formula)

        def nnf_inner(node: LogicFormula):
            if isinstance(node, Not):
                if isinstance(node.formula, Not):
                    return node.formula.formula  # ~~a -> a
                elif isinstance(node.formula, BoolOp):
                    match node.formula.boolop:
                        case BoolOpType.CONJ:
                            return into_canonical_logic_formula(
                                NNF(
                                    PNF(~node.formula.formula1 | ~node.formula.formula2)
                                )
                            )  # ~(a & b) -> (~a | ~b)
                        case BoolOpType.DISJ:
                            return into_canonical_logic_formula(
                                NNF(
                                    PNF(~node.formula.formula1 & ~node.formula.formula2)
                                )
                            )  # ~(a | b) -> (~a & ~b)
                elif isinstance(node.formula, Comp):
                    match node.formula.comp:
                        case CompType.LOWER_THAN:
                            return (node.formula.expr1 == node.formula.expr2) | (
                                node.formula.expr2 < node.formula.expr1
                            )
                        case CompType.EQUAL:
                            return (node.formula.expr1 < node.formula.expr2) | (
                                node.formula.expr2 < node.formula.expr1
                            )
                elif isinstance(node.formula, BoolConst):
                    return BoolConst(not node.formula.const)
            return node

        f = f.map_formula(nnf_inner)
        self.formula = join_quantifiers(quantifiers, f)

    def __repr_colored__(self, level: int) -> str:
        return f"{color_level(level, 'NNF(')}{self.formula.__repr_colored__(level + 1)}{color_level(level, ')')}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"NNF({self.formula})"


class DNF(LogicFormula):
    """
    Disjunctive Normal Form.

    # Invariant

    This class must always contain a formula in it’s Disjunctive Normal Form.
    This invariant is ensured by the constructor.
    """

    def __init__(self, formula: IntoLogicFormula) -> None:
        formula = into_canonical_logic_formula(formula)
        while isinstance(formula, Quantifier):
            formula = formula.formula

        def dnf_inner(node: LogicFormula):
            if isinstance(node, Not):
                if isinstance(node.formula, Not):
                    return node.formula.formula  # ~~a -> a
                elif isinstance(node.formula, BoolOp):
                    match node.formula.boolop:
                        case BoolOpType.CONJ:
                            return ~node.formula.formula1.map_formula(
                                dnf_inner
                            ) | ~node.formula.formula2.map_formula(dnf_inner)
                            # ~(a & b) -> (~a | ~b)
                        case BoolOpType.DISJ:
                            return ~node.formula.formula1.map_formula(
                                dnf_inner
                            ) & ~node.formula.formula2.map_formula(dnf_inner)
                            # ~(a | b) -> (~a & ~b)
            elif isinstance(node, BoolOp):
                if node.boolop == BoolOpType.CONJ:
                    if (
                        isinstance(node.formula1, BoolOp)
                        and node.formula1.boolop == BoolOpType.DISJ
                    ):
                        return (
                            node.formula1.formula1 & node.formula2
                            | node.formula1.formula2 & node.formula2
                        ).map_formula(dnf_inner)  # (a | b) & c -> (a & c) | (b & c)
                    elif (
                        isinstance(node.formula2, BoolOp)
                        and node.formula2.boolop == BoolOpType.DISJ
                    ):
                        return (
                            node.formula1 & node.formula2.formula1
                            | node.formula1 & node.formula2.formula2
                        ).map_formula(dnf_inner)  # a & (b | c) -> (a & b) | (a & c)
            return node

        self.formulas: FormulaSet = FormulaSet(
            [
                flatten_conj(formula)
                for formula in flatten_disj(
                    into_canonical_logic_formula(formula).map_formula(dnf_inner)
                ).iter_formulas()
            ],
            BoolOpType.DISJ,
        )

    def __repr_colored__(self, level: int) -> str:
        return f"{color_level(level, 'DNF')}{self.formulas.__repr_colored__(level)}"

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"DNF({self.formulas})"


class CNF(LogicFormula):
    """
    Conjunctive Normal Form.

    # Invariant

    This class must always contain a formula in it’s Conjunctive Normal Form.
    This invariant is ensured by the constructor.
    """

    def __init__(self, formula: IntoLogicFormula) -> None:
        formula = into_canonical_logic_formula(formula)
        while isinstance(formula, Quantifier):
            formula = formula.formula

        def cnf_inner(node: LogicFormula):
            if isinstance(node, Not):
                if isinstance(node.formula, Not):
                    return node.formula.formula  # ~~a -> a
                elif isinstance(node.formula, BoolOp):
                    match node.formula.boolop:
                        case BoolOpType.CONJ:
                            return ~node.formula.formula1.map_formula(
                                cnf_inner
                            ) | ~node.formula.formula2.map_formula(cnf_inner)
                            # ~(a & b) -> (~a | ~b)
                        case BoolOpType.DISJ:
                            return ~node.formula.formula1.map_formula(
                                cnf_inner
                            ) & ~node.formula.formula2.map_formula(cnf_inner)
                            # ~(a | b) -> (~a & ~b)
            elif isinstance(node, BoolOp):
                if node.boolop == BoolOpType.DISJ:
                    if (
                        isinstance(node.formula1, BoolOp)
                        and node.formula1.boolop == BoolOpType.CONJ
                    ):
                        return (
                            (node.formula1.formula1 | node.formula2)
                            & (node.formula1.formula2 | node.formula2)
                        ).map_formula(cnf_inner)  # (a & b) | c -> (a | c) & (b | c)
                    elif (
                        isinstance(node.formula2, BoolOp)
                        and node.formula2.boolop == BoolOpType.CONJ
                    ):
                        return (
                            (node.formula1 | node.formula2.formula1)
                            & (node.formula1 | node.formula2.formula2)
                        ).map_formula(cnf_inner)  # a | (b & c) -> (a | b) & (a | c)
            return node

        self.formulas: FormulaSet = FormulaSet(
            [
                flatten_disj(formula)
                for formula in flatten_conj(
                    into_canonical_logic_formula(formula).map_formula(cnf_inner)
                ).iter_formulas()
            ],
            BoolOpType.CONJ,
        )

    def __repr_colored__(self, level: int) -> str:
        return f"{color_level(level, 'CNF')}{self.formulas.__repr_colored__(level)}"

    def __iter__(self) -> Iterator[Variable]:
        return iter(into_canonical_logic_formula(self))

    def __repr__(self) -> str:
        if COLORING:
            return self.__repr_colored__(0)
        else:
            return f"CNF({self.formulas})"
