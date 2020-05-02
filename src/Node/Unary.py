from src.Node.AST import Operator, AST, BoolClasses
from src.Node.Constant import CBool
from src.ErrorListener import RerefError

printString = '\tcall i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str{format_type}, i32 0, i32 0), {print_type} {value})\n'


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)
        self.funct = None

    def __str__(self):
        return "Unary Operator: {value}".format(value=self.value)

    def get_type(self):
        return self[0].get_type()  # Only one type as argument

    def comments(self, comment_out: bool = True) -> str:
        comment = self.value + " " + self[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)


class UPlus(Unary):
    def __init__(self, value="+"):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fadd {type} {value}, 0.0\n"
        else:
            return "\t{result} = add {type} {value}, 0\n"


class UMinus(Unary):
    def __init__(self, value="-"):
        Unary.__init__(self, value)
        self.funct = lambda args: -args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fsub {type} 0.0, {value}\n"
        else:
            return "\t{result} = sub {type} 0, {value}\n"


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
            template = "\t{{result}} = fcmp oeq {{type}} {neutral}, {{value}}\n"
        else:
            template = "\t{{result}} = icmp eq {{type}} {neutral}, {{value}}\n"
        template = template.format(neutral=str(self.get_neutral()))
        return template


class ArrayIndex(Unary):
    def __init__(self, index=None):
        self.index = index
        Unary.__init__(self, "[{i}]".format(i=index))

    def get_type(self):
        try:
            return self[0].get_type()
        except:
            return None

    def get_llvm_template(self):
        code = "{temp_index} = sext {index_type} {index} to i64\n"
        code += "{temp} = getelementptr inbounds {array_type}, {array_type}* {variable}, i64 0, i64 {temp_index}\n"
        code += "{result} = load {type}, {type}* {temp}, align {align}\n"  # NOTE: not the array align
        return code

    def get_align(self):
        return self[0].get_align(ignore_array=True)

    def comments(self, comment_out=True):
        comment = self[0].value + self.value
        return self.comment_out(comment, comment_out)


class Print(Unary):
    def __init__(self, value="printf"):
        Unary.__init__(self, value)

    def get_type(self):
        return "function"

    def comments(self, comment_out=True):
        comment = "Print " + self[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)


class UDeref(Unary):
    def __init__(self, value="&"):
        Unary.__init__(self, value)

    def get_type(self):
        return self[0].get_type() + "*"

    def is_declaration(self):
        return self[0].is_declaration()


class UReref(Unary):
    def __init__(self, value="*"):
        Unary.__init__(self, value)

    def get_type(self):
        child_type = self[0].get_type()
        if child_type[len(child_type) - 1] != "*":
            raise RerefError()
        return child_type[:-1]

    def is_declaration(self):
        return self[0].is_declaration()

