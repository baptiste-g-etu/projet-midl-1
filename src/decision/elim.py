from formula.boolconst import BoolConst
from formula.boolop import BoolOpType
from formula.comp import Comp, CompType
from formula.forms import DNF, NNF, PNF, FormulaSet
from formula.formula_set import flatten_conj
from formula.notb import Not
from formula.quantifier import QuantifierType
from formula.types import IntoLogicFormula, LogicFormula, into_canonical_logic_formula
from formula.variable import into_variable
from functions import (
    all_exists,
    close,
    compute_formula_only_constants,
    free_variables,
    separate_quantifiers,
)


def decide(f: IntoLogicFormula) -> bool:
    closed = close(f)
    print(f"\x1b[1mTrying to decied formula : {closed}\x1b[21m")
    prenex = PNF(closed)
    alle = all_exists(prenex)

    print(f"  (quantifiers replaced) : {alle}")
    quantifiers, current_formula = separate_quantifiers(alle)

    invert = (
        False  # True if the next iteration should add a `Not` in front of the formula
    )
    for inv, qt, var in quantifiers:
        assert qt == QuantifierType.EXISTS
        current_formula = into_canonical_logic_formula(current_formula)
        if invert:
            current_formula = Not(current_formula)
        print(
            f"\x1b[1mEliminating variable {var} in formula {current_formula} :\x1b[21m"
        )
        current_formula = NNF(PNF(current_formula))
        print(f"  - NNF : {current_formula}")
        current_formula = DNF(current_formula)
        print(f"  - DNF : {current_formula}")
        # Now that the formula is in DNF, we assume the current exisential quantifier applies to each member of the DNF.
        new_dnf: FormulaSet = FormulaSet(set(), BoolOpType.DISJ)
        for conj in current_formula.formulas.iter_formulas():
            var_is_not_free_in_conj = True
            assert type(conj) is FormulaSet

            for form in conj.iter_formulas():
                if var in free_variables(form):
                    var_is_not_free_in_conj = False
                    break

            end = False
            if var_is_not_free_in_conj:
                # var is in free_variables
                # print(f"      - {var} isn’t in conjunction")
                new_dnf.formulas.add(conj)
                end = True  # To the next conjunction of the outer DNF

            if not end:
                for form in conj.iter_formulas():
                    if (
                        isinstance(form, Comp)
                        and form.is_syntaxically_eq(var < var)
                        or isinstance(form, BoolConst)
                        and not form.const
                    ):
                        # var < var or False are in the conjunction, we insert False (we could theoretically skip inserting)
                        new_dnf.formulas.add(BoolConst(False))
                        end = True

            if not end:
                # x < var
                var_on_lhs: FormulaSet = FormulaSet(set(), BoolOpType.CONJ)
                # var < x
                var_on_rhs: FormulaSet = FormulaSet(set(), BoolOpType.CONJ)
                # var = x or x = var
                var_equals: FormulaSet = FormulaSet(set(), BoolOpType.CONJ)
                # x = y or x < y
                var_not_present: FormulaSet = FormulaSet(set(), BoolOpType.CONJ)

                for form in conj.iter_formulas():
                    if isinstance(form, Comp):
                        if form.comp == CompType.LOWER_THAN:
                            if form.expr1.is_syntaxically_eq(var):
                                assert not form.expr2.is_syntaxically_eq(var)
                                var_on_lhs.formulas.add(form)
                            elif form.expr2.is_syntaxically_eq(var):
                                var_on_rhs.formulas.add(form)
                            else:
                                var_not_present.formulas.add(form)
                        else:
                            if form.is_syntaxically_eq(var == var):
                                # Skip when var = var
                                continue
                            if form.expr1.is_syntaxically_eq(var):
                                assert not form.expr2.is_syntaxically_eq(var)
                                var_equals.formulas.add(form)
                            elif form.expr2.is_syntaxically_eq(var):
                                var_equals.formulas.add(form.expr2 == form.expr1)
                            else:
                                var_not_present.formulas.add(form)
                    elif isinstance(form, BoolConst):
                        assert (
                            form.const
                        )  # We would have stopped earlier if we found a False constant
                    else:
                        assert False, (
                            f"The DNF contained something else than comparisons and boolean constants : {form}"
                        )

                if len(var_equals.formulas) > 0:
                    # We can replace all instances of the current variable with the found variable
                    first_equality = var_equals.iter_formulas().__next__()
                    assert isinstance(first_equality, Comp)
                    new_var = into_variable(first_equality.expr2)
                    assert not new_var.is_syntaxically_eq(var)

                    new_dnf.formulas.add(
                        flatten_conj(
                            (var_on_lhs & var_on_rhs & var_equals)[var:new_var]
                            & var_not_present
                        )
                    )
                elif len(var_on_lhs.formulas) > 0 and len(var_on_rhs.formulas) > 0:
                    var_product = FormulaSet(set(), BoolOpType.CONJ)
                    for lhs in var_on_lhs.iter_formulas():
                        assert isinstance(lhs, Comp)
                        for rhs in var_on_rhs.iter_formulas():
                            assert isinstance(rhs, Comp), f"{rhs}"
                            var_product.formulas.add(rhs.expr1 < lhs.expr2)
                    new_dnf.formulas.add(flatten_conj(var_product & var_not_present))
                else:
                    new_dnf.formulas.add(var_not_present)

        invert = inv
        print()
        # Tiny optimization on dnf to remove boolean constants
        formulas: set[FormulaSet | LogicFormula] = set(
            FormulaSet(
                set(
                    [
                        form
                        for form in conj.iter_formulas()
                        if not isinstance(form, BoolConst)
                    ]
                ),
                BoolOpType.CONJ,
            )
            for conj in new_dnf.formulas
            if isinstance(conj, FormulaSet)
            and not any(
                isinstance(form, BoolConst)
                and BoolConst(False).is_syntaxically_eq(form)
                for form in conj.iter_formulas()
            )
        )
        new_dnf.formulas = formulas
        current_formula = new_dnf

    if invert:
        current_formula = Not(current_formula)
    print(f"Final formula : {current_formula}")
    return compute_formula_only_constants(current_formula)
