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


class LLVMAddition(LLVMBinaryOperation):
    def __init__(self, optype):
        super().__init__("add", optype)


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
