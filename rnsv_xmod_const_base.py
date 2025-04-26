from xmod import xmod

class rnsv_xmod_const_base(xmod):
    def __init__(self, x, m, parent):
        assert(isinstance(x, int))
        assert(isinstance(m, int))
        self.parent = parent
        self.name = f"xmod_const{x}"
        super().__init__(x, m)
        self.declare_and_assign_me()
    def __str__(self):
        return self.name
    def declare_and_assign_me(self): ## defined in fast subclass
        pass
