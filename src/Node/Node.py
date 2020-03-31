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


class If(Node):
    def __init__(self):
        Node.__init__(self, "if")


class For(Node):
    def __init__(self):
        Node.__init__(self, "for")


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


# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.constant import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Operate import *
from src.Node.Comments import *
