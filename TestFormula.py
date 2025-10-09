from main import *

# Formula from the subjet pdf
print(allq("x",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))
print(allq("x1",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))

# This formula is rejected
#print(allq("1",allq(y,allq(z,exq(u,impl(conj(ltf(x, y), ltf(x, z)),conj(ltf(y, u), ltf(z, u))))))))

