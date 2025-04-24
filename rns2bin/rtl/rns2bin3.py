## Demonstrate the algorithm to convert RNS to binary
## for RNS base, {8,9,5,7,13,11,17}.

import sys
sys.path.append('c:/users/edcar/rns')
from rns import rns
from xmod import xmod

def _rnsmod_help(xx, mm, iters):
    ai = -xx
    m = xx.base[0]
    mmi = xmod(mm, m).mulinv()
    #mmi = xx._mulinv(mm, m)
    k = ai[0] * mmi
    debug(f"k={k}, m={m}")
    #nx = xx.remove_mod()
    nx = (xx[1:] + k.x * mm) / m
    debug(f"nx = {nx}")
    if iters == 1:
        return nx
    return _rnsmod_help(nx, mm, iters - 1)

def rnsmod(x, mm, iters):
    ## first we calculate the product of the moduli used in the iterations (mod mm)
    p = 1
    for m in x.base[0:iters]:
        p = (p*m) % mm
    debug(f"p = {p}")
    sign = 1
    if p > mm//2:
        ## use negative number for p
        p = mm - p
        sign = -1
    xx = x*p ## so that the iteration divisions cancel out p
    nx = _rnsmod_help(xx, mm, iters)
    return nx,sign

def normalize(z,mm):
    if mm==16:
        return normalize_full_16(z)
    if (z.integer > mm + 3):
        print(f"WARNING - z > {mm + 3}")
        exit()
    if z == mm:
        z = z - mm
    if z == mm + 1:
        z = z - mm
    if z == mm + 2:
        z = z - mm
    if z == mm + 3:
        z = z - mm
    return z

def normalize_full_16(z):
    # use new mod 16 to calculate z % 16
    # z is in RNS base, {17,11}
    tmp = z - z[0].x
    x = tmp[1:]/z[0].m
    x16 = xmod(x[0].x, 16)
    z16 = xmod(z[0].x, 16) + x16
    return rns(z16.x, z.base)

def negate(z,s,mm):
    if (s < 0):
        return mm - z
    return z

def debug(s, level=1):
    if level <= debug_level:
        print(s)

def rns2bin(x):
    base = [8,9,7,13,5,17,11]
    assert(isinstance(x, int))
    y = rns(x, base)
    debug(f"y={y}")

    ## convert the first residue (mod 8) to x[2:0]
    x20 = y[0].x
    y = y-x20
    y = y[1:]
    y = y/8
    debug(f"y={y}")

    ## zero is special case
    y_is_zero = (y==0)

    ## run the rnsmod algorithm modulo 2^4 = 16 for 9,5,7, and 13
    z0,s0 = rnsmod(y, 16, 4)
    debug(f"z0={z0}")

    if y_is_zero:
        z0 = rns(0, z0.base)
    else:
        z0 = normalize(z0, 16)
    debug(f"z0={z0}")  ## still doesn't account for sign
    
    z1,s1 = rnsmod(y, 256, 4)
    debug(f"z1={z1}")

    z2,s2 = rnsmod(y, 256*16, 4)
    debug(f"z2={z2}")

    r1 = (z1 - z0) / 16
    r1 = normalize(r1, 16)
    
    r2 = (z2 - r1*16 - z0) / 256
    r2 = normalize(r2, 16)
    debug(f"r1={r1}")
    debug(f"r2={r2}")

    ## Now account for sign for z0,r1,r2
    if y_is_zero:
        z0s = rns(0, z0.base)
    else:
        z0s = negate(z0, s0, 16)
    if y_is_zero:
        r1s = rns(0, r1.base)
    else:
        #r1s = (negate(r1*16+z0, s1, 256) - z0s)/16
        r1s = 15 - r1  ## the math for above reduces to this
    if y_is_zero:
        r2s = rns(0, r2.base)
    else:
        #r2s = (negate(r2*256+r1*16+z0, s2, 16*256) - z0s - r1s*16)/256
        r2s = 15 - r2  ## the math for above reduces to this
    r = z0s + r1s*16 + r2s*256
    
    debug(f"z0s={z0s}")
    debug(f"r1s={r1s}")
    debug(f"r2s={r2s}")
    debug(f"r={r}")
    # reduced version of y to match RNS base = [11,17]
    #ry = y.remove_mod().remove_mod().remove_mod().remove_mod()
    ry = y[-2:]
    debug(f"ry={ry}")
    r3 = (ry - r) / 4096
    debug(f"r3={r3}")

    x63 = z0s.integer
    x10_7 = r1s.integer
    x14_11 = r2s.integer
    x18_15 = r3.integer

    debug(f"x[2:0] = {bin(x20)} = {x20}")
    debug(f"x[6:3] = {bin(x63)} = {x63}")
    debug(f"x[10:7] = {bin(x10_7)} = {x10_7}")
    debug(f"x[14:11] = {bin(x14_11)} = {x14_11}")
    debug(f"x[18:15] = {bin(x18_15)} = {x18_15}")
    ## Final check
    finalx = x18_15*(2**15) + x14_11*(2**11) + x10_7*(2**7) + x63*8 + x20
    debug(f"finalx={finalx}  x={x}")
    assert(finalx == x)


## Testing
debug_level = 1 # no debug info
for x in range(700200*8, 700201*8, 8):
    if x%800==0:
        print(f"\n{x}", end='', flush=True)
    elif x%80==0:
        print('.', end='', flush=True)
    rns2bin(x)

## works up to 5602087
