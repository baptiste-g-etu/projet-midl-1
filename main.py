from setup import *

# form: list = [
#     Eq, Eq(), EQUAL, EQUAL(),
#     Lt, Lt(), LOWER_THAN, LOWER_THAN(),
#     All, All(), FORALL, FORALL(),
#     Ex, Ex(), EXISTS, EXISTS(),
#     Conj, Conj(), CONJ, CONJ(),
#     Disj, Disj(), DISJ, DISJ(),
#     ConstF(True), BoolConst(True),
#     ComparF(f, LOWER_THAN(), f), Comp(f, EQUAL(), f),
#     NotF(l), Not(l),
#     true, false,

#     eqf(f, f), CompBuilder(CompType.EQUAL)(f, f),
#     ltf(f, f), CompBuilder(CompType.LOWER_THAN)(f, f),
#     conj(l, l), BoolOpBuilder(BoolOpType.CONJ)(l, l),
#     disj(l, l), BoolOpBuilder(BoolOpType.DISJ)(l, l),
#     forall.v(l), QuantifierBuilder(QuantifierType.FORALL).v(l),
#     exists.v(l), QuantifierBuilder(QuantifierType.EXISTS).v(l),
#     sum(f, f), ArithOp(f, ArithOpType.SUM, f), ArithOpF(f, Sum, f), ArithOpF(f, Sum(), f), ArithOpBuilder(ArithOpType.SUM)(f, f),
#     sub(f, f), ArithOp(f, ArithOpType.SUB, f), ArithOp(f, Sub, f), ArithOpF(f, Sub(), f), ArithOpBuilder(ArithOpType.SUB)(f, f),
#     prod(f, f),ArithOp(f, ArithOpType.PROD, f), ArithOp(f, Prod, f), ArithOpF(f, Prod(), f), ArithOpBuilder(ArithOpType.PROD)(f, f),
# 

#     BoolOpF(l, Lt, l), BoolOp(l, Eq(), l),
#     QuantifF(FORALL, v, l), Quantifier(EXISTS, v, l),
#     allq(v, l), exq(v, l),
#     impl(l, l),
#     a, b, c, d,
#     ...,
# ]
# print(form)
