from src.Node.AST import AST


class Variable(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#af93ff")
        self.type = ""
        self.ptr = False  # e.g. int* a (in declaration), &a (deref in rvalue)
        self.const = False
        self.defined = False

        self.reref = False  # e.g. *a

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '{name}[label="Variable Type: {type}: {value}", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                               type=var_type,
                                                                                               value=self.value,
                                                                                               color=self.color)

    def getType(self, args):
        return self.type + ("*" if self.ptr else "")

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

    def collapse_comment(self, ast):
        return self.value


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "int"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '{name}[label="Variable Type: {type}: {value}", fillcolor="{color}"] \n'.format(name=self.id(), type=var_type, value=self.value, color=self.color)

    def getLLVMType(self):
        return "i32" + ("*" if self.ptr else "")

    def getLLVMPrintType(self):
        return "i32"

    def getFormatType(self):
        return "d"

    def getAlign(self):
        return 4 + 4 * self.ptr

    def convertString(self, type):
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
        self.type = "char"


    def getLLVMType(self):
        return "i8" + ("*" if self.ptr else "")

    def getLLVMPrintType(self):
        return "i8"

    def getFormatType(self):
        return "c"

    def getAlign(self):
        return 1 + 7 * self.ptr

    def convertString(self, type):
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
        self.type = "float"


    def getLLVMType(self):
        return "float" + ("*" if self.ptr else "")

    def getLLVMPrintType(self):
        return "double"

    def getFormatType(self):
        return "f"

    def getAlign(self):
        return 4 + 4 * self.ptr

    def convertString(self, type):
        if type == "int":
            return "{}{} = fptosi float {}{} to i32\n"
        elif type == "char":
            return "{}{} = fptoui float {}{} to i8\n"
        elif type == "float":
            return ""
        elif type == "double":
            return "{}{} = fpext float {}{} to double\n"
