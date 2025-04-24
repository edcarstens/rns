## Demonstrate the algorithm to convert RNS to binary
## for RNS base, {8,9,5,7,13,11,17}.

from rns import rns
from xmod import xmod

def _rnsmod_help(xx, mm, iters):
    ai = -xx
    m = xx.base[0]
    mmi = xmod(mm, m).mulinv()
    #mmi = xx._mulinv(mm, m)
    k = ai[0] * mmi
    print(f"k={k}, m={m}")
    #nx = xx.remove_mod()
    nx = (xx[1:] + k.x * mm) / m
    print(f"nx = {nx}   ({nx.integer})")
    if iters == 1:
        return nx
    return _rnsmod_help(nx, mm, iters - 1)

def rnsmod(x, mm, iters):
    ## first we calculate the product of the moduli used in the iterations (mod mm)
    p = 1
    for m in x.base[0:iters]:
        p = (p*m) % mm
    print(f"p = {p}")
    sign = 1
    if p > mm//2:
        ## use negative number for p
        p = mm - p
        sign = -1
    xx = x*p ## so that the iteration divisions cancel out p
    nx = _rnsmod_help(xx, mm, iters)
    return nx,sign

def normalize(z,s,mm):
    if s < 0: ## sign=-1
        if (z.integer > mm + 0):
            print(f"WARNING - z > {mm + 0}")
            #exit()
            z = mm - z
        #elif (z.integer == mm + 1):
        #    z = z - 2
        else:
            z = mm - z
    else:
        if (z.integer > mm + 0):
            print(f"WARNING - z > {mm + 1}")
            #exit()
        #elif (z.integer == mm + 1):
        #    z = z - mm
        elif (z.integer == mm):
            z = z - mm
    return z

def rns2bin(x):
    base = [8,9,7,13,5,17,11]
    assert(isinstance(x, int))
    y = rns(x, base)
    print(f"y={y}  ({y.integer})")
    #mrv,mrb,mri = y.mixed_radix()
    #print(f"y={y}  ({mri})")

    ## convert the first residue (mod 8) to x[2:0]
    x20 = y[0].x
    y = y-x20
    y = y[1:]
    y = y/8
    print(f"y={y}  ({y.integer})")

    ## zero is special case
    y_is_zero = (y==0)

    ## run the rnsmod algorithm modulo 2^4 = 16 for 9,5,7, and 13
    z0,s0 = rnsmod(y, 16, 4)
    print(f"z0={z0}")

    if y_is_zero:
        z0 = rns(0, z0.base)
    else:
        z0 = normalize(z0, s0, 16)
    print(f"z0={z0}")
     
    z1,s1 = rnsmod(y, 256, 4)
    print(f"z1={z1}")
    if y_is_zero:
        z1 = rns(0, z1.base)
    else:
        z1 = normalize(z1, s1, 256)
    print(f"z1={z1}")
    z2,s2 = rnsmod(y, 256*16, 4)
    print(f"z2={z2}")
    if y_is_zero:
        z2 = rns(0, z2.base)
    else:
        z2 = normalize(z2, s2, 256*16)
    print(f"z2={z2}")

    r1 = (z1 - z0) / 16
    r2 = (z2 - z1) / 256

    ## Now take care of sign for z0,r1,r2,r3
    print(f"z0={z0}")
    print(f"r1={r1}")
    print(f"r2={r2}")
    # reduced version of y to match RNS base = [11,17]
    #ry = y.remove_mod().remove_mod().remove_mod().remove_mod()
    ry = y[-2:]
    print(f"ry={ry}")
    #nz2 = z0 + r1*16 + r2*256
    r3 = (ry - z2) / 4096
    print(f"r3={r3}")

    x63 = z0.integer
    x10_7 = r1.integer
    x14_11 = r2.integer
    x18_15 = r3.integer

    print(f"x[2:0] = {bin(x20)} = {x20}")
    print(f"x[6:3] = {bin(x63)} = {x63}")
    print(f"x[10:7] = {bin(x10_7)} = {x10_7}")
    print(f"x[14:11] = {bin(x14_11)} = {x14_11}")
    print(f"x[18:15] = {bin(x18_15)} = {x18_15}")
    ## Final check
    finalx = x18_15*(2**15) + x14_11*(2**11) + x10_7*(2**7) + x63*8 + x20
    print(f"finalx={finalx}  x={x}")
    assert(finalx == x)


## Testing
#for x in range(32768*2 - 8*100, 32768*2 + 8*14 + 1):
#for x in range(65536 - 8*2000, 65536 - 8*900):
#for x in range(30000, 40000):
#    rns2bin(x)

## works up to 34807
#rns2bin(34807)
rns2bin(34808)

#rns2bin(31011)

