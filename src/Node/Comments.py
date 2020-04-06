from src.Node.AST import *


class Comments(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "38A038")


class SingleLine(Comments):
    def __init__(self, value):
        Comments.__init__(self, value)

    def get_LLVM(self):
        return ";" + self.value

    def llvm_code(self):
        return ";; " + self.value

class Multiline(Comments):
    def __init__(self, value):
        Comments.__init__(self, value)

    def get_LLVM(self):
        commentLLVM = ""
        for line in self.value:
            commentLLVM += "; " + self.value
        return commentLLVM

    def llvm_code(self):
        code = ""
        for line in self.code:
            code += ";; " + line
        return code