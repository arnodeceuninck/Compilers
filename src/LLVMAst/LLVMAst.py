# This will set the offset per type, and put it in the dict
def set_offset(llvm_ast):
    # The variable needs to be a llvm variable
    if not isinstance(llvm_ast, LLVMVariable):
        return

    LLVMAst.offset_dct[llvm_ast.value] = llvm_ast.get_offset()


class LLVMAst:
    _id = 0
    offset_dct = {}

    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None
        self.id_ = None
        self.offset = 0  # This is the offset that a single variable needs

    def __str__(self):
        return self.value

    def __getitem__(self, item):
        return self.children[item]

    def id(self):
        if not self.id_:
            LLVMAst._id += 1
            self.id_ = LLVMAst._id
        return self.id_

    # Perform a pre-order traversal
    def traverse(self, function):
        function(self)
        for child in self.children:
            child.traverse(function)

    # This function will get the index of the variable position in the global table
    # NOTE: this will only work in variable
    def get_index_offset(self):
        # Seek the top-most symbol table
        _parent = self
        while _parent.parent:
            _parent = _parent.parent

        # Store the symbol table
        symbol_table = _parent.symbol_table
        for i, v in enumerate(symbol_table.total_table):
            if v == self.value:
                # TODO let this calculation support arrays :)
                return 4 * i

    # This method tries to find the position of a node with respect to the first node with a symbol table in it
    # The parent nr is a way of saying which parent we need to use, first we seek the parent then we go digging
    def get_position(self, parent_nr=0):
        # This will go the the max of parent_nr for seeking a parent
        parent = self.parent
        child = self
        while parent_nr and parent:
            child = parent
            parent = parent.parent
            parent_nr -= 1

        position = 0
        # Iterate over all the children of the operation sequence and check if the ast node is met
        # If it is met, then this will be the final position at which the variable is declared
        for _child in parent:
            if _child == child:
                break
            position += 1
        return position


# The root
class LLVMCode(LLVMAst):
    def __init__(self):
        super().__init__("LLVM Code")
        self.symbol_table = SymbolTable(self.id())


class LLVMFunction(LLVMAst):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.rettype = None
        self.symbol_table = SymbolTable(self.id())

    def __str__(self):
        return "Function: {name}".format(name=self.name)


class LLVMFunctionUse(LLVMAst):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.rettype = None

    def __str__(self):
        return "Function call: {name}".format(name=self.name)

    def to_mips(self):
        return self.name + ":"


class LLVMOperationSequence(LLVMAst):
    def __init__(self):
        super().__init__("Operation Sequence")
        self.symbol_table = SymbolTable(self.id())


class LLVMOperation(LLVMAst):
    def __init__(self, operation):
        super().__init__(operation)
        self.operation = operation
        self.optype = None


class LLVMBinaryOperation(LLVMOperation):
    def __init__(self, operation):
        super().__init__(operation)


class LLVMCompareOperation(LLVMBinaryOperation):
    def __init__(self, operation):
        super().__init__(operation)


class LLVMFloatCompareOperation(LLVMBinaryOperation):
    def __init__(self, operation):
        super().__init__(operation)


class LLVMIntCompareOperation(LLVMBinaryOperation):
    def __init__(self, operation):
        super().__init__(operation)


class LLVMAssignment(LLVMAst):
    def __init__(self):
        super().__init__("=")


class LLVMVariable(LLVMAst):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.type = None  # Currently only set with use argument

    def __str__(self):
        if self.type:
            return "{} {}".format(self.type, self.name)
        else:
            return self.name


class LLVMConst(LLVMAst):
    def __init__(self, value):
        super().__init__(value)
        self.constval = value


class LLVMConstInt(LLVMConst):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "int {val}".format(val=self.constval)

    def get_str_value(self):
        return self.constval

    def get_mips_type(self):
        return ".word"

    def get_type(self):
        return "int"


class LLVMConstFloat(LLVMConst):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "float {val}".format(val=self.constval)

    def get_str_value(self):
        return self.constval

    def get_mips_type(self):
        return ".float"

    def get_type(self):
        return "float"


class LLVMStore(LLVMAst):
    def __init__(self):
        super().__init__("LLVM Store")
        self.type = None


class LLVMAllocate(LLVMAst):
    def __init__(self, align, global_=False):
        super().__init__("LLVM Allocate")
        self.align = align
        self.global_ = bool(global_)
        self.type = None

    def __str__(self):
        return "{allo_type} {type} {align}".format(allo_type="Global" if self.global_ else "Alocate", type=self.type,
                                                   align=self.align)


class LLVMPrintStr(LLVMAst):
    def __init__(self, var, ccount):
        super().__init__(var)
        self.printvar = var
        self.ccount = ccount

    def __str__(self):
        return "Printstr {var}".format(var=self.printvar)

    def get_mips_type(self):
        return ".asciiz"

    def get_type(self):
        return "string"

    def get_str_value(self):
        return "\"" + self.printvar + "\""


class LLVMPrint(LLVMAst):
    def __init__(self, ccount):
        super().__init__("LLVM Print")
        self.ccount = ccount


class LLVMDeclare(LLVMAst):
    def __init__(self, fname):
        super().__init__(fname)
        self.name = fname
        self.rettype = None

    def __str__(self):
        return "Declare {rettype} {name}".format(rettype=self.rettype, name=self.name)


class LLVMLoad(LLVMAst):
    def __init__(self):
        super().__init__("LLVM Load")
        self.type = None

    def __str__(self):
        return "load {type}".format(type=self.type)


class LLVMReturn(LLVMAst):
    def __init__(self):
        super().__init__("LLVM return")
        self.type = None

    def __str__(self):
        return "return {type}".format(type=self.type)


class LLVMArgumentList(LLVMAst):
    def __init__(self):
        super().__init__("Argument List")


class LLVMArgument(LLVMAst):
    def __init__(self):
        super().__init__("Argument")
        self.type = None

    def __str__(self):
        return "Argument: {type}".format(type=self.type)


class LLVMUseArgumentList(LLVMAst):
    def __init__(self):
        super().__init__("Use Argument List")


class LLVMUseArgument(LLVMAst):
    def __init__(self):
        super().__init__("Use argument")
        self.type = None

    def __str__(self):
        return "Argument {type}".format(type=self.type)


class LLVMStringArgument(LLVMAst):
    def __init__(self, ccount):
        super().__init__("String")
        self.ccount = ccount

    def __str__(self):
        return "String Argument: {c} chars".format(c=self.ccount)

    def get_mips_type(self):
        return ".asciiz"


class LLVMLabel(LLVMAst):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def __str__(self):
        return "Label: {name}".format(name=self.name)


class LLVMExtension(LLVMOperation):
    def __init__(self, op):
        super().__init__(op)
        self.from_type = None
        self.to_type = None

    def __str__(self):
        return "{op} {from_} to {to_}".format(op=self.operation, from_=self.from_type, to_=self.to_type)


class LLVMBranch(LLVMAst):
    def __init__(self, branch_type):
        super().__init__(branch_type)


class LLVMNormalBranch(LLVMBranch):
    def __init__(self):
        super().__init__("Branch")


class LLVMConditionalBranch(LLVMBranch):
    def __init__(self):
        super().__init__("Conditional Branch")
        self.optype = None


class LLVMArrayIndex(LLVMAst):
    def __init__(self):
        super().__init__("Pointer index")
        self.type = None
        # self.index = index # in child

    def __str__(self):
        return "Index {}".format(self.type)


# TODO: use these classes as type in the other classes
class LLVMType(LLVMAst):
    def __init__(self, type):
        super().__init__(type)
        self.type = type

    def __str__(self):
        return self.type


class LLVMStringType(LLVMAst):
    def __init__(self, length):
        super().__init__("String")
        self.length = int(length)


class LLVMArrayType(LLVMType):
    def __init__(self, size):
        super().__init__("Array type")
        self.size = int(size)
        self.type = None

    def __str__(self):
        return "[{} x {}]".format(self.size, self.type)

from src.symbolTable import *
