from src.Node.AST import Operator, Variable, AST, CBool, VFloat
from src.Utils import printString
from src.ErrorListener import RerefError

class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)
        self.funct = None

    def __str__(self):
        return '{name}[label="Unary Operator: {value}", fillcolor="{color}"] \n'.format(name=self.name, value=self.value, color=self.color)

    def get_type(self):
        return self[0].get_type()  # Only one type as argument


    def comments(self, comment_out: bool = True) -> str:
        comment = self.value + " " + self[0].comments()
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        AST.llvm_output += self.comments()

        type = self.get_llvm_type()

        code = self.get_llvm_template()
        code.format(result=self.variable(), type=type, value=self[0].variable())

        AST.llvm_output += code


class UPlus(Unary):
    def __init__(self, value="+"):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fadd {type} {value}, 0.0\n"
        else:
            return "{result} = add {type} {value}, 0\n"


class UMinus(Unary):
    def __init__(self, value="-"):
        Unary.__init__(self, value)
        self.funct = lambda args: -args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fsub {type} 0.0, {value}\n"
        else:
            return "{result} = sub {type} 0, {value}\n"



class UDMinus(Unary):
    def __init__(self, value="--"):
        Unary.__init__(self, value)
        self.funct = lambda args: args[0] - 1


class UDPlus(Unary):
    def __init__(self, value="++"):
        Unary.__init__(self, value)
        self.funct = lambda args: args[0] - 1


class UNot(Unary):
    def __init__(self, value="!"):
        Unary.__init__(self, value)
        self.funct = lambda args: not args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fcmp oeq {} {}{}, 0.0\n"
        return "{}{} = icmp eq {} {}{}, 0\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp oeq {type} 0.0, {value}\n"
        else:
            return "{result} = eq {type} 0, {value}\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()

        type = self.get_llvm_type()

        temp = self.get_temp()

        code = self.get_llvm_template()
        code = code.format(temp, type, self[0].variable())
        AST.llvm_output += code

        bool_to_type = CBool.convert_template(self.get_type())
        bool_to_type.format(self.variable(), temp)

        AST.llvm_output += bool_to_type


class UDeref(Unary):
    def __init__(self, value="&"):
        Unary.__init__(self, value)

    def getType(self, args):
        return args[0] + "*"


class UReref(Unary):
    def __init__(self, value="*"):
        Unary.__init__(self, value)

    def get_type(self):
        child_type = self[0].get_type()
        if child_type[len(child_type) - 1] != "*":
            raise RerefError()
        return child_type[:len(child_type - 1)]

    def llvm_code(self):
        self[0].llvm_code()
        type = self.get_llvm_type()

        # Load the value into the ast node
        code = self.llvm_load_template()
        code = code.format(result=self.variable(), type=type[:-1], var=self[0].variable())

        AST.llvm_output += code


class Print(Unary):
    def __init__(self, value="printf"):
        Unary.__init__(self, value)

    def get_type(self):
        return "function"

    def llvm_code(self):
        # Generate LLVM for the node that needs to be printed
        self[0].llvm_code()
        format_type = self[0].get_format_type()
        print_type = self[0].get_llvm_print_type()

        # Because you can't print floats
        if print_type == "double":
            convert_code = VFloat.convertString("double")
            convert_code = convert_code.format(self.variable(), self[0].variable())
            AST.llvm_output += convert_code


        print_code = printString.format(format_type=format_type, print_type=print_type, value=self.variable())
        AST.llvm_output += print_code

    def comments(self, comment_out=True):
        comment = "Print " + self[0].comments()
        return self.comment_out(comment, comment_out)
