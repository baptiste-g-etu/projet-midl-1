from formula import (
    BoolConst,
    BoolOp,
    BoolOpBuilder,
    BoolOpType,
    Comp,
    CompBuilder,
    CompType,
    Not,
    Quantifier,
    QuantifierBuilder,
    QuantifierType,
    Variable,
)
from string import ascii_lowercase


# Compatibility with the original syntax.py
Eq = CompType.EQUAL
Lt = CompType.LOWER_THAN

All = QuantifierType.FORALL
Ex = QuantifierType.EXISTS

Conj = BoolOpType.CONJ
Disj = BoolOpType.DISJ

ConstF = BoolConst
ComparF = Comp
NotF = Not
BoolOpF = BoolOp
QuantifF = Quantifier

eqf = CompBuilder(CompType.EQUAL)
ltf = CompBuilder(CompType.LOWER_THAN)

allq = QuantifierBuilder(QuantifierType.FORALL)
exq = QuantifierBuilder(QuantifierType.EXISTS)

conj = BoolOpBuilder(BoolOpType.CONJ)
disj = BoolOpBuilder(BoolOpType.DISJ)

# TODO impl (function or class ?)

# New aliases to make formulas faster to type and easier to read
forall = QuantifierBuilder(QuantifierType.FORALL)
exists = QuantifierBuilder(QuantifierType.EXISTS)

true = BoolConst(True)
false = BoolConst(False)

# Define all ascii lowercase letters as variables
for char in ascii_lowercase:
    globals()[char] = Variable(char)
