from src.Node.AST import AST, StatementSequence, Assign
from src.Node.Unary import Unary
from src.ErrorListener import RerefError


class Variable(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#af93ff")
        self.ptr = 0  # e.g. int* a (in declaration), &a (deref in rvalue)
        self.const = False
        self.defined = False
        self.llvm_defined = False  # If the variable is already defined in llvm code

        self.reref = 0

        self.array = False
        self.array_number = 0  # The index or the size in case of declaration
        self.array_size = 0  # The size of the array

        self.declaration = False

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.get_type()
        label = "Variable Type: {type}: {value}".format(type=var_type,
                                                        value=self.value)
        if self.array:
            label += "[{nr}]".format(nr=self.array_number)
        return '\t{name}[label=\"{label}\", fillcolor="{color}"] \n'.format(name=self.id(), label=label,
                                                                            color=self.color)

    def constant_folding(self):
        return False

    def get_type(self):
        raise Exception("Abstract function")
        # return self.type + ("*" if self.ptr else "")

    def getFormatType(self):
        return ""

    def convertString(self, type):
        return ""

    def get_llvm_template(self):
        return self.llvm_load_template()

    def max_array_size(self):
        if not self.array:
            return 0
        return self.array_size

    def get_align(self):
        return 0

    def comments(self, comment_out: bool = True):
        comment = self.value
        return self.comment_out(comment, comment_out)


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_llvm_print_type(self) -> str:
        return "i32"

    def get_type(self):
        return "int" + ("*"*self.ptr)  # TODO: arrays should also include a '*', but this lets 3 tests fail

    def get_format_type(self):
        return "d"

    def get_align(self, ignore_array=False):
        if self.array and not ignore_array:
            return 4 if self.array_number < 4 else 16
        return 8 if self.ptr else 4

    def convert_template(self, type):
        if type == "int":
            return ""
        elif type == "char":
            return "\t{}{} = trunc i32 {}{} to i8\n"
        elif type == "float":
            return "\t{}{} = sitofp i32 {}{} to float\n"
        elif type == "double":
            return "\t{}{} = sitofp i32 {}{} to double\n"
        elif type == "bool":
            return "\t{}{} = trunc i32 {}{} to i1\n"


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_type(self):
        return "char" + ("*"*self.ptr)

    def get_llvm_print_type(self) -> str:
        return "i8"

    def get_format_type(self):
        return "c"

    def get_align(self):
        return 8 if self.ptr else 1

    def convert_template(self, type):
        if type == "int":
            return "\t{result} = zext i8 {value} to i32\n"
        elif type == "char":
            return None
        elif type == "float":
            return "\t{result} = uitofp i8 {value} to float\n"
        elif type == "double":
            return "\t{result} = uitofp i8 {value} to double\n"
        elif type == "bool":
            return "\t{result} = trunc i8 {value} to i1\n"


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_type(self):
        return "float" + ("*"*self.ptr)

    def get_llvm_print_type(self) -> str:
        return "double"

    def get_format_type(self):
        return "f"

    def get_align(self):
        return 8 if self.ptr else 4

    def get_neutral(self) -> str:
        return "0.0"

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "\t{result} = fptosi float {value} to i32\n"
        elif type == "char":
            return "\t{result} = fptoui float {value} to i8\n"
        elif type == "float":
            return ""
        elif type == "double":
            return "\t{result} = fpext float {value} to double\n"
        elif type == "bool":
            return "\t{result} = fptoui float {value} to i1\n"
