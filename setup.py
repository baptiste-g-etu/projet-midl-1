from formula import (
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
    LogicFormula,
    Not,
    Quantifier,
    QuantifierBuilder,
    QuantifierType,
    Variable,
)
from string import ascii_lowercase


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


def allq(var: Variable, formula: LogicFormula):
    return Quantifier(QuantifierType.FORALL, var, formula)


def exq(var: Variable, formula: LogicFormula):
    return Quantifier(QuantifierType.EXISTS, var, formula)


conj = BoolOpBuilder(BoolOpType.CONJ)
disj = BoolOpBuilder(BoolOpType.DISJ)


def impl(formula1: LogicFormula, formula2: LogicFormula) -> BoolOp:
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

true = BoolConst(True)
false = BoolConst(False)

# Define all ascii lowercase letters as variables
for char in ascii_lowercase:
    globals()[char] = Variable(char)
