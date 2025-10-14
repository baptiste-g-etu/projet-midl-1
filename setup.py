from formula import (
    ArithExpression,  # noqa: F401
    ArithOp,
    ArithOpBuilder,
    ArithOpType,
    BoolConst,
    BoolOp,
    BoolOpBuilder,
    BoolOpType,
    Comp,
    CompBuilder,
    CompType,
    IntoLogicFormula,
    IntoVariable,
    LogicFormula,  # noqa: F401
    Not,
    Quantifier,
    QuantifierBuilder,
    QuantifierType,
    Variable,
)
import string


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

# Define all ascii lowercase letters as variables
for char in string.ascii_lowercase:
    globals()[char] = Variable(char)
