import gmpy2
import libnum
from Crypto.Util.number import *
n =
e =
c =
p =
q =
phi = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi)
d =
m = pow(c,d,n)
print(long_to_bytes(m))