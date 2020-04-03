from src.Node.Node import *


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)
        self.funct = None

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getType(self, args):
        return args[0]  # Only one type as argument

    def generate_LLVM(self, ast):
        return ""


class UPlus(Unary):
    def __init__(self, value="+"):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fadd {} {}{}, 0.0\n"
        return "{}{} = add {} {}{}, 0\n"

    def generate_LLVM(self, ast):
        output = ""
        is_float = ast.getType() == "float"
        type = ast.getLLVMType()
        tempvar1 = str(ast.children[0])
        if isinstance(ast.children[0].node, Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += get_LLVM_load().format("%", tempvar1, type, type, "@", ast.children[0].node.value)

        output += ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1)
        return output


class UMinus(Unary):
    def __init__(self, value="-"):
        Unary.__init__(self, value)
        self.funct = lambda args: -args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fsub {} 0.0, {}{}\n"
        return "{}{} = sub {} 0, {}{}\n"

    def generate_LLVM(self, ast):
        output = ""
        is_float = ast.getType() == "float"
        type = ast.getLLVMType()
        tempvar1 = str(ast.children[0])
        if isinstance(ast.children[0].node, Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += get_LLVM_load().format("%", tempvar1, type, type, "@", ast.children[0].node.value)

        output += ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1)
        return output


class UDMinus(Unary):
    def __init__(self, value="--"):
        Unary.__init__(self, value)
        self.funct = lambda args: args[0] - 1


class UDPlus(Unary):
    def __init__(self, value="++"):
        Unary.__init__(self, value)
        self.funct = lambda args: args[0] - 1


class UNot(Unary):
    def __init__(self, value="!"):
        Unary.__init__(self, value)
        self.funct = lambda args: not args[0]

    def get_LLVM(self, is_float):
        if is_float:
            return "{}{} = fcmp oeq {} {}{}, 0.0\n"
        return "{}{} = icmp eq {} {}{}, 0\n"

    def generate_LLVM(self, ast):
        output = ""
        is_float = ast.getType() == "float"
        type = ast.getLLVMType()
        tempvar1 = "t" + str(ast.node.get_id())
        if isinstance(ast.children[0].node, Variable):
            output += get_LLVM_load().format("%", tempvar1, type, type, "@", ast.children[0].node.value)

            tempvar2 = "t" + str(ast.node.get_id())

            output += UNot().get_LLVM(is_float).format("%", tempvar2, type, "%", tempvar1)
            output += CBool().convertString(type).format("%", str(ast), "%", tempvar2)
        return output


class UDeref(Unary):
    def __init__(self, value="&"):
        Unary.__init__(self, value)

    def getType(self, args):
        return args[0] + "*"


class UReref(Unary):
    def __init__(self, value="*"):
        Unary.__init__(self, value)

    def getType(self, args):
        if args[0][len(args[0]) - 1] != "*":
            raise RerefError()
        return args[0][:len(args[0]) - 1]

    def generate_LLVM(self, ast):
        output = ast.children[0].node.generate_LLVM(ast.children[0])
        type = ast.getLLVMType()
        # Load the value into the ast node
        output += get_LLVM_load().format("%", str(ast), type[:-1], type[:-1], "%", str(ast.children[0]))
        return output


class Print(Unary):
    def __init__(self, value="printf"):
        Unary.__init__(self, value)

    def getType(self, args):
        return "function"

    def generate_LLVM(self, ast):
        # Generate LLVM for the node that needs to be printed
        output = ast.children[0].node.generate_LLVM(ast)
        formatType = ast.children[0].node.getFormatType()
        printType = ast.children[0].node.getLLVMPrintType()

        if isinstance(ast.children[0].node, Variable):
            if printType == "double":
                output += VFloat().convertString("double").format("%", str(ast), "%", str(ast.children[0]))
        output += printString.format(formatType, printType, "%", str(ast))
        return output
