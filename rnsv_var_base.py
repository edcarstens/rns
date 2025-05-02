from rns import rns
class rnsv_var_base:
    def __init__(self, name, parent):
        self.base = parent.base
        self.name = name
        self.parent = parent
#        self.declared = False
        self.includes = parent.includes
        self.declarations = parent.declarations
        self.instances = parent.instances
        self.comb = parent.comb
        self.sva = parent.sva
        self.my_slice = None
        self.comb_comment = ""
    def __str__(self):
        return self.name
    def op_map(self, fct, m):
        vname = f"{self.name}.x{m}"
        rmap = {}
        for x in range(m):
            y = fct(x) % m
            xname = f"{vname}[{x}]"
            if y in rmap:
                rmap[y].append(xname)
            else:
                rmap[y] = [xname]
        r = []
        for x in range(m-1,-1,-1):
            if x in rmap:
                r.append(f"{'|'.join(rmap[x])}")
            else:
                r.append("1'b0")
        return r
    def map2comb(self, op, x=None):
        """
        Subclass defines this function, which calls op_map
        :param fct: function
        :param op: operation (neg, add, mul)
        :param x: int type argument to operation
        :return:
        """
        pass
    def create(self, name, parent=None):
        parent = parent if parent else self.parent
        return type(self)(name, parent)
    def copy(self):
        rv = self.create(self.name)
        rv.parent = self.parent
#        rv.declared = self.declared
        rv.includes = self.includes
        rv.declarations = self.declarations
        rv.instances = self.instances
        rv.comb = self.comb
        rv.sva = self.sva
        rv.my_slice = self.my_slice
        #rv.n = self.n
        rv.xmods = [z.copy() for z in self.xmods]  ## deep copy needed here?
        for xmod in rv.xmods:
            xmod.parent = rv
        return rv
    def connect_inst(self, other, modname):
        "Subclass must define this"
        pass
    def resolve_slice(self, s1, s2):
        if s1 is None:
            return s2
        if s2 is None:
            return s1
        if s1 == s2:
            return s1
        raise Exception(f"Slices differ: {s1} vs {s2}")
    def get_slice(self, length, other=None):
        s = self.my_slice
        if isinstance(other, type(self)):
            s = self.resolve_slice(s, other.my_slice)
        if s is None:
            return 0,length,1
        start = s.start if s.start else 0
        stop = s.stop if s.stop else length
        step = s.step if s.step else 1
        return start,stop,step
    def _call_nops(self, idxs):
        for idx in range(len(self.xmods)):
            if idx not in idxs:
                self.xmods[idx].nop()
    def assign_xmods_parent(self):
        for xmod in self.xmods:
            xmod.parent = self
    def __neg__(self):
        rv = self.map2comb('neg')
        start,stop,step = self.get_slice(len(self.xmods))
        idxs = []
        for idx in range(start, stop, step):
            rv.xmods[idx] = -self.xmods[idx]
            idxs.append(idx)
        self._call_nops(idxs)
        rv.assign_xmods_parent()
        rv.my_slice = self.my_slice  # propagate the slice
        return rv
    def __lshift__(self, other):
        "Subclass must define this"
        pass
    def __add__(self, other):
        if isinstance(other, int):
            rv = self.map2comb('add', other)
            start,stop,step = self.get_slice(len(self.xmods))
            idxs = []
            for idx in range(start, stop, step):
                rv.xmods[idx] = self.xmods[idx] + other
                idxs.append(idx)
            self._call_nops(idxs)
            rv.assign_xmods_parent()
            rv.my_slice = self.my_slice  # propagate the slice
            return rv
        elif isinstance(other, type(self)):
            # hookup modadd modules
            start,stop,step = self.get_slice(len(self.xmods), other)
            return self.connect_inst(other, "modadd", start,stop,step)
        elif isinstance(other, type(self.xmods[0])):
            return self + (self << other)
        else:
            raise Exception(f"{other} type is not int or rnsv_var")
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        if isinstance(other, type(self.xmods[0])):
            return self - (self << other)
        return self + (-other)
    def __rsub__(self, other):
        return -self + other
    def __mul__(self, other):
        if isinstance(other, int):
            rv = self.map2comb('mul', other)
            start,stop,step = self.get_slice(len(self.xmods))
            idxs = []
            for idx in range(start, stop, step):
                rv.xmods[idx] = self.xmods[idx] * other
                idxs.append(idx)
            self._call_nops(idxs)
            rv.assign_xmods_parent()
            rv.my_slice = self.my_slice  # propagate the slice
            return rv
        elif isinstance(other, type(self)):
            start,stop,step = self.get_slice(len(self.xmods), other)
            return self.connect_inst(other, "modmul", start,stop,step)
        elif isinstance(other, type(self.xmods[0])):
            return self * (self << other)
        else:
            raise Exception(f"{other} type is not int or rnsv_var")
    def __rmul__(self, other):
        return self * other
    def get_base(self):
        if self.my_slice is None:
            return self.base
        else:
            return self.base[self.my_slice]
    def __truediv__(self, other):
        if isinstance(other, int):
            self.comb_comment = f"div({other})"
            x = rns(other, self.get_base())
            xi = x.mulinv()
            (mrv,mrb,mri) = xi.mixed_radix()
            return self * mri
        else:
            raise Exception(f"Division operator (/) only supports int type, encountered {other}")
    def __eq__(self, other):
        start,stop,step = self.get_slice(len(self.xmods), other)
        bits = []
        for idx in range(start, stop, step):
            bits.append(self.xmods[idx] == other)
        return ' & '.join(bits)
    def __ne__(self, other):
        start,stop,step = self.get_slice(len(self.xmods), other)
        bits = []
        for idx in range(start, stop, step):
            bits.append(self.xmods[idx] != other)
        return ' | '.join(bits)
