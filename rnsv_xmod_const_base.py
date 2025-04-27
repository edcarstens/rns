from xmod import xmod

class rnsv_xmod_const_base(xmod):
    def __init__(self, x, m, rnsv_base):
        assert(isinstance(x, int))
        assert(isinstance(m, int))
        self.rnsv_base = rnsv_base
        self.name = f"xmod{m}_const{x}"
        super().__init__(x, m)
        self.declare_and_assign_me()
    def __str__(self):
        return self.name
    def declare_and_assign_me(self): ## defined in fast subclass
        pass
