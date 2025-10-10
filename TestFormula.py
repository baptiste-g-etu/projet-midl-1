from formula import *
from setup import *
from functions import *


# Formula from the subjet pdf
print(allq("x",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))
print(allq("x1",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))

# This formula is rejected
#print(allq("1",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))


# Example usage for Dual() (used subject exemple):
f = conj(ConstF(True), ConstF(False))
print(f)

print(f"After dual(): {map_formula(f, dual)}")
print(f"dual(not(f)): {map_formula(Not(f), dual)}")
#print("Dual with a quantifier (should raise an error):")
#map_formula(allq("x", f), dual)


# Example usage for swap_quantifiers():
f2 = allq("x", exq("y", conj(ltf("x", "y"), ltf("y", "x"))))
print(f"Test formula for swap_quantifiers(): {f2}")
print(f"After swap_quantifiers(): {swap_quantifiers(f2)}")