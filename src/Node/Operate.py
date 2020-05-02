from src.Node.AST import Binary, AST, BoolClasses
from src.Node.Constant import Constant
from src.ErrorListener import UnknownOperationError


class Operate(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def get_type(self):
        supported_operations = [("int", "int"), ("char", "char"), ("float", "float")]
        if (self[0].get_type(), self[1].get_type()) in supported_operations:
            return self[0].get_type()
        else:
            raise UnknownOperationError(self.value, self[0].get_type(), self[1].get_type())
            # return "UNKNOWN"


class BMinus(Operate):
    def __init__(self, value="-"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] - args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "\t{result} = fsub {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = sub {type} {lvalue}, {rvalue}\n"


class BPlus(Operate):
    def __init__(self, value="+"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] + args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "\t{result} = fadd {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = add {type} {lvalue}, {rvalue}\n"


class Div(Operate):
    def __init__(self, value="/"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] / args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "\t{result} = fdiv {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = sdiv {type} {lvalue}, {rvalue}\n"


class Mult(Operate):
    def __init__(self, value="*"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] * args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "\t{result} = fmul {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = mul {type} {lvalue}, {rvalue}\n"


class Mod(Operate):
    def __init__(self, value="%"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] % args[1]

    def getType(self, args):
        return "int"

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "\t{result} = frem {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = srem {type} {lvalue}, {rvalue}\n"
