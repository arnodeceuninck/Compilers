from src.Node.AST import Operator, Variable, AST, If
from src.Node.constant import CBool
from src.Node.Variable import VFloat
from src.Utils import printString
from src.ErrorListener import RerefError


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)
        self.funct = None

    def __str__(self):
        return '{name}[label="Unary Operator: {value}", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                        value=self.value,
                                                                                        color=self.color)

    def get_type(self):
        return self[0].get_type()  # Only one type as argument

    def comments(self, comment_out: bool = True) -> str:
        comment = self.value + " " + self[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        type = self.get_llvm_type()

        code = self.get_llvm_template()
        code = code.format(result=self.variable(), type=type, value=self[0].variable())

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

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            template = "{{result}} = fcmp oeq {{type}} {neutral}, {{value}}\n"
        else:
            template = "{{result}} = icmp eq {{type}} {neutral}, {{value}}\n"
        template = template.format(neutral=str(self.get_neutral()))
        return template

    def llvm_code(self):
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        type = self.get_llvm_type()

        # We need to have the variable in order to have the correct translation when the parrent is the If
        # because we do not want to extend the i1 we have to keep it that way
        if isinstance(self.parent, If):
            temp = self.variable(self.id())
        else:
            temp = self.get_temp()

        code = self.get_llvm_template()
        code = code.format(result=temp, type=type, value=self[0].variable())
        AST.llvm_output += code

        # if the parent is an if statement then do not convert the variable
        if isinstance(self.parent, If):
            return
        bool_to_type = CBool.convert_template(self.get_type())
        bool_to_type = bool_to_type.format(result=self.variable(), value=temp)

        AST.llvm_output += bool_to_type


class UDeref(Unary):
    def __init__(self, value="&"):
        Unary.__init__(self, value)

    def get_type(self):
        return self[0].get_type() + "*"

    def get_llvm_type(self):
        return self[0].get_type() + "*"

    def llvm_code(self):
        self[0].llvm_code()
        self[0].variable()
        pass # TODO: fix it


class UReref(Unary):
    def __init__(self, value="*"):
        Unary.__init__(self, value)

    def get_type(self):
        child_type = self[0].get_type()
        if child_type[len(child_type) - 1] != "*":
            raise RerefError()
        return child_type[:len(child_type)-1]

    def get_llvm_type(self):
        child_type = self[0].get_llvm_type()
        if child_type[len(child_type) - 1] != "*":
            raise RerefError()
        return child_type[:len(child_type) - 1]

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
        AST.print = True

        # Generate LLVM for the node that needs to be printed
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        format_type = self[0].get_format_type()
        print_type = self[0].get_llvm_print_type()

        variable = self[0].variable()
        # Because you can't print floats
        if print_type == "double":
            convert_code = VFloat.convert_template("double")
            convert_code = convert_code.format(result=self.variable(), value=self[0].variable())
            variable = self.variable()
            AST.llvm_output += convert_code

        print_code = printString.format(format_type=format_type, print_type=print_type, value=variable)
        AST.llvm_output += print_code

    def comments(self, comment_out=True):
        comment = "Print " + self[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)
