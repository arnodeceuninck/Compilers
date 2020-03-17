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
    def print_dot(self, filename):
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

    def plus(self, x, y):
        return x + y

    def min(self, x, y):
        return x - y

    def mult(self, x, y):
        return x * y

    def div(self, x, y):
        return x / y

    def mod(self, x, y):
        return x % y

    def minU(self, x):
        return -x

    def plusU(self, x):
        return +x

    def traverse(self, func):
        func(self)
        for child in self.children:
            # func(child) # Why would you do this? you'll already do a func(self) when calling the traverse function of child
            child.traverse(func)

    # Does nothing with Comparison operators or logical operators
    def constant_folding(self):
        binary = True
        funct = None
        # Special case for when we are in the root
        if self.node.value == "Statement Sequence" or self.node.value == "=" or isinstance(self.node, Variable):
            for child in self.children:
                child.constant_folding()
            return

        if self.node.value == "+":
            if len(self.children) == 1 and not isinstance(self.children[0], Variable):
                funct = self.plusU
                binary = False
            elif len(self.children) == 1:
                binary = False
            elif not isinstance(self.children[0], Variable) and not isinstance(self.children[1], Variable):
                funct = self.plus
        elif self.node.value == "-":
            if len(self.children) == 1 and not isinstance(self.children[0], Variable):
                funct = self.minU
                binary = False
            elif len(self.children) == 1:
                binary = False
            elif not isinstance(self.children[0], Variable) and not isinstance(self.children[1], Variable):
                funct = self.min
        elif self.node.value == "*" and not isinstance(self.children[0], Variable) and not isinstance(self.children[1],
                                                                                                      Variable):
            funct = self.mult
        elif self.node.value == "/" and not isinstance(self.children[0], Variable) and not isinstance(self.children[1],
                                                                                                      Variable):
            funct = self.div
        elif self.node.value == "%" and not isinstance(self.children[0], Variable) and not isinstance(self.children[1],
                                                                                                      Variable):
            funct = self.mod
        elif len(self.children) == 0:
            try:
                return True, float(self.node.value)
            except ValueError:
                # The casting of value to float has failed
                return False, None

        left = None
        right = None
        for child in self.children:
            result = child.constant_folding()
            if left is None:
                left = result
            elif right is None:
                right = result

        # Check whether the subtrees where able to const fold successfully
        if funct is not None and left is not None and left[0]:
            if binary:
                if not right[0]:
                    return False
                self.node = CInt(funct(left[1], right[1]))
            elif not binary:
                self.node = CInt(funct(left[1]))
            self.children = []
            return True, self.node.value
        else:
            return False
