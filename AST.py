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
        # self.left = None
        # self.right = None
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
        output = ""
        output += str(self)
        output += '[label="{}"] \n'.format(str(self.node))

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
    def print_dot(self):
        output = "Digraph G { \n"

        output += self.dotNode()
        output += self.dotConnections()

        output += "}"

        outputFile = open("c_tree.dot", "w")
        outputFile.write(output)

