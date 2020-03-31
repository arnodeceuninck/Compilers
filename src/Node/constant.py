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
