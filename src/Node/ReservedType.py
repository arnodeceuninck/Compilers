from src.Node.AST import AST


class Break(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: break", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "; break"

    def llvm_code(self):
        AST.llvm_output += self.comments()
        pass


class Continue(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: Continue", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                        color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "; break"

    def llvm_code(self):
        AST.llvm_output += self.comments()
        pass
