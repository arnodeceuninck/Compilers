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
    # Constructor of the AST class
    def __init__(self, tree: ParserRuleContext):
        self.children = list()
        self.parent = None
        self.node = Node(tree)
        if not tree.getChildCount():
            return

        child: ParserRuleContext
        for child in tree.getChildren():
            tempChild = AST(child)
            tempChild.parent = self
            self.children.append(tempChild)
            # self.children.append(AST(child))


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

    def is_leaf(self):
        return self.children.count()

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
