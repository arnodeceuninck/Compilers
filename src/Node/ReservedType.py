from src.Node.AST import AST, For, While


class Break(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: break", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "; break\n"

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


class Continue(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: Continue", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                        color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "; continue\n"

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


class Return(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: return", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                      color=self.color)

    def get_type(self):
        # If the return has a child then we return the type of that child else we return a void type
        if self.children:
            # The type is the type of the only child
            return self.children[0].get_type
        return "void"

    def get_llvm_template(self):
        return "ret {type} {temp}\n"

    def comments(self, comment_out: bool = True) -> str:
        return "; return\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # If we find that the return has no children then return a void type
        if not self.children:
            AST.llvm_output += "ret void\n"
            return

        # Generate code for the only child of return
        self[0].llvm_code()

        # The loop in which the user situates itself
        AST.llvm_output = "ret " + self.value
