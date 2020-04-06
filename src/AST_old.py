# https://medium.com/@raguiar2/building-a-working-calculator-in-python-with-antlr-d879e2ea9058 (accessed on 6/3/2020 14:31)
from src.Node.AST import *
from src.Node.Unary import *
from src.symbolTable import *
from src.Operations import *


def insert_comments(ast):
    output = ""
    formatTypes = set()
    # If the ast node is a sequence then the nodes below it can be instructions,
    # but this node means nothing in code generation
    if isinstance(ast.node, StatementSequence):
        for child in ast.children:
            child.node.collapse_comment(child)


def generate_LLVM(ast):
    output = ""
    formatTypes = set()
    # If the ast node is a sequence then the nodes below it can be instructions,
    # but this node means nothing in code generation
    if isinstance(ast.node, StatementSequence):
        for child in ast.children:
            tempret = generate_LLVM(child)
            output = handle_return(tempret, output, formatTypes)
    # If we encounter a variable then we do not need to do anything because it is already assigned
    elif isinstance(ast.node, (UPlus, UMinus, UNot, UReref, Variable, Constant)):
        if isinstance(ast.node, (Assign, Unary)):
            output += "; " + ast.node.comment + "\n"
        output += ast.node.generate_LLVM(ast)
    # If we encounter an Binary operate then we need to operate on its children
    elif isinstance(ast.node, Assign):
        output += "; " + ast.node.comment + "\n"
        # generate LLVM for the left and right side of the operator
        tempret = generate_LLVM(ast.children[1])
        output = handle_return(tempret, output, formatTypes)

        output += ast.node.generate_LLVM(ast)
    elif isinstance(ast.node, Binary):
        output += "; " + ast.node.comment + "\n"
        # generate LLVM for the left and right side of the operator
        for child in ast.children:
            tempret = generate_LLVM(child)
            output = handle_return(tempret, output, formatTypes)

        output += ast.node.generate_LLVM(ast)
    elif isinstance(ast.node, Print):
        output += "; " + ast.node.comment + "\n"
        output += ast.node.generate_LLVM(ast)
        formatType = ast.children[0].node.getFormatType()
        formatTypes.add(formatType)
    elif isinstance(ast.node, UDeref):
        pass
    elif isinstance(ast.node, (If, For)):
        output += "; " + ast.node.comment + "\n"
    return output, formatTypes


class AST_old:


    def __init__(self, node=None):
        self.node = node
        self.parent = None
        self.children = list()
        AST_old.symbol_table = SymbolTable()  # symbol table must reset after each test


    def getLLVMType(self):
        this = self
        # If this is an operator or statement sequence then we can't deduce its type so we need
        # to assign the left most child since it is always the correct type
        while isinstance(this.node, Operator) or isinstance(this.node, StatementSequence):
            this = this.children[0]
        return this.node.getLLVMType()

    def getNeutral(self):
        this = self
        # If this is an operator or statement sequence then we can't deduce its type so we need
        # to assign the left most child since it is always the correct type
        while isinstance(this.node, Operator) or isinstance(this.node, StatementSequence):
            this = this.children[0]
        return this.node.getNeutral()

    # Returns the expected value
    def getNodeInfo(self):
        if isinstance(self.node, Variable):
            return self.node.value
        elif isinstance(self.node, UDeref) or isinstance(self.node, UReref):
            return self.children[0].node.value
        return str(self)

    def getValue(self):
        if isinstance(self.node, CChar):
            return ord(self.node.value[1])
        return self.node.value
