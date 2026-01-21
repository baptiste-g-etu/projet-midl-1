from functions import dual, swap_quantifiers
from prelude import (
    CNF,
    DNF,
    NNF,
    PNF,
    ConstF,
    Not,
    allq,
    conj,
    exists,
    exq,
    forall,
    impl,
    ltf,
    u,
    x,
    y,
    z,
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
conn = forall.x.y((x == y) | (x < y) | (y < x))  # Connectivité
dense = forall.x.y((x < y) >> exists.z((x < z) & (z < y)))  # Densité
sextr = forall.x(exists.y.z((y < x) & (x < z)))  # Sans extrema

f3 = trans & asym & conn & dense & sextr
print(f"f3         : {f3}")
print(f"NNF(f3)    : {NNF(PNF(f3))}")
print(f"CNF(f3)    : {CNF(f3)}")
print(f"\ntrans      : {trans}")
print(f"NNF(trans) : {NNF(PNF(trans))}")
print(f"DNF(trans) : {DNF(trans)}")
print(f"\nasym       : {asym}")
print(f"DNF(asym)  : {DNF(asym)}")
print(f"\nconn       : {conn}")
print(f"DNF(conn)  : {DNF(conn)}")
print(f"\ndense      : {dense}")
print(f"DNF(dense) : {DNF(dense)}")
print(f"\nsextr      : {sextr}")
print(f"CNF(sextr) : {CNF(sextr)}")
