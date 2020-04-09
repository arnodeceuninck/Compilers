from src.Node.AST import Binary, AST, If
from src.Node.constant import Constant


class Operate(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def get_type(self):
        if self[0].get_type() == self[1].get_type():
            return self[0].get_type()
        elif self[0].get_type() == "int" and self[1].get_type() == "float" or \
                self[0].get_type() == "float" and self[1].get_type() == "int":
            return "float"
        else:
            return "UNKNOWN"

    def llvm_code(self) -> str:

        self[0].llvm_code()
        self[1].llvm_code()

        output = self.comments()

        llvm_type = self.get_llvm_type()

        result = self.variable()
        # If the parent is an if statement then we need to store the code into a temporary variable and then convert it
        if isinstance(self.parent, If):
            result = self.get_temp()

        code = self.get_llvm_template()
        code = code.format(result=result, type=llvm_type, lvalue=self[0].variable(),
                           rvalue=self[1].variable())

        output += code

        # We need to convert this node into a bool type (i1), because the node above it is an if statement
        if isinstance(self.parent, If):
            constant_type = Constant().create_constant(self.get_type())
            type_to_bool = constant_type.convert_template("bool")
            type_to_bool = type_to_bool.format(result=self.variable(), value=result)
            output += type_to_bool

        AST.llvm_output += output


class BMinus(Operate):
    def __init__(self, value="-"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] - args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "{result} = fsub {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = sub {type} {lvalue}, {rvalue}\n"


class BPlus(Operate):
    def __init__(self, value="+"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] + args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "{result} = fadd {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = add {type} {lvalue}, {rvalue}\n"


class Div(Operate):
    def __init__(self, value="/"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] / args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "{result} = fdiv {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = sdiv {type} {lvalue}, {rvalue}\n"


class Mult(Operate):
    def __init__(self, value="*"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] * args[1]

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "{result} = fmul {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = mul {type} {lvalue}, {rvalue}\n"


class Mod(Operate):
    def __init__(self, value="%"):
        Operate.__init__(self, value)
        self.funct = lambda args: args[0] % args[1]

    def getType(self, args):
        return "int"

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "{result} = frem {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = srem {type} {lvalue}, {rvalue}\n"
