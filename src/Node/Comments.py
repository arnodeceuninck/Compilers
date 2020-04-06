from src.Node.AST import AST


class Comments(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#38A038")


class SingleLine(Comments):
    def __init__(self, value):
        Comments.__init__(self, value)

    def llvm_code(self):
        return ";; " + self.value

class Multiline(Comments):
    def __init__(self, value):
        Comments.__init__(self, value)

    def llvm_code(self):
        code = ""
        for line in self.code:
            code += ";; " + line
        return code