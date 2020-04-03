from src.Node.Node import *


class Variable(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#af93ff")
        self.type = ""
        self.ptr = False  # e.g. int* a (in declaration), &a (deref in rvalue)
        self.const = False
        self.defined = False

        self.reref = False  # e.g. *a

    def __str__(self):
        return '[label="Variable: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        return self.type + ("*" if self.ptr else "")

    def getLLVMType(self):
        return ""

    def getFormatType(self):
        return ""

    def convertString(self, type):
        return ""

    def generateLLVM(self, ast):
        return get_LLVM_load().format("%", str(ast), ast.getLLVMType(), ast.getLLVMType(), "@", ast.getValue())


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "int"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)

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
            return "{}{} = trunc i32 {}{} to i8"
        elif type == "float":
            return "{}{} = sitofp i32 {}{} to float"
        elif type == "double":
            return "{}{} = sitofp i32 {}{} to double"


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "char"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)

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
            return "{}{} = zext i8 {}{} to i32"
        elif type == "char":
            return ""
        elif type == "float":
            return "{}{} = uitofp i8 {}{} to float"
        elif type == "double":
            return "{}{} = uitofp i8 {}{} to double"


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "float"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)

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
            return "{}{} = fptosi float {}{} to i32"
        elif type == "char":
            return "{}{} = fptoui float {}{} to i8"
        elif type == "float":
            return ""
        elif type == "double":
            return "{}{} = fpext float {}{} to double"
