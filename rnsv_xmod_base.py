from rns import rns
class rnsv_xmod_base:
    def __init__(self, name, m, rnsv_base, parent=None, do_declaration=True):
        self.name = name
        self.m = m
        self.rnsv_base = rnsv_base
        self.parent = parent
        self.comb_comment = ""
    def __str__(self):
        return self.name
    def op_map(self, fct):
        name = self.name
        m = self.m
        rmap = {}
        for x in range(m):
            y = fct(x) % m
            xname = f"{name}[{x}]"
            if y in rmap:
                rmap[y].append(xname)
            else:
                rmap[y] = [xname]
        r = []
        for x in range(m-1,-1,-1):
            if x in rmap:
                r.append('|'.join(rmap[x]))
            else:
                r.append("1'b0")
        return r
    def map2comb(self, fct, op, x=None):
        """
        Subclass defines this function, which calls op_map
        :param fct: function
        :param op: operation (neg, add, mul)
        :param x: int type argument to operation
        :return:
        """
        pass
    def create(self, name, _m=0):
        m = _m if _m else self.m
        return type(self)(name, m, self.rnsv_base, self.parent)
    def copy(self):
        return self.create(self.name)
    def connect_inst(self, other, modname):
        """
        Subclass defines this function
        """
        pass
    def nop(self):
        return self.map2comb(lambda x: x, 'nop')
    def __neg__(self):
        return self.map2comb(lambda x: -x, 'neg')
    def __add__(self, other):
        if isinstance(other, int):
            return self.map2comb(lambda x: x+other, 'add', other)
        elif isinstance(other, type(self)):
            # hookup modadd modules
            return self.connect_inst(other, "modadd")
        else:
            raise Exception(f"{other} type is not int or rnsv_var")
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        return self + (-other)
    def __rsub__(self, other):
        return -self + other
    def __mul__(self, other):
        if isinstance(other, int):
            return self.map2comb(lambda x: x*other, 'mul', other)
        elif isinstance(other, type(self)):
            return self.connect_inst(other, "modmul")
        else:
            raise Exception(f"{other} type is not int or rnsv_var")
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        if isinstance(other, int):
            self.comb_comment = f"xmod{self.m}: div({other})"
            x = rns(other, [self.m])
            xi = x.mulinv()
            (mrv,mrb,mri) = xi.mixed_radix()
            #print(f"mri={mri}")
            return self * mri
        else:
            raise Exception(f"Division operator (/) only supports int type, encountered {other}")
    def map_to_mod_helper(self, m, start_idx=0):
        if m >= self.m - start_idx:
            bitr = f"{self.m - 1}:{start_idx}"
            if self.m - 1 == start_idx:
                bitr = start_idx
            return f"{{{m-self.m+start_idx}'b0, {self.name}[{bitr}]}}"
        else:
            z = self.map_to_mod_helper(m, start_idx + m)
            return f"{self.name}[{m-1 + start_idx}:{start_idx}] | {z}"
    def map_to_mod(self, m):
        if m == self.m:
            return self.name
        if m > self.m:
            return f"{{{m - self.m}'b0, {self.name}}}"
        return f"{self.name}[{m-1}:0] | {self.map_to_mod_helper(m,m)}"
    def __eq__(self, other):
        if isinstance(other, int):
            idx = other % self.m
            return f"{self.name}[{idx}]"
        return f"(| ({self.name} & {other.name}))"
    def __ne__(self, other):
        if isinstance(other, int):
            idx = other % self.m
            return f"~{self.name}[{idx}]"
        return f"~({self.name} & {other.name})"
    
            
