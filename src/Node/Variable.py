from src.Node.AST import AST


class Variable(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#af93ff")
        self.ptr = False  # e.g. int* a (in declaration), &a (deref in rvalue)
        self.const = False
        self.defined = False

        self.reref = False  # e.g. *a

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.get_type()
        var_type += "*" if self.ptr else ""
        return '{name}[label="Variable Type: {type}: {value}", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                               type=var_type,
                                                                                               value=self.value,
                                                                                               color=self.color)

    def constant_folding(self):
        return False

    def get_type(self):
        raise Exception("Abstract function")
        # return self.type + ("*" if self.ptr else "")

    def getLLVMType(self):
        return ""

    def getFormatType(self):
        return ""

    def convertString(self, type):
        return ""

    def get_llvm_template(self):
        return self.llvm_load_template()

    # Variable should be llvm_formated, e.g. %1
    def llvm_load(self, variable: str):
        code = self.get_llvm_template()
        code.format(result=variable, type=self.get_llvm_type(), var=self.variable())

    def llvm_code(self):
        return self.llvm_load()

    def comments(self, comment_out: bool = False):
        comment = self.value
        return self.comment_out(comment, comment_out)


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_llvm_type(self) -> str:
        return "i32" + ("*" if self.ptr else "")

    def get_llvm_print_type(self) -> str:
        return "i32"

    def get_type(self):
        return "int"

    def get_format_type(self):
        return "d"

    def get_align(self):
        return 4 + 4 * self.ptr

    def convert_template(self, type):
        if type == "int":
            return ""
        elif type == "char":
            return "{}{} = trunc i32 {}{} to i8\n"
        elif type == "float":
            return "{}{} = sitofp i32 {}{} to float\n"
        elif type == "double":
            return "{}{} = sitofp i32 {}{} to double\n"


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_llvm_type(self) -> str:
        return "i8" + ("*" if self.ptr else "")

    def get_type(self):
        return "char"

    def get_llvm_print_type(self) -> str:
        return "i8"

    def get_format_type(self):
        return "c"

    def get_align(self):
        return 1 + 7 * self.ptr

    def convert_template(self, type):
        if type == "int":
            return "{}{} = zext i8 {}{} to i32\n"
        elif type == "char":
            return ""
        elif type == "float":
            return "{}{} = uitofp i8 {}{} to float\n"
        elif type == "double":
            return "{}{} = uitofp i8 {}{} to double\n"


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_type(self):
        return "float"

    def get_llvm_type(self):
        return "float" + ("*" if self.ptr else "")

    def get_llvm_print_type(self) -> str:
        return "double"

    def get_format_type(self):
        return "f"

    def get_align(self):
        return 4 + 4 * self.ptr

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "{result} = fptosi float {value} to i32\n"
        elif type == "char":
            return "{result} = fptoui float {value} to i8\n"
        elif type == "float":
            return ""
        elif type == "double":
            return "{result} = fpext float {value} to double\n"
