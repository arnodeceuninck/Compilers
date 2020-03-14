# https://medium.com/@raguiar2/building-a-working-calculator-in-python-with-antlr-d879e2ea9058 (accessed on 6/3/2020 14:31)

from antlr4 import *
from gen import cParser


class Node:
    def __init__(self, tree_node: ParserRuleContext):
        if tree_node.getChildCount():
            self.string = cParser.cParser.ruleNames[tree_node.getRuleIndex()]
        else:
            self.string = tree_node.getText()

    def __str__(self):
        return str(self.string)


class AST:

    def __init__(self, value=None):
        self.value = value
        self.parent = None
        self.node = None
        self.children = list()
        pass

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
        # The output needs to be the id + The contents of the labels
        output = str(self)
        output += '[label="{}"] \n'.format(self.value)

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

        output += self.dotNode()
        output += self.dotConnections()

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

    # Does nothing with Comparison operators or logical operators
    def constant_folding(self):
        binary = True
        funct = None
        # Special case for when we are in the root
        if self.value == "Root":
            for child in self.children:
                child.constant_folding()
            return

        if self.value == "+":
            if len(self.children) == 1:
                funct = self.plusU
                binary = False
            else:
                funct = self.plus
        elif self.value == "-":
            if len(self.children) == 1:
                funct = self.minU
                binary = False
            else:
                funct = self.min
        elif self.value == "*":
            funct = self.mult
        elif self.value == "/":
            funct = self.div
        elif self.value == "%":
            funct = self.mod
        elif len(self.children) == 0:
            try:
                return True, float(self.value)
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

        # Check whether the substrees where able to const fold succesfully
        if funct is not None and left[0]:
            if binary:
                if not right[0]:
                    return False
                self.value = funct(left[1], right[1])
            elif not binary:
                self.value = funct(left[1])
            self.children = []
            return True, self.value
        else:
            return False
