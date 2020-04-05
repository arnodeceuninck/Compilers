from src.Node.AST import *


class Operate(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def getType(self, args):
        if args[0] == args[1]:
            return args[0]
        elif "float" in args and "int" in args:
            return "float"
        else:
            return "unknown"

    def generate_LLVM(self, ast):
        is_float = (ast.getType() == "float")

        # execute operator
        type = ast.getLLVMType()
        # Operate on the children
        return ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", ast.children[0],
                                                  "%", str(ast.children[1]))


class BMinus(Operate):
    def __init__(self, value="-"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] - args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fsub {} {}{}, {}{}\n"
        return "{}{} = sub {} {}{}, {}{}\n"


class BPlus(Operate):
    def __init__(self, value="+"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] + args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fadd {} {}{}, {}{}\n"
        return "{}{} = add {} {}{}, {}{}\n"


class Div(Operate):
    def __init__(self, value="/"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] / args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fdiv {} {}{}, {}{}\n"
        return "{}{} = sdiv {} {}{}, {}{}\n"


class Mult(Operate):
    def __init__(self, value="*"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] * args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fmul {} {}{}, {}{}\n"
        return "{}{} = mul {} {}{}, {}{}\n"


class Mod(Operate):
    def __init__(self, value="%"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] % args[1]

    def getType(self, args):
        return "int"

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = frem {} {}{}, {}{}\n"
        return "{}{} = srem {} {}{}, {}{}\n"
