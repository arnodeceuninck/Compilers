from src.Node.AST import AST
from src.Node.Operate import BPlus


class Constant(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#FFD885")
        self.funct = None

    def __str__(self):
        return '{name}[label="Constant {value}", fillcolor="{color}"] \n'.format(name=self.id(), value=self.value,
                                                                                 color=self.color)

    def constant_folding(self):
        return True

    def set_value(self, value):
        self.value = value

    def get_llvm_type(self) -> str:
        raise Exception("Abstract method")

    # TODO: wtf is the use of tis function?
    def get_format_type(self):
        raise Exception("Abstract method")

    @staticmethod
    def convert_template(type):
        raise Exception("Abstract methos")

    def get_llvm_template(self):
        if self.get_type() == "float":
            return "{result} = fadd {type} {lvalue}, {rvalue}\n"
        else:
            return "{result} = add {type} {lvalue}, {rvalue}\n"

    def llvm_code(self) -> int:
        output = self.comments()
        code = self.get_llvm_template()
        code = code.format(result=self.variable(), type=self.get_llvm_type(), lvalue=self.value,
                           rvalue=self.get_neutral())
        output += code
        AST.llvm_output += output

    def comments(self, comment_out=True):
        return self.comment_out(str(self.value), comment_out=comment_out)


class CInt(Constant):
    def __init__(self, value: str = "0"):
        Constant.__init__(self, str(int(round(float(value)))))

    def get_type(self):
        return "int"

    def set_value(self, value: float):
        self.value = str(int(round(value)))

    def get_llvm_type(self) -> str:
        return "i32"

    def get_format_type(self):
        return "d"

    @staticmethod
    def convert_template(type):
        if type == "int":
            return None
        elif type == "char":
            return "{result} = trunc i32 {value} to i8\n"
        elif type == "float":
            return "{result} = sitofp i32 {value} to float\n"
        elif type == "double":
            return "{result} = sitofp i32 {value} to double\n"


class CFloat(Constant):
    def __init__(self, value=0):
        Constant.__init__(self, float(value))

    def get_type(self):
        return "float"

    def set_value(self, value):
        self.value = str(float(value))

    def get_llvm_type(self) -> str:
        return "float"

    def get_llvm_print_type(self):
        return "double"

    def get_format_type(self):
        return "f"

    def get_neutral(self) -> str:
        return "0.0"

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "{result} = fptosi float {value} to i32\n"
        elif type == "char":
            return "{result} = fptoui float {value} to i8\n"
        elif type == "float":
            return None
        elif type == "double":
            return "{result} = fpext float {value} to float\n"


class CChar(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)

    def get_type(self):
        return "char"

    def get_llvm_type(self) -> str:
        return "i8"

    def get_format_type(self):
        return "c"

    @staticmethod
    def convertString(type):
        if type == "int":
            return "{result} = zext i8 {value} to i32\n"
        elif type == "char":
            return None
        elif type == "float":
            return "{result} = uitofp i8 {value} to float\n"
        elif type == "double":
            return "{result} = uitofp i8 {value} to double\n"

    def llvm_code(self) -> int:
        output = self.comments()
        code = self.get_llvm_template()
        code = code.format(result=self.variable(), type=self.get_llvm_type(), lvalue=str(ord(self.value)),
                           rvalue=self.get_neutral())
        output += code
        AST.llvm_output += output


class CBool(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)

    def get_type(self):
        return "bool"

    def get_llvm_type(self) -> str:
        return "i1"

    def get_format_type(self):
        return "c"

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "{result} = zext i1 {value} to i32\n"
        elif type == "char":
            return "{result} = zext i1 {value} to i8\n"
        elif type == "float":
            return "{result} = uitofp i1 {value} to float\n"
        elif type == "double":
            return "{result} = uitofp i1 {value} to double\n"
