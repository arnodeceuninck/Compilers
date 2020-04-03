"""
!
"""
from src.ErrorListener import RerefError
from src.Utils import *


class Node:
    id = 0

    def __init__(self, value="", color="#9f9f9f"):
        self.value = value
        self.color = color
        self.funct = None
        self.comment = ""

    @staticmethod
    def get_id():
        Node.id += 1
        return Node.id

    def __str__(self):
        return '[label="{}", fillcolor="{}"] \n'.format(self.value, self.color)

    def getLLVMType(self):
        return ""


class StatementSequence(Node):
    def __init__(self):
        Node.__init__(self, "Statement Sequence")

    def collapse_comment(self, ast):
        for child in ast.children:
            child.node.collapse_comment(child)
        return ""


class If(Node):
    def __init__(self):
        Node.__init__(self, "if")

    def collapse_comment(self, ast):
        self.comment = "if " + ast.children[0].node.collapse_comment(ast.children[0])
        ast.children[1].node.collapse_comment(ast.children[1])


class For(Node):
    def __init__(self):
        Node.__init__(self, "for")

    def collapse_comment(self, ast):
        self.comment = "for "
        is_first = True
        for child in ast.children:
            if is_first:
                self.comment += child.node.collapse_comment(child)
                is_first = False
                continue
            self.comment += "; " + child.node.collapse_comment(child)


class Operator(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '[label="Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class Binary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def collapse_comment(self, ast):
        self.comment = ast.children[0].node.collapse_comment(ast.children[0]) + self.value + \
                       ast.children[1].node.collapse_comment(ast.children[1])
        return self.comment


class Assign(Binary):
    def __init__(self, value="="):
        Binary.__init__(self, value)
        self.declaration = True

    def __str__(self):
        if self.declaration:
            return '[label="Assign Declaration", fillcolor="{}"] \n'.format(self.color)
        return '[label="Assign", fillcolor="{}"] \n'.format(self.color)

    def get_LLVM(self):
        return "store {} {}{}, {}* {}{}\n"

    def generate_LLVM(self, ast):
        output = ast.children[1].node.generate_LLVM(ast.children[1])
        # If The right side is a variable then take the variable name not the node type
        if isinstance(ast.children[1].node, UDeref):
            output += ast.node.get_LLVM().format(ast.children[0].getLLVMType(), "@",
                                                 str(ast.children[1].getNodeInfo()), ast.children[0].getLLVMType(),
                                                 "@", str(ast.children[0].getNodeInfo()))
        else:  # If the node wasnt a variable take the node id
            output += ast.node.get_LLVM().format(ast.children[0].getLLVMType(), "%", str(ast.children[1]),
                                                 ast.children[0].getLLVMType(), "@",
                                                 str(ast.children[0].getNodeInfo()))
        return output

    def collapse_comment(self, ast):
        self.comment = ast.children[0].node.collapse_comment(ast.children[0]) + self.value + \
                       ast.children[1].node.collapse_comment(ast.children[1])
        return self.comment


# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.constant import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Operate import *
from src.Node.Comments import *
