from src.Node.Node import *


class Constant(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#FFD885")
        self.funct = None

    def __str__(self):
        return '[label="Constant {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def set_value(self, value):
        self.value = value

    def getLLVMType(self):
        return ""

    def getLLVMPrintType(self):
        return self.getLLVMType()

    def getFormatType(self):
        return ""

    def getNeutral(self):
        return "0"

    def convertString(self, type):
        return ""

    def generateLLVM(self, ast):
        type = ast.getLLVMType()
        val = ast.getValue()
        neutralval = ast.getNeutral()
        return BPlus().get_LLVM(type == "float").format("%", str(ast), type, "", val, "", neutralval)


class CInt(Constant):
    def __init__(self, value=0):
        Constant.__init__(self, int(round(int(value))))
        self.type = "int"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type

    def set_value(self, value):
        self.value = int(round(value))

    def getLLVMType(self):
        return "i32"

    def getFormatType(self):
        return "d"

    def convertString(self, type):
        if type == "int":
            return ""
        elif type == "char":
            return "{}{} = trunc i32 {}{} to i8"
        elif type == "float":
            return "{}{} = sitofp i32 {}{} to float"
        elif type == "double":
            return "{}{} = sitofp i32 {}{} to double"

    def generateLLVM(self, ast):
        val = ast.getValue()
        return BPlus().get_LLVM(False).format("%", str(ast), "i32", "", val, "", "0")


class CFloat(Constant):
    def __init__(self, value=0):
        Constant.__init__(self, float(value))
        self.type = "float"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type

    def set_value(self, value):
        self.value = float(value)

    def getLLVMType(self):
        return "float"

    def getLLVMPrintType(self):
        return "double"

    def getFormatType(self):
        return "f"

    def getNeutral(self):
        return "0.0"

    def convertString(self, type):
        if type == "int":
            return "{}{} = fptosi float {}{} to i32"
        elif type == "char":
            return "{}{} = fptoui float {}{} to i8"
        elif type == "float":
            return ""
        elif type == "double":
            return "{}{} = fpext float {}{} to float"

    def generateLLVM(self, ast):
        val = ast.getValue()
        return BPlus().get_LLVM(True).format("%", str(ast), "float", "", val, "", "0.0")


class CChar(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "char"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type

    def getLLVMType(self):
        return "i8"

    def getFormatType(self):
        return "c"

    def convertString(self, type):
        if type == "int":
            return "{}{} = zext i8 {}{} to i32"
        elif type == "char":
            return ""
        elif type == "float":
            return "{}{} = uitofp i8 {}{} to float"
        elif type == "double":
            return "{}{} = uitofp i8 {}{} to double"

    def generateLLVM(self, ast):
        val = ast.getValue()
        return BPlus().get_LLVM(False).format("%", str(ast), "i8", "", val, "", "0")


class CBool(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "bool"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)

    def getType(self, args):
        return self.type

    def getLLVMType(self):
        return "i1"

    def getFormatType(self):
        return "c"

    def convertString(self, type):
        if type == "int":
            return "{}{} = zext i1 {}{} to i32"
        elif type == "char":
            return "{}{} = zext i1 {}{} to i8"
        elif type == "float":
            return "{}{} = uitofp i1 {}{} to float"
        elif type == "double":
            return "{}{} = uitofp i1 {}{} to double"
