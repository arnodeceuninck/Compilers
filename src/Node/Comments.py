from src.Node.AST import *


class Comments(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "38A038")


class SingleLine(Comments):
    def __init__(self, value):
        Comments.__init__(self, value)

    def get_LLVM(self):
        return ";" + self.value


class Multiline(Comments):
    def __init__(self, value):
        Comments.__init__(self, value)

    def get_LLVM(self):
        commentLLVM = ""
        for line in self.value:
            commentLLVM += ";" + self.value
        return commentLLVM
