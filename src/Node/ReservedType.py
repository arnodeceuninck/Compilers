from src.Node.AST import AST, For, While


class ReservedType(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#adff76")

    def __str__(self):
        return '{name}[label="Reserved Word: {value}", fillcolor="{color}"] \n'.format(name=self.id(), value=self.value,
                                                                                       color=self.color)


class Break(ReservedType):
    def __init__(self, value="break"):
        ReservedType.__init__(self, value)

    def __str__(self):
        return '{name}[label="Reserved Word: break", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "\t; break\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # The loop in which the user situates itself
        loop = self
        # Get the loop in which the break situates itself, it can be situated in an if statement
        while not isinstance(loop, (While, For)):
            loop = loop.parent

        # Handle the break
        end_label = "end" + str(loop.id())
        loop.goto(end_label)


class Continue(ReservedType):
    def __init__(self, value=""):
        ReservedType.__init__(self, "continue")

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "\t; continue\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # The loop in which the user situates itself
        loop = self
        # Get the loop in which the break situates itself, it can be situated in an if statement
        while not isinstance(loop, (While, For)):
            loop = loop.parent

        # Handle the continue
        loop_label = "loop" + str(loop.id())
        loop.goto(loop_label)


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

    def llvm_code(self):
        # If we find that the return has no children then return a void type
        if not self.children:
            AST.llvm_output += self.comments()
            AST.llvm_output += "\tret void\n"
            return

        # Generate code for the only child of return
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        # The loop in which the user situates itself
        code = "\tret " + self[0].get_llvm_type() + " " + self[0].variable()
        AST.llvm_output += code


class Void(ReservedType):
    def __init__(self, value=""):
        ReservedType.__init__(self, "void")

    def get_type(self):
        return "void"

    def get_llvm_template(self):
        return "void"

    def comments(self, comment_out: bool = True) -> str:
        return "\t; void\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()
