from src.Node.AST import AST, Binary, BoolClasses
from src.Node.Constant import CBool
from src.Node.Operate import Mult, BPlus


class Compare(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return 'Binary Operator Compare: {value}'.format(value=self.value)


class LessT(Compare):
    def __init__(self, value="<"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] < args[1]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fcmp olt {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = icmp slt {type} {lvalue}, {rvalue}\n"


class MoreT(Compare):
    def __init__(self, value=">"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] > args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "\t{}{} = fcmp ogt {} {}{}, {}{}\n"
        return "\t{}{} = icmp sgt {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fcmp ogt {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = icmp sgt {type} {lvalue}, {rvalue}\n"


class LessOrEq(Compare):
    def __init__(self, value="<="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] <= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "\t{}{} = fcmp ole {} {}{}, {}{}\n"
        return "\t{}{} = icmp sle {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fcmp ole {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = icmp sle {type} {lvalue}, {rvalue}\n"


class MoreOrEq(Compare):
    def __init__(self, value=">="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] >= args[1]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fcmp oge {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = icmp sge {type} {lvalue}, {rvalue}\n"


class Equal(Compare):
    def __init__(self, value="=="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] == args[1]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fcmp oeq {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = icmp eq {type} {lvalue}, {rvalue}\n"


class NotEqual(Compare):
    def __init__(self, value="!="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] != args[1]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fcmp one {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = icmp ne {type} {lvalue}, {rvalue}\n"


class LogicAnd(Compare):
    def __init__(self, value="&&"):
        Compare.__init__(self, value)
        self.funct = lambda args: (args[0] * args[1]) != 0

    def get_llvm_template(self) -> str:
        # A and B <=> A*B != 0
        if self.get_type() == "float":
            template = "\t{result_temp} = fmul {type} {lvalue}, {rvalue}\n"
            template += "\t{result} = fcmp one {type} {result_temp}, 0.0\n"
        else:
            template = "\t{result_temp} = mul {type} {lvalue}, {rvalue}\n"
            template += "\t{result} = icmp ne {type} {result_temp}, " + str(self.get_neutral()) + "\n"
        return template


class LogicOr(Compare):
    def __init__(self, value="||"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] or args[1]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            template = "\t{temp} = fadd {{type}} {{lvalue}}, {{rvalue}}\n"
            template += "\t{{result}} = fcmp one {{type}} {temp}, 0.0\n"
        else:
            template = "\t{temp} = add {{type}} {{lvalue}}, {{rvalue}}\n"
            template += "\t{{result}} = icmp ne {{type}} {temp}, {neutral}\n"
        temp = self.get_temp()
        template = template.format(temp=temp, neutral=self.get_neutral())
        return template
        # return "{result} = icmp or {type} {lvalue}, {rvalue}\n"
