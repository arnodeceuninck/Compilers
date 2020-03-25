"""
!
"""
from src.ErrorListener import RerefError


class Node:
    id = 0

    def __init__(self, value="", color="#9f9f9f"):
        self.value = value
        self.color = color
        self.funct = None

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
        self.funct = None

    def __str__(self):
        return '[label="Constant {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def set_value(self, value):
        self.value = value


class CInt(Constant):
    def __init__(self, value=0):
        Constant.__init__(self, int(round(int(value))))
        self.type = "int"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type

    def set_value(self, value):
        self.value = int(round(value))


class CFloat(Constant):
    def __init__(self, value=0):
        Constant.__init__(self, float(value))
        self.type = "float"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type

    def set_value(self, value):
        self.value = float(value)


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
        self.funct = None

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        return args[0]  # Only one type as argument


class UPlus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fadd {} {}{}, 0.0\n"
        return "{}{} = add {} {}{}, 0\n"

class UMinus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)
        self.funct = lambda args: -args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fsub {} 0.0, {}{}\n"
        return "{}{} = sub {} 0, {}{}\n"


class UNot(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)
        self.funct = lambda args: not args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fcmp oeq {} {}{}, 0.0\n"
        return "{}{} = icmp eq {} {}{}, 0\n"


class UDeref(Unary):
    def __init__(self, value="&"):
        Unary.__init__(self, value)

    def getType(self, args):
        return args[0] + "*"


class UReref(Unary):
    def __init__(self, value="*"):
        Unary.__init__(self, value)

    def getType(self, args):
        if args[0][len(args[0]) - 1] != "*":
            raise RerefError()
        return args[0][:len(args[0]) - 1]


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
        if args[0] == args[1]:
            return args[0]
        elif "float" in args and "int" in args:
            return "float"
        else:
            return "unknown"


class LessT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] < args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp olt {} {}{}, {}{}\n"
        return "{}{} = icmp slt {} {}{}, {}{}\n"


class MoreT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] > args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp ogt {} {}{}, {}{}\n"
        return "{}{} = icmp sgt {} {}{}, {}{}\n"


class LessOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] <= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp ole {} {}{}, {}{}\n"
        return "{}{} = icmp sle {} {}{}, {}{}\n"


class MoreOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] >= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp oge {} {}{}, {}{}\n"
        return "{}{} = icmp sge {} {}{}, {}{}\n"


class Equal(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] == args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp oeq {} {}{}, {}{}\n"
        return "{}{} = icmp eq {} {}{}, {}{}\n"


class NotEqual(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] != args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp one {} {}{}, {}{}"
        return "{}{} = icmp ne {} {}{}, {}{}\n"


class LogicAnd(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] and args[1]

    def get_LLVM(self, is_float=False):
        return "{}{} = icmp and {} {}{}, {}{}\n"


class LogicOr(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] or args[1]

    def get_LLVM(self, is_float=False):
        return "{}{} = icmp or {} {}{}, {}{}\n"


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

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fsub {} {}{}, {}{}\n"
        return "{}{} = sub {} {}{}, {}{}\n"


class BPlus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] + args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fadd {} {}{}, {}{}\n"
        return "{}{} = add {} {}{}, {}{}\n"


class Div(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] / args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fdiv {} {}{}, {}{}\n"
        return "{}{} = sdiv {} {}{}, {}{}\n"


class Mult(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] * args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fmul {} {}{}, {}{}\n"
        return "{}{} = mul {} {}{}, {}{}\n"


class Mod(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] % args[1]

    def getType(self, args):
        return "int"

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = frem {} {}{}, {}{}\n"
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
