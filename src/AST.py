# https://medium.com/@raguiar2/building-a-working-calculator-in-python-with-antlr-d879e2ea9058 (accessed on 6/3/2020 14:31)

from src.Node import *
from src.symbolTable import *


class AST:
    symbol_table = SymbolTable()

    def __init__(self, node=None):
        self.node = node
        self.parent = None
        self.children = list()

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

    def to_LLVM(self, file):
        file

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

    def plus(self, args):
        return args[0] + args[1]

    def min(self, args):
        return args[0] - args[1]

    def mult(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]

    def mod(self, args):
        return args[0] % args[1]

    def minU(self, args):
        return -args[0]

    def plusU(self, args):
        return +args[0]

    def traverse(self, func):
        func(self)
        for child in self.children:
            # func(child) # Why would you do this? you'll already do a func(self) when calling the traverse function of child
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

        funct = None

        if self.node.value == "+":
            if len(self.children) == 1:
                funct = self.plusU
            elif len(self.children) == 2:
                funct = self.plus
        elif self.node.value == "-":
            if len(self.children) == 1:
                funct = self.minU
            elif len(self.children) == 2:
                funct = self.min
        elif self.node.value == "*":
            funct = self.mult
        elif self.node.value == "/":
            funct = self.div
        elif self.node.value == "%":
            funct = self.mod

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
        self.node.value = str(funct(args))
        self.children = list()

        return True
