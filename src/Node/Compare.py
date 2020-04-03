from src.Node.Node import *
from src.Node.constant import *


class Compare(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        if args[0] == args[1]:
            return args[0]
        elif "float" in args and "int" in args:
            return "float"
        else:
            return "unknown"

    def generateLLVM(self, ast):
        # execute operator
        type = ast.getLLVMType()
        is_float = ast.getType() == "float"
        # Both variable
        tempSave = "t" + str(ast.node.get_id())
        output = ast.node.get_LLVM(is_float).format("%", tempSave, type, "%", str(ast.children[0]),
                                                    "%", str(ast.children[1]))
        output += CBool().convertString(type).format("%", str(ast), "%", tempSave)
        return output


class LessT(Compare):
    def __init__(self, value="<"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] < args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp olt {} {}{}, {}{}\n"
        return "{}{} = icmp slt {} {}{}, {}{}\n"


class MoreT(Compare):
    def __init__(self, value=">"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] > args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp ogt {} {}{}, {}{}\n"
        return "{}{} = icmp sgt {} {}{}, {}{}\n"


class LessOrEq(Compare):
    def __init__(self, value="<="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] <= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp ole {} {}{}, {}{}\n"
        return "{}{} = icmp sle {} {}{}, {}{}\n"


class MoreOrEq(Compare):
    def __init__(self, value=">="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] >= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp oge {} {}{}, {}{}\n"
        return "{}{} = icmp sge {} {}{}, {}{}\n"


class Equal(Compare):
    def __init__(self, value="=="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] == args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp oeq {} {}{}, {}{}\n"
        return "{}{} = icmp eq {} {}{}, {}{}\n"


class NotEqual(Compare):
    def __init__(self, value="!="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] != args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp one {} {}{}, {}{}"
        return "{}{} = icmp ne {} {}{}, {}{}\n"


class LogicAnd(Compare):
    def __init__(self, value="&&"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] and args[1]

    def get_LLVM(self, is_float=False):
        return "{}{} = icmp and {} {}{}, {}{}\n"

    def generateLLVM(self, ast):
        # execute operator
        type = ast.getLLVMType()
        is_float = (ast.getType() == "float")
        # Both variable
        tempSave1 = "t" + str(ast.node.get_id())
        tempSave2 = "t" + str(ast.node.get_id())
        output = Mult().get_LLVM(is_float).format("%", tempSave1, type, "%",
                                                  str(ast.children[0]),
                                                  "%", str(ast.children[1]))
        output += NotEqual().get_LLVM(is_float).format("%", tempSave2, type, "%", tempSave1,
                                                       "", ast.getNeutral())
        output += CBool().convertString(type).format("%", str(ast), "%", tempSave2)
        return output


class LogicOr(Compare):
    def __init__(self, value="||"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] or args[1]

    def get_LLVM(self, is_float=False):
        return "{}{} = icmp or {} {}{}, {}{}\n"

    def generateLLVM(self, ast):
        # execute operator
        type = ast.getLLVMType()
        is_float = (ast.getType() == "float")
        # Both variable
        tempSave1 = "t" + str(ast.node.get_id())
        tempSave2 = "t" + str(ast.node.get_id())
        output = BPlus().get_LLVM(is_float).format("%", tempSave1, type, "%",
                                                   str(ast.children[0]),
                                                   "%", str(ast.children[1]))
        output += NotEqual().get_LLVM(is_float).format("%", tempSave2, type, "%", tempSave1,
                                                       "", ast.getNeutral())
        output += CBool().convertString(type).format("%", str(ast), "%", tempSave2)
        return output
