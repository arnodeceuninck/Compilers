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
    symbol_table = SymbolTable()

    def __init__(self, node=None):
        self.node = node
        self.parent = None
        self.children = list()
        AST_old.symbol_table = SymbolTable()  # symbol table must reset after each test

    def childIndex(self, ast):
        return self.children.index(ast)

    def simplifyTree(self):
        for idx in range(0, len(self.children)):
            if len(self.children[idx].children) == 1:
                self.children[idx] = self.children[idx].children[0]
                self.children[idx].parent = self
                self.simplifyTree()
            else:
                self.children[idx].simplifyTree()

    def __str__(self):
        returnStr = ""
        if self.parent:
            returnStr += "N"
            returnStr += str(self.parent.childIndex(self))
            returnStr += str(self.parent)
        else:
            returnStr += "T"
        return returnStr

    def to_LLVM(self, filename):
        output = ""
        symbol_table = self.symbol_table.elements
        ptr_types = list()
        # generate variable declarations from the symbol table
        for var in symbol_table:
            # define all the variables
            LLVM_var_name = "@" + var
            ptr = "*" if symbol_table[var].type.ptr else ""
            LLVM_align = "align"
            if symbol_table[var].type.const:
                LLVM_type = "constant"
            else:
                LLVM_type = "global"
            LLVM_type += " {} undef".format(symbol_table[var].type.getLLVMType())
            LLVM_align += " {}".format(symbol_table[var].type.getAlign())
            output += LLVM_var_name + " = {}, {}\n".format(LLVM_type, LLVM_align)
        output += "\n"
        output += "define i32 @main() {\n"
        retval = generate_LLVM(self)
        output += retval[0]

        output += "ret i32 0\n"
        output += "}\n\n"

        # If we need to print then create the print function
        if len(retval[1]):
            for char in retval[1]:
                output += '@.str{formatType} = private unnamed_addr constant [4 x i8] c"%{formatType}\\0A\\00"' \
                          ', align 1\n'.format(formatType=char)
            output += 'declare i32 @printf(i8*, ...)\n'

        # Write output to the outputfile
        outputFile = open(filename, "w")
        outputFile.write(output)
        outputFile.close()

    def dotNode(self):
        # The output needs to be the id + The label itself
        output = str(self)
        output += str(self.node)

        for child in self.children:
            output += child.dotNode()

        return output

    def dotConnections(self):
        output = ""
        for child in self.children:
            output += str(self) + " -> " + str(child) + "\n"
            output += child.dotConnections()

        return output

    # Print the tree in dot
    def to_dot(self, filename):
        output = "Digraph G { \n"
        # Add symbol table
        output += str(self.symbol_table)
        output += "subgraph cluster_1 {\n"
        output += "node [style=filled, shape=rectangle, penwidth=2];\n"

        output += self.dotNode()
        output += self.dotConnections()

        output += "label = \"AST\";\n"
        output += "}\n"
        output += "}"

        outputFile = open(filename, "w")
        outputFile.write(output)
        outputFile.close()

    def traverse(self, func):
        func(self)
        for child in self.children:
            child.traverse(func)

    # Does nothing with Comparison operators or logical operators
    def constant_folding(self):
        if isinstance(self.node, Variable):
            # You can't fold variables
            return False
        if isinstance(self.node, (CInt, CFloat)):
            # Ints and floats are already folded
            return True

        ready_to_continue_folding = True  # Only ready to continue if all children are
        for i in range(len(self.children)):
            # must iterate over i, because for child in self.children doesn't work by reference
            ready_to_continue_folding = self.children[i].constant_folding() and ready_to_continue_folding

        if not ready_to_continue_folding:
            # Can only continue folding if all children have folded properly
            return False

        funct = self.node.funct

        if funct is None:
            return False  # Can't continue folding if the function is unknown for folding

        args = list()
        # We need the right type of node, because compiling wrong type can cause issues
        node = None
        for child in self.children:
            try:
                args.append(float(child.node.value))
                # Set the type of the node to one of the children
                node = child.node
            except ValueError:
                return False  # Can't continue folding if one of the children isn't a float

        # Set the node type to the correct value
        self.node = node
        self.node.set_value(float(funct(args)))
        self.children = list()

        return True

    def getType(self):
        args = list()
        for child in self.children:
            args.append(child.getType())
        return self.node.getType(args)
        # if isinstance(self.node, Variable):
        #     return self.symbol_table[self.node.value]
        # elif isinstance(self.node, CFloat):
        #     return "float"
        # elif isi

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
