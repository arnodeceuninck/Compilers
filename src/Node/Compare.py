from src.Node.AST import AST, Binary
from src.Node.constant import CBool
from src.Node.Operate import Mult, BPlus


class Compare(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '{name}[label="Binary Operator Compare: {value}", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                                 value=self.value,
                                                                                                 color=self.color)

    def get_type(self):
        if self[0].get_type() == self[1].get_type():
            return self[0].get_type()
        else:
            return "unknown"

    def llvm_code(self) -> str:
        self[0].llvm_code()
        self[1].llvm_code()

        output = self.comments()

        llvm_type = self.get_llvm_type()

        temp = self.get_temp()

        comp_output = self.get_llvm_template()

        comp_output = comp_output.format(result=temp, type=llvm_type,
                                         lvalue=self[0].variable(),
                                         rvalue=self[1].variable())

        output += comp_output

        # Now convert the output (i1) we got to the type we need
        bool_to_type = CBool.convert_template(self.get_type())
        bool_to_type = bool_to_type.format(result=self.variable(self.id()), value=temp)

        output += bool_to_type

        AST.llvm_output += output


class LessT(Compare):
    def __init__(self, value="<"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] < args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp olt {} {}{}, {}{}\n"
        return "{}{} = icmp slt {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp olt {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = icmp slt {type} {lvalue}, {rvalue}\n"


class MoreT(Compare):
    def __init__(self, value=">"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] > args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp ogt {} {}{}, {}{}\n"
        return "{}{} = icmp sgt {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp ogt {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = icmp sgt {type} {lvalue}, {rvalue}\n"


class LessOrEq(Compare):
    def __init__(self, value="<="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] <= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp ole {} {}{}, {}{}\n"
        return "{}{} = icmp sle {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp ole {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = icmp sle {type} {lvalue}, {rvalue}\n"


class MoreOrEq(Compare):
    def __init__(self, value=">="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] >= args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp oge {} {}{}, {}{}\n"
        return "{}{} = icmp sge {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp oge {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = icmp sge {type} {lvalue}, {rvalue}\n"


class Equal(Compare):
    def __init__(self, value="=="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] == args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp oeq {} {}{}, {}{}\n"
        return "{}{} = icmp eq {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp oeq {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = icmp eq {type} {lvalue}, {rvalue}\n"


class NotEqual(Compare):
    def __init__(self, value="!="):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] != args[1]

    def get_LLVM(self, is_float=False):
        if is_float:
            return "{}{} = fcmp one {} {}{}, {}{}"
        return "{}{} = icmp ne {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "{result} = fcmp one {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = icmp ne {type} {lvalue}, {rvalue}\n"


class LogicAnd(Compare):
    def __init__(self, value="&&"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] and args[1]

    def get_LLVM(self, is_float=False):
        return "{}{} = icmp and {} {}{}, {}{}\n"

    def get_llvm_template(self) -> str:
        # A and B <=> A*B != 0
        if self.get_type() == "float":
            template = "{result_temp} = fmul {type} {lvalue}, {rvalue}\n"
            template += "{result} = fcmp one {type} {result_temp}, " + str(self.get_neutral()) + "\n"
        else:
            template = "{result_temp} = mul {type} {lvalue}, {rvalue}\n"
            template += "{result} = icmp ne {type} {result_temp}, " + str(self.get_neutral()) + "\n"
        return template

    def llvm_code(self) -> (str, int):
        output = self.comments()

        llvm_type = self.get_llvm_type()

        temp1 = self.get_unique_id()
        temp2 = self.get_unique_id()

        comp_output = self.get_llvm_template()

        comp_output = comp_output.format(result_temp=self.variable(temp1), type=llvm_type,
                                         lvalue=self.variable(self.children[0].id()),
                                         rvalue=self.variable(self.children[1].id()), result=temp2)

        output += comp_output

        # Now convert the output (i1) we got to the type we need
        bool_to_type = CBool.convertString(self.get_type())
        bool_to_type = bool_to_type.format(self.variable(self.id()), self.variable(temp2))

        output += bool_to_type

        AST.llvm_output += output


class LogicOr(Compare):
    def __init__(self, value="||"):
        Compare.__init__(self, value)
        self.funct = lambda args: args[0] or args[1]

    def get_llvm_template(self) -> str:
        return "{result} = icmp or {type} {lvalue}, {rvalue}\n"

    # TODO?
    # def generate_LLVM(self, ast):
    #     # execute operator
    #     type = ast.getLLVMType()
    #     is_float = (ast.getType() == "float")
    #     # Both variable
    #     tempSave1 = "t" + str(ast.node.get_id())
    #     tempSave2 = "t" + str(ast.node.get_id())
    #     output = BPlus().get_LLVM(is_float).format("%", tempSave1, type, "%",
    #                                                str(ast.children[0]),
    #                                                "%", str(ast.children[1]))
    #     output += NotEqual().get_LLVM(is_float).format("%", tempSave2, type, "%", tempSave1,
    #                                                    "", ast.getNeutral())
    #     output += CBool().convertString(ast.getType()).format("%", str(ast), "%", tempSave2)
    #     return output
