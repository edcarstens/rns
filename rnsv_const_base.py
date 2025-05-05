from rns import rns

class rnsv_const_base(rns):
    def __init__(self, x, parent):
        assert(isinstance(x, int))
        self.parent = parent
        self.name = f"{parent.struct_name}_const{x}"
        super().__init__(x, self.parent.base)
        self.declare_and_assign_me()
    def __str__(self):
        return self.name
    def declare_and_assign_me(self): ## defined in fast subclass
        pass
