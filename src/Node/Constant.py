from src.Node.AST import AST, BoolClasses, stringVar, stringArg


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
            return "\t{result} = fadd {type} {lvalue}, {rvalue}\n"
        else:
            return "\t{result} = add {type} {lvalue}, {rvalue}\n"

    def comments(self, comment_out=True):
        return self.comment_out(str(self.value), comment_out=comment_out)

    # Returns a constant based of of the type passed through
    def create_constant(self, type):
        if type == "int":
            return CInt("0")
        elif type == "float":
            return CFloat("0.0")
        elif type == "char":
            return CChar("0")
        elif type == "bool":
            return CBool("0")
        return None


class CArray(Constant):
    def __init__(self, value: str = "Array"):
        Constant.__init__(self, value)

    def get_llvm_type(self) -> str:
        if len(self.children) == 0:
            return None
        type = self[0].get_llvm_type()
        for child in self.children:
            if type != child.get_llvm_type():
                return None
        return type

    def get_llvm_template(self):
        pass


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

    def get_align(self):
        return 4

    @staticmethod
    def convert_template(type):
        if type == "int":
            return None
        elif type == "char":
            return "\t{result} = trunc i32 {value} to i8\n"
        elif type == "float":
            return "\t{result} = sitofp i32 {value} to float\n"
        elif type == "double":
            return "\t{result} = sitofp i32 {value} to double\n"
        elif type == "bool":  # Bool needs to be treated special because trunc will cut of bytes, and not convert it properly so an not equal to 0 must be used
            return "\t{result} = icmp ne i32 {value}, 0\n"


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

    def get_align(self):
        return 4

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "\t{result} = fptosi float {value} to i32\n"
        elif type == "char":
            return "\t{result} = fptoui float {value} to i8\n"
        elif type == "float":
            return None
        elif type == "double":
            return "\t{result} = fpext float {value} to double\n"
        elif type == "bool":  # Bool needs to be treated special because trunc will cut of bytes, and not convert it properly so an not equal to 0 must be used
            return "\t{result} = fcmp one float {value}, 0.0\n"


class CChar(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)

    def get_type(self):
        return "char"

    def get_llvm_type(self) -> str:
        return "i8"

    def get_format_type(self):
        return "c"

    def get_align(self):
        return 1

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "\t{result} = zext i8 {value} to i32\n"
        elif type == "char":
            return None
        elif type == "float":
            return "\t{result} = uitofp i8 {value} to float\n"
        elif type == "double":
            return "\t{result} = uitofp i8 {value} to double\n"
        elif type == "bool":  # Bool needs to be treated special because trunc will cut of bytes, and not convert it properly so an not equal to 0 must be used
            return "{result} = icmp ne i8 {value}, 0\n"

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
            return "\t{result} = zext i1 {value} to i32\n"
        elif type == "char":
            return "\t{result} = zext i1 {value} to i8\n"
        elif type == "float":
            return "\t{result} = uitofp i1 {value} to float\n"
        elif type == "double":
            return "\t{result} = uitofp i1 {value} to double\n"
        elif type == "bool":
            return ""


# This really shouldn't exist
# TODO: Replace this with another type see printf and scanf for dependencies
class CString(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)

    def get_type(self):
        return "string"

    def get_llvm_type(self) -> str:
        return ""

    def get_format_type(self):
        return "s"


