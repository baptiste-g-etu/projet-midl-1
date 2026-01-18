from formula.boolop import BoolOpType
from formula.comp import Comp, CompType
from formula.forms import DNF, NNF, PNF, FormulaSet
from formula.notb import Not
from formula.quantifier import QuantifierType
from formula.types import IntoLogicFormula, into_canonical_logic_formula
from functions import all_exists, close, free_variables, separate_quantifiers


def decide(f: IntoLogicFormula) -> bool:
    closed = close(f)
    prenex = PNF(closed)
    alle = all_exists(prenex)

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
        new_dnf: list[FormulaSet] = []
        for conj in current_formula.formulas.iter_formulas():
            print(f"      - Conj {conj}")
            var_in_free_variables = True
            assert type(conj) is FormulaSet

            for form in conj.iter_formulas():
                if var not in free_variables(form):
                    var_in_free_variables = False
                    break

            if var_in_free_variables:
                # var is in free_variables
                print(f"      - {var} is in free_variables of the conjunction")
                new_dnf.append(conj)
                continue  # To the next conjunction of the outer DNF

            for form in conj.iter_formulas():
                if form.is_syntaxically_eq(var < var):
                    # var < var is in the conjunction, we insert an empty set (we could theoretically skip inserting)
                    new_dnf.append(FormulaSet([], BoolOpType.CONJ))

            # var < x
            var_on_rhs: FormulaSet = FormulaSet([], BoolOpType.CONJ)
            # x < var
            var_on_lhs: FormulaSet = FormulaSet([], BoolOpType.CONJ)
            # var = x or x = var
            var_equals: FormulaSet = FormulaSet([], BoolOpType.CONJ)
            # x = y or x < y
            var_not_present: FormulaSet = FormulaSet([], BoolOpType.CONJ)

            for form in conj.iter_formulas():
                if isinstance(form, Comp):
                    if form.comp == CompType.LOWER_THAN:
                        if form.expr1.is_syntaxically_eq(var):
                            assert not form.expr2.is_syntaxically_eq(var)
                            var_on_lhs.formulas.append(form)
                        elif form.expr2.is_syntaxically_eq(var):
                            var_on_rhs.formulas.append(form)
                        else:
                            var_not_present.formulas.append(form)
                    else:
                        if form.expr1.is_syntaxically_eq(var):
                            assert not form.expr2.is_syntaxically_eq(var)
                            var_equals.formulas.append(form)
                        elif form.expr2.is_syntaxically_eq(var):
                            var_equals.formulas.append(form.expr2 == form.expr1)
                        else:
                            var_not_present.formulas.append(form)
                else:
                    assert False, (
                        f"The DNF contained something else than comparisons : {form}"
                    )

            if len(var_equals.formulas) > 0:
                # We can replace all instances of the current variable with the found variable
                pass

            raise NotImplementedError

        invert = inv
        print()

    # Logical XOR gate
    return True is not invert
