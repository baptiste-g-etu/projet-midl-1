import string

from decision.elim import decide  # type: ignore # noqa: F401
from formula.arithop import ArithOp, ArithOpBuilder, ArithOpType
from formula.boolconst import BoolConst
from formula.boolop import BoolOp, BoolOpBuilder, BoolOpType
from formula.coloring import COLORING, color_level  # type: ignore # noqa: F401
from formula.comp import Comp, CompBuilder, CompType
from formula.forms import CNF, DNF, NNF, FormulaSet  # type: ignore # noqa: F401
from formula.notb import Not
from formula.quantifier import Quantifier, QuantifierBuilder, QuantifierType
from formula.types import (
    ArithExpression,  # type: ignore # noqa: F401
    IntoArithExpression,  # type: ignore # noqa: F401
    IntoLogicFormula,
    LogicFormula,  # type: ignore # noqa: F401
    into_canonical_logic_formula,  # type: ignore # noqa: F401
)
from formula.variable import IntoVariable, Variable
from functions import close, dual, free_variables, negation, swap_quantifiers # type: ignore # noqa: F401
from variables import a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z  # type: ignore # noqa: F401 # fmt: skip



# Compatibility with the original syntax.py
Eq = CompType.EQUAL
EQUAL = CompType.EQUAL
Lt = CompType.LOWER_THAN
LOWER_THAN = CompType.LOWER_THAN

All = QuantifierType.FORALL
FORALL = QuantifierType.FORALL
Ex = QuantifierType.EXISTS
EXISTS = QuantifierType.EXISTS

Conj = BoolOpType.CONJ
CONJ = BoolOpType.CONJ
Disj = BoolOpType.DISJ
DISJ = BoolOpType.DISJ

ConstF = BoolConst
ComparF = Comp
NotF = Not
BoolOpF = BoolOp
QuantifF = Quantifier

eqf = CompBuilder(CompType.EQUAL)
ltf = CompBuilder(CompType.LOWER_THAN)


def allq(var: IntoVariable, formula: IntoLogicFormula):
    return Quantifier(QuantifierType.FORALL, var, formula)


def exq(var: IntoVariable, formula: IntoLogicFormula):
    return Quantifier(QuantifierType.EXISTS, var, formula)


conj = BoolOpBuilder(BoolOpType.CONJ)
disj = BoolOpBuilder(BoolOpType.DISJ)


def impl(formula1: IntoLogicFormula, formula2: IntoLogicFormula) -> BoolOp:
    return disj(Not(formula1), formula2)


# Assumptions of the second part made from the original syntax.py
Sum = ArithOpType.SUM
Sub = ArithOpType.SUB
Prod = ArithOpType.PROD

ArithOpF = ArithOp

sum = ArithOpBuilder(ArithOpType.SUM)
sub = ArithOpBuilder(ArithOpType.SUB)
prod = ArithOpBuilder(ArithOpType.PROD)

# New aliases to make formulas faster to type and easier to read
forall = QuantifierBuilder(QuantifierType.FORALL)
exists = QuantifierBuilder(QuantifierType.EXISTS)

true = top = BoolConst(True)
false = bot = BoolConst(False)

cnf = CNF
dnf = DNF
nnf = NNF

# Define all ascii lowercase letters as variables
for char in string.ascii_lowercase:
    globals()[char] = Variable(char)
