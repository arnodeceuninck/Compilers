from src.Node.AST import AST, For, While


class ReservedType(AST):
    def __init__(self, value=""):
        AST.__init__(self, value)

    def __str__(self):
        return "Reserved Word: {value}".format(value=self.value)


class Break(ReservedType):
    def __init__(self, value="break"):
        ReservedType.__init__(self, value)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "\t; break\n"



class Continue(ReservedType):
    def __init__(self, value=""):
        ReservedType.__init__(self, "continue")

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "\t; continue\n"


class Return(ReservedType):
    def __init__(self, value=""):
        ReservedType.__init__(self, "return")

    def get_type(self):
        # If the return has a child then we return the type of that child else we return a void type
        if self.children:
            # The type is the type of the only child
            return self[0].get_type()
        return "void"

    def get_llvm_template(self):
        return "\tret {type} {temp}\n"

    def comments(self, comment_out: bool = True) -> str:
        return "\t; return\n"


class Void(ReservedType):
    def __init__(self, value=""):
        ReservedType.__init__(self, "void")

    def get_type(self):
        return "void"

    def get_llvm_template(self):
        return "void"

    def comments(self, comment_out: bool = True) -> str:
        return "\t; void\n"
