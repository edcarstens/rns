from prime_factorization import is_relatively_prime

class xmod:
    def __init__(self, x, m):
        self.x = x % m
        self.m = m
        self.max_recursions = 99
    def __repr__(self):
        return f"{type(self)}({self.x},{self.m})"
    def __str__(self):
        return f"{self.x} (mod {self.m})"
    def __eq__(self, other):
        return self.x == other.x and self.m == other.m
    def __ne__(self, other):
        return not self==other
    def copy(self):
        return type(self)(self.x,self.m)
    def __neg__(self):
        x = self.x if self.x==0 else self.m-self.x
        return type(self)(x,self.m)
    def __add__(self, other):
        if isinstance(other, int):
            y = other
        else:
            y = other.x
            assert(self.m == other.m)
        x = (self.x + y) % self.m
        return type(self)(x,self.m)
    def __sub__(self, other):
        if isinstance(other, int):
            y = other
        else:
            y = other.x
            assert(self.m == other.m)
        x = (self.x - y) % self.m
        return type(self)(x,self.m)
    def __mul__(self, other):
        if isinstance(other, int):
            y = other
        elif isinstance(other, type(self)):
            y = other.x
            assert(self.m == other.m)
        x = (self.x * y) % self.m
        return type(self)(x,self.m)
    def __radd__(self, other):
        return self+other
    def __rmul__(self, other):
        return self*other
    def __rsub__(self, other):
        return -self + other
    def __iadd__(self, other):
        if isinstance(other, int):
            y = other
        elif isinstance(other, type(self)):
            y = other.x
            assert(self.m == other.m)
        self.x = (self.x + y) % self.m
        return self
    def __imul__(self, other):
        if isinstance(other, int):
            y = other
        elif isinstance(other, type(self)):
            y = other.x
            assert(self.m == other.m)
        self.x = (self.x * y) % self.m
        return self
    def __isub__(self, other):
        if isinstance(other, int):
            y = other
        elif isinstance(other, type(self)):
            y = other.x
            assert(self.m == other.m)
        self.x = (self.x - y) % self.m
        return self
    def _find_f(self, y, m, delta):
        while ((y != 1) and not is_relatively_prime(y,m)):
            y = (y + delta) % m
        return y
    def _mulinv(self, recursions):
        if recursions > self.max_recursions:
            raise Exception(f"exceeded max recursions ({self.max_recursions}) in _mulinv")
        x = self.x
        m = self.m
        if x==1:
            return self.copy()
        if not is_relatively_prime(x,m):
            raise Exception(f"{x} is not relatively prime to {m}, so {x} does not have a multiplicative inverse")
        y = m//x
        yn = self._find_f(y, m, -1)
        zn = (x * yn) % m
        abs_zn = min(m-zn,zn)
        if (abs_zn != 1 or yn == 1):
            abs_zp = x
            yp = y
            while abs_zp >= x:
                yp = (yp + 1) % m
                yp = self._find_f(yp, m, 1)
                zp = (x*yp) % m
                abs_zp = min(m-zp,zp)
        else:
            yp = yn
            zp = zn
        if yn==1:
            yn = yp
            zn = zp
        if zp == 1:
            return type(self)(yp,m)
        if zp == m - 1:
            return type(self)(m - yp, m)
        if zn == 1:
            return type(self)(yn, m)
        if zn == m - 1:
            return type(self)(m - yn, m)
        mzp = m - zp
        mzn = m - zn
        abs_zp = min(mzp,zp)
        abs_zn = min(mzn,zn)
        if abs_zp <= abs_zn:
            z = zp
            y = yp
        else:
            z = zn
            y = yn
        mz = m - z
        if z <= mz:
            zmod = type(self)(z,m)
            rvx = (y*zmod._mulinv(recursions+1).x) % m
            return type(self)(rvx,m)
        ## keep track of negative sign
        mzmod = type(self)(mz,m)
        #print(f"mzmod={mzmod}")
        #tmp = mzmod._mulinv(recursions+1)
        #print(f"tmp={tmp}")
        rvx = ((m - y)*mzmod._mulinv(recursions+1).x) % m
        return type(self)(rvx,m)
    
    def mulinv(self):
        """
        returns multiplicative inverse of self (creates/returns a new object)
        """
        return self._mulinv(0)

    def __truediv__(self, other):
        """
        self/other returns self*other.mulinv()
        """
        if isinstance(other, int):
            y = type(self)(other, self.m)
        elif isinstance(other, type(self)):
            y = other
            assert(self.m == other.m)
        return self * y.mulinv()
    def __rtruediv__(self, other):
        return self.mulinv() * other
    def __itruediv__(self, other):
        if isinstance(other, int):
            y = type(self)(other, self.m)
        elif isinstance(other, type(self)):
            y = other
            assert(self.m == other.m)
        self *= y.mulinv()
        return self
    def onehot(self):
        rv = ''
        for idx in range(self.m-1,-1,-1):
            rv += '1' if (self.x == idx) else '0'
        return rv
