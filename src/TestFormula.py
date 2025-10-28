from src.functions import dual, swap_quantifiers
from src.prelude import (
    CNF,
    DNF,
    NNF,
    ConstF,
    Not,
    allq,
    exq,
    impl,
    ltf,
    conj,
    forall,
    exists,
    x,
    y,
    z,
    u,
)
# from prelude import *
# from functions import *


# Formula from the subjet pdf


print(
    allq(
        "x",
        allq(
            y,
            allq(
                z, exq(u, impl(conj(ltf(x, y), ltf(x, z)), conj(ltf(y, u), ltf(z, u))))
            ),
        ),
    )
)
print(
    allq(
        "x1",
        allq(
            y,
            allq(
                z, exq(u, impl(conj(ltf(x, y), ltf(x, z)), conj(ltf(y, u), ltf(z, u))))
            ),
        ),
    )
)

# This formula is rejected
# print(allq("1",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))


# Example usage for Dual() (used subject exemple):
f = conj(ConstF(True), ConstF(False))
print(f)

print(f"After dual(): {dual(f)}")
print(f"dual(not(f)): {dual(Not(f))}")
# print("Dual with a quantifier (should raise an error):")
# map_formula(allq("x", f), dual)


# Example usage for swap_quantifiers():
f2 = allq("x", exq("y", conj(ltf("x", "y"), ltf("y", "x"))))
print(f"Test formula for swap_quantifiers(): {f2}")
print(f"After swap_quantifiers(): {swap_quantifiers(f2)}")

trans = forall.x.y.z(((x < y) & (y < z)) >> (x < z))  # Transitivité
asym = forall.x.y((x < y) >> ~(y < x))  # Asymétrie
conn = forall.x.y.z((x == y) | (x < y) | (y < x))  # Connectivité
dense = forall.x.y((x < y) >> exists.z((x < z) & (z < y)))  # Densité
sextr = forall.x(exists.y.z((y < x) & (x < z)))  # Sans extrema

f3 = trans & asym & conn & dense & sextr
print(f"f3         : {f3}")
print(f"NNF(f3)    : {NNF(f3)}")
print(f"\ntrans      : {trans}")
print(f"NNF(trans) : {NNF(trans.formula.formula.formula)}")
print(f"DNF(trans) : {DNF(trans.formula.formula.formula)}")
print(f"CNF(trans) : {CNF(trans.formula.formula.formula)}")
print(f"\nconn       : {asym}")
print(f"NNF(asym)  : {NNF(asym.formula.formula)}")
print(f"DNF(asym)  : {DNF(asym.formula.formula)}")
print(f"CNF(asym)  : {CNF(asym.formula.formula)}")
print(f"\nconn       : {conn}")
print(f"NNF(conn)  : {NNF(conn.formula.formula.formula)}")
print(f"DNF(conn)  : {DNF(conn.formula.formula.formula)}")
print(f"CNF(conn)  : {CNF(conn.formula.formula.formula)}")
print(f"\ndense      : {dense}")
print(f"NNF(dense) : {NNF(dense.formula.formula)}")
print(f"DNF(dense) : {DNF(dense.formula.formula)}")
print(f"CNF(dense) : {CNF(dense.formula.formula)}")
print(f"\nsextr      : {sextr}")
print(f"NNF(sextr) : {NNF(sextr.formula.formula.formula)}")
print(f"DNF(sextr) : {DNF(sextr.formula.formula.formula)}")
print(f"CNF(sextr) : {CNF(sextr.formula.formula.formula)}")
