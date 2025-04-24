from xmod import xmod

class rns:
    base = [4,3,5]       ## ex default base
    init_integer = True
    def __init__(self, x, base=None):
        if base:
            self.base = base
        if isinstance(x, int):
            self.xmods = [xmod(x,m) for m in self.base]
            self.integer = x
        else:
            self.xmods = x
            self.base = [z.m for z in self.xmods]
            if self.init_integer:
                self.__class__.init_integer = False
                jnk,jnk,i = self.mixed_radix()
                self.integer = i
                self.__class__.init_integer = True
            else:
                self.integer = None
    def __repr__(self):
        s = [repr(z) for z in self.xmods]
        return f"{type(self)}([{','.join(s)}])"
    def __str__(self):
        s = [str(z) for z in self.xmods]
        if self.integer is not None:
            sint = f"  ({self.integer})"
        else:
            sint = ""
        return f"[{',  '.join(s)}]" + sint
    def __eq__(self, other):
        if isinstance(other, int):
            y = type(self)(other, self.base)
        else:
            y = other
        return self.base == y.base and self.xmods == y.xmods
    def __ne__(self, other):
        return not self==other
    def copy(self):
        return type(self)(self.xmods.copy())
    def __neg__(self):
        return type(self)([-z for z in self.xmods])
    def __add__(self, other):
        if isinstance(other, int):
            return type(self)([x+other for x in self.xmods])
        else:
            return type(self)([x+y for x,y in zip(self.xmods, other.xmods)])
    def __radd__(self, other):
        return self + other
    def __iadd__(self, other):
        if isinstance(other, int):
            for x in self.xmods:
                x += other
        else:
            for x,y in  zip(self.xmods, other.xmods):
                x += y
        return self
    def __sub__(self, other):
        if isinstance(other, int):
            return type(self)([x-other for x in self.xmods])
        else:
            return type(self)([x-y for x,y in zip(self.xmods, other.xmods)])
    def __rsub__(self, other):
        return -self + other
    def __isub__(self, other):
        if isinstance(other, int):
            for x in self.xmods:
                x -= other
        else:
            for x,y in  zip(self.xmods, other.xmods):
                x -= y
        return self
    def __mul__(self, other):
        if isinstance(other, int):
            return type(self)([x*other for x in self.xmods])
        else:
            return type(self)([x*y for x,y in zip(self.xmods, other.xmods)])
    def __rmul__(self, other):
        return self * other
    def __imul__(self, other):
        if isinstance(other, int):
            for x in self.xmods:
                x *= other
        else:
            for x,y in  zip(self.xmods, other.xmods):
                x *= y
        return self
    def mulinv(self):
        return type(self)([x.mulinv() for x in self.xmods])
    def __truediv__(self, other):
        if isinstance(other, int):
            return type(self)([x/other for x in self.xmods])
        else:
            return type(self)([x/y for x,y in zip(self.xmods, other.xmods)])
    def __rtruediv__(self, other):
        if isinstance(other, int):
            return type(self)([other/x for x in self.xmods])
        else:
            return type(self)([y/x for x,y in zip(self.xmods, other.xmods)])
    def __itruediv__(self, other):
        if isinstance(other, int):
            for x in self.xmods:
                x /= other
        else:
            for x,y in  zip(self.xmods, other.xmods):
                x /= y
        return self
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            #print('slice')
            return type(self)(self.xmods[idx])
        else:
            return self.xmods[idx]
    def __setitem__(self, idx, val):
        #print(f"__setitem__ called with {idx} and {val}")
        if isinstance(idx, slice):
            step = 1 if idx.step is None else idx.step
            start = 0 if idx.start is None else idx.start
            stop = len(self) if idx.stop is None else idx.stop
            j = 0
            if isinstance(val, int):
                for i in range(start,stop,step):
                    self.xmods[i] = xmod(val, self.base[j])
                    j += 1
            elif isinstance(val, type(self)):
                for i in range(start,stop,step):
                    self.xmods[i] = val.xmods[j]
                    j += 1
            else:
                for i in range(start,stop,step):
                    self.xmods[i] = val[j]
                    j += 1
        else:
            if isinstance(val, int):
                self.xmods[idx] = xmod(val, self.base[idx])
            else:
                self.xmods[idx] = val
    def __len__(self):
        return len(self.xmods)
    def mixed_radix(self, p=1, idx=0):
        """
        Calculate mixed-radix representation for this RNS number
        :return: mixed-radix representation, integer equivalent
        """
        z = self[idx].x
        m = self[idx].m
        x = self.copy()
        if (len(self) > idx+1):
            x[idx+1:] = (self[idx+1:] - z)/m
            #print(f"x={x}")
            v,b,i = x.mixed_radix(p*m, idx+1)
            vs = [z] + v
            bs = [p] + b
            i += z*p
        else:
            vs = [z]
            bs = [p]
            i = z*p
        return vs,bs,i
    
        
