"""
!
"""
from src.ErrorListener import RerefError

class Node:
    id = 0

    def __init__(self, value="", color="#9f9f9f"):
        self.value = value
        self.color = color

    @staticmethod
    def get_id():
        Node.id += 1
        return Node.id

    def __str__(self):
        return '[label="{}", fillcolor="{}"] \n'.format(self.value, self.color)


class StatementSequence(Node):
    def __init__(self):
        Node.__init__(self, "Statement Sequence")


class Constant(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#FFD885")

    def __str__(self):
        return '[label="Constant {}", fillcolor="{}"] \n'.format(self.value, self.color)


class CInt(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "int"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type


class CFloat(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "float"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type


class CChar(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "char"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type


class Operator(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '[label="Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        return args[0]  # Only one type as argument


class UPlus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]


class UMinus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]


class UNot(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)
        self.funct = lambda args: not args[0]


class UDeref(Unary):
    def __init__(self, value="&"):
        Unary.__init__(self, value)

    def getType(self, args):
        return args[0] + "*"


class UReref(Unary):
    def __init__(self, value="*"):
        Unary.__init__(self, value)

    def getType(self, args):
        if args[0][len(args[0])-1] != "*":
            raise RerefError()
        return args[0][:len(args[0])-1]

class Print(Unary):
    def __init__(self, value="printf"):
        Unary.__init__(self, value)

    def getType(self, args):
        return "function"


class Binary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class Compare(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        return "int"


class LessT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] < args[1]


class MoreT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] > args[1]


class LessOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] <= args[1]


class MoreOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] >= args[1]


class Equal(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] == args[1]


class NotEqual(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] != args[1]


class LogicAnd(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] and args[1]


class LogicOr(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] or args[1]


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


class BMinus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] - args[1]

    def get_LLVM(self):
        return "{}{} = sub {} {}{}, {}{}\n"


class BPlus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] + args[1]

    def get_LLVM(self):
        return "{}{} = add {} {}{}, {}{}\n"


class Div(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] / args[1]

    def get_LLVM(self):
        return "{}{} = sdiv {} {}{}, {}{}\n"


class Mult(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] * args[1]

    def get_LLVM(self):
        return "{}{} = mul {} {}{}, {}{}\n"


class Mod(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] % args[1]

    def getType(self, args):
        return "int"

    def get_LLVM(self):
        return "{}{} = srem {} {}{}, {}{}\n"


class Assign(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)
        self.declaration = True

    def __str__(self):
        if self.declaration:
            return '[label="Assign Declaration", fillcolor="{}"] \n'.format(self.color)
        return '[label="Assign", fillcolor="{}"] \n'.format(self.color)

    def get_LLVM(self):
        return "store {} {}{}, {}* {}{}\n"


class Variable(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#af93ff")
        self.type = ""
        self.ptr = False  # e.g. int* a (in declaration), &a (deref in rvalue)
        self.const = False
        self.defined = False

        self.reref = False  # e.g. *a

    def __str__(self):
        return '[label="Variable: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        ptr = ""
        if self.ptr:
            ptr = "*"
        return self.type + ptr


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "int"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "float"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "char"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)
