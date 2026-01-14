from .boolop import BoolOp
from .comp import Comp
from .notb import Not
from .quantifier import Quantifier
from .types import IntoLogicFormula, LogicFormula, into_logic_formula
from .variable import Variable


class VariableInfo:
    """
    Represents a variable inside a formula.

    Useful to get info such as free-ness (which is lazily calculated)
    """

    def __init__(self, f: IntoLogicFormula, v: Variable) -> None:
        f = into_logic_formula(f)
        if v not in f:
            raise KeyError("Variable is not in formula")
        self.variable: Variable = v
        self.formula: LogicFormula = f

    def is_free(self) -> bool:
        """
        Returns `True` if the variable is used freely at least once inside the formula,
        returning `False` if all uses of the variable are made when it is quantified.

        If the variable is not inside the formula, this function returns `False`
        """

        if self.variable not in self.formula:
            return False
        if isinstance(self.formula, BoolOp):
            return (
                self.variable in self.formula.formula1
                and self.formula.formula1[self.variable].is_free()
                or self.variable in self.formula.formula2
                and self.formula.formula2[self.variable].is_free()
            )
        elif isinstance(self.formula, Comp):
            # This assumes that v is in f which is the case
            return True
        elif isinstance(self.formula, Quantifier):
            if self.formula.variable == self.variable:
                # v is quantified in the whole inner formula
                return False
            else:
                return self.formula.formula[self.variable].is_free()
        elif isinstance(self.formula, Not):
            return self.formula.formula[self.variable].is_free()
        else:
            # unreachable
            assert False
