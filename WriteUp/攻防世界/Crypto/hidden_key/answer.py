from Crypto.Util.number import *
import random
import hashlib
# 先算出key的高12位，再爆破key的低12位
high_key = 2669175714787937 << 12
xor = [140, 96, 112, 178, 38, 180, 158, 240, 179, 202, 251, 138, 188, 185, 23, 67, 163, 22, 150, 18, 143, 212, 93, 87, 209, 139, 92, 252, 55, 137, 6, 231, 105, 12, 65, 59, 223, 25, 179, 101, 19, 215]
def rand(rng):
    return rng - random.randrange(rng)

for i in range(2**12):
    key=long_to_bytes(high_key + i)
    flag = []
    random.seed(int(hashlib.md5(key).hexdigest(), 16))
    for i in range(len(xor)):
        rand(256)
        pieces = xor[i]^rand(256)
        flag.append(pieces)
    if all(c < 256 for c in flag):
        flag = bytes(flag)
        if(flag.startswith(b'flag')):
            print(flag)

