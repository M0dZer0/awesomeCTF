#!/usr/bin/python
#-*- coding:utf-8 -*-

import re
import pickle
from itertools import product
from libnum import invmod, gcd


def solve_linear(a, b, mod):
    if a & 1 == 0 or b & 1 == 0:
        return None
    return (b * invmod(a, mod)) & (mod - 1)  # hack for mod = power of 2


def to_n(s):
    s = re.sub(r"[^0-9a-f]", "", s)
    return int(s, 16)


def msk(s):
    cleaned = "".join(map(lambda x: x[-2:], s.split(":")))
    return msk_ranges(cleaned), msk_mask(cleaned), msk_val(cleaned)


def msk_ranges(s):
    return [range(16) if c == " " else [int(c, 16)] for c in s]


def msk_mask(s):
    return int("".join("0" if c == " " else "f" for c in s), 16)


def msk_val(s):
    return int("".join("0" if c == " " else c for c in s), 16)


E = 0x10001

N = to_n("""00:db:fa:bd:b1:49:5d:32:76:e7:62:6b:84:79:6e:
    9f:c2:0f:a1:3c:17:44:f1:0c:8c:3f:3e:3c:2c:60:
    40:c2:e7:f3:13:df:a3:d1:fe:10:d1:ae:57:7c:fe:
    ab:74:52:aa:53:10:2e:ef:7b:e0:09:9c:02:25:60:
    e5:7a:5c:30:d5:09:40:64:2d:1b:09:7d:d2:10:9a:
    e0:2f:2d:cf:f8:19:8c:d5:a3:95:fc:ac:42:66:10:
    78:48:b9:dd:63:c3:87:d2:53:8e:50:41:53:43:04:
    20:33:ea:09:c0:84:15:5e:65:2b:0f:06:23:40:d5:
    d4:71:7a:40:2a:9d:80:6a:6b""")

p_ranges, pmask_msk, pmask_val = msk("""00:  :6 : 1:1 :  :b :0 : 2:c : b:2 :  : a:1 :
    c :  : 0:  :28:0 :  :cd:  : 8:  :  :20: c:  :
      : 5:  :9 : c:3 :  :  : a:b :c :3 :  :  :  :
     f:  :  : f: 1: 1:b :  : c:f : a:  :a :  :  :
     a:38:  :6 :  """)

q_ranges, qmask_msk, qmask_val = msk("""00:e :  :d :2 :6 : 7:  :33:  :46:  : 4:  :  :
      :5 :  : 4:6 :  : 6:  : e:d :  :  : 9: e:1 :
      :  :  :  :  :0 :  :  :  :c : 5:  :  :a :0 :
    6 :  :  :8 :e9:f : f:7 :5 : e:1 :  :  : 1:9 :
     4:d :e9: 6:  """)

_, dmask_msk, dmask_val = msk(""" f:  :  : a: a:9 :e :  : 1: 2:  :  :e :  :1 :
3 : 1:  :  :  : a:  :2 :  :  :  :  :  :  :  :
9 : a:  :  :  :  :  : 5:c1: 0:b : 3: 2:0 :b0:
  :c : f:  :f :  :d2:  :  : d:  :1 :  :3 :  :
  :  :  :0 : 3:  :  : 5:c :  :3 :6 :  :a4:  :
4 :  :  :8f:  :  :  :  : a:  : c:5f: 7: 6:  :
 1:  : b:  : 5:  :84:0 :b : f: 3:  :  : 4: 6:
  :  : 5:1 :  :d :  : f:  : c:  :  : 5:  :  :
  :e :f4:b :4 :8e:  :  """)

_, dpmask_msk, dpmask_val = msk(""" 9:d : 5:  :c :67:  : 9:  :  :  : d:  :  : 3:
 f:6 : 0:c :  :6 :ad:  :2 :d :d :  :  :0 :7 :
  :5 : 6:  : 5:1 :f : d:  : 2:  :  : 2: 3:  :
9 :  :  :  :  :67: 3:  :4 : 7:c0: 4:b :c :f :
  :3 :b : 1""")

_, dqmask_msk, dqmask_val = msk("""1 : 9:47:8 :  :  :  : 3:  :  :  :6 :  :  :0 :
e :e :8 :  :  :  :  : 1:c :74:  :  :d : 9:3 :
5 : e:  : 2:  :7 : 2:c :  :  :  :  :5 :  : 8:
  :  :c :  : 1:  :a :  : 9: 5:  : 3:  : e:c :
  :  : 6:  """)


def search(K, Kp, Kq, check_level, break_step):
    max_step = 0
    cands = [0]
    for step in range(1, break_step + 1):
        #print " ", step, "( max =", max_step, ")"
        max_step = max(step, max_step)

        mod = 1 << (4 * step)
        mask = mod - 1

        cands_next = []
        for p, new_digit in product(cands, p_ranges[-step]):
            pval = (new_digit << ((step - 1) * 4)) | p

            if check_level >= 1:
                qval = solve_linear(pval, N & mask, mod)
                if qval is None or not check_val(qval, mask, qmask_msk, qmask_val):
                    continue

            if check_level >= 2:
                val = solve_linear(E, 1 + K * (N - pval - qval + 1), mod)
                if val is None or not check_val(val, mask, dmask_msk, dmask_val):
                    continue

            if check_level >= 3:
                val = solve_linear(E, 1 + Kp * (pval - 1), mod)
                if val is None or not check_val(val, mask, dpmask_msk, dpmask_val):
                    continue

            if check_level >= 4:
                val = solve_linear(E, 1 + Kq * (qval - 1), mod)
                if val is None or not check_val(val, mask, dqmask_msk, dqmask_val):
                    continue

                if pval * qval == N:
                    print "Kq =", Kq
                    print "pwned"
                    print "p =", pval
                    print "q =", qval
                    p = pval
                    q = qval
                    d = invmod(E, (p - 1) * (q - 1))
                    coef = invmod(p, q)

                    from Crypto.PublicKey import RSA
                    print RSA.construct(map(long, (N, E, d, p, q, coef))).exportKey()
                    quit()

            cands_next.append(pval)

        if not cands_next:
            return False
        cands = cands_next
    return True



def check_val(val, mask, mask_msk, mask_val):
    test_mask = mask_msk & mask
    test_val = mask_val & mask
    return val & test_mask == test_val


# K = 4695
# Kp = 15700
# Kq = 5155

for K in range(1, E):
    if K % 100 == 0:
        print "checking", K
    if search(K, 0, 0, check_level=2, break_step=20):
        print "K =", K
        break

for Kp in range(1, E):
    if Kp % 1000 == 0:
        print "checking", Kp
    if search(K, Kp, 0, check_level=3, break_step=30):
        print "Kp =", Kp
        break

for Kq in range(1, E):
    if Kq % 100 == 0:
        print "checking", Kq
    if search(K, Kp, Kq, check_level=4, break_step=9999):
        print "Kq =", Kq
        break

