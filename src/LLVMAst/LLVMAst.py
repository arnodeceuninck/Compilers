class LLVMAst:
    _id = 0

    def __init__(self, value, color="#069420"):
        self.value = value
        self.color = color
        self.children = []
        self.parent = None
        self.id_ = None

    def __str__(self):
        return self.value

    def id(self):
        if not self.id_:
            LLVMAst._id += 1
            self.id_ = LLVMAst._id
        return self.id_


# The root
class LLVMCode(LLVMAst):
    def __init__(self):
        super().__init__("LLVM Code")


class LLVMFunction(LLVMAst):
    def __init__(self, name, rettype):
        super().__init__(name)
        self.name = name
        self.rettype = rettype

    def __str__(self):
        return "Function: {name}".format(name=self.name)


class LLVMOperationSequence(LLVMAst):
    def __init__(self):
        super().__init__("Operation Sequence")


class LLVMOperation(LLVMAst):
    def __init__(self, operation, optype):
        super().__init__(operation)
        self.operation = operation
        self.optype = optype


class LLVMBinaryOperation(LLVMOperation):
    def __init__(self, operation, optype):
        super().__init__(operation, optype)


class LLVMAssignment(LLVMAst):
    def __init__(self):
        super().__init__("=")


class LLVMVariable(LLVMAst):
    def __init__(self, name):
        super().__init__(name)
        self.name = name


class LLVMConst(LLVMAst):
    def __init__(self, value):
        super().__init__(value)
        self.constval = value


class LLVMConstInt(LLVMConst):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "int {val}".format(val=self.constval)

class LLVMConstFloat(LLVMConst):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "float {val}".format(val=self.constval)


class LLVMStore(LLVMAst):
    def __init__(self, optype):
        super().__init__("LLVM Store")
        self.type = optype


class LLVMAllocate(LLVMAst):
    def __init__(self, optype, align):
        super().__init__("LLVM Allocate")
        self.type = optype
        self.align = align

    def __str__(self):
        return "Allocate {type} {align}".format(type=self.type, align=self.align)


class LLVMPrintStr(LLVMAst):
    def __init__(self, var):
        super().__init__(var)
        self.printvar = var

    def __str__(self):
        return "Printstr {var}".format(var=self.printvar)


class LLVMPrint(LLVMAst):
    def __init__(self):
        super().__init__("LLVM Print")


class LLVMDeclare(LLVMAst):
    def __init__(self, fname, rettype):
        super().__init__(fname)
        self.name = fname
        self.rettype = rettype

    def __str__(self):
        return "Declare {rettype} {name}".format(rettype=self.rettype, name=self.name)


class LLVMLoad(LLVMAst):
    def __init__(self, type):
        super().__init__("LLVM Load")
        self.type = type

    def __str__(self):
        return "load {type}".format(type=self.type)


class LLVMReturn(LLVMAst):
    def __init__(self, type):
        super().__init__("LLVM return")
        self.type = type

    def __str__(self):
        return "return {type}".format(type=self.type)
