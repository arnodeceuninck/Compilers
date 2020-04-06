"""
!
"""
from src.ErrorListener import RerefError
from src.Utils import *
from abc import ABC, abstractmethod


class AST:
    id = 0

    def __init__(self, value: str = "", color: str = "#9f9f9f"):

        self.parent: AST = None
        self.children: list = list()

        self.value: str = value  # The text that's displayed in the dot tree
        self.color: str = color  # The color that's displayed in the dot tree
        self.funct = None  # The function that is applied for constant folding
        self.comment: str = ""  # Additional information as comment in the LLVM file

    # Returns always a unique number
    @staticmethod
    def get_id() -> int:
        AST.id += 1
        return AST.id

    # returns the dot representation of the given node
    def __str__(self):
        return '[label="{}", fillcolor="{}"] \n'.format(self.value, self.color)

    # Returns the type of the tree in LLVM
    def get_llvm_type(self) -> str:
        return "None"

    # A function that provides comments to put in the llvm code (end with \n)
    def comments(self, comment_out: bool = True) -> str:
        return ""

    # A function that generates the llvm code for the given tree (end with \n)
    # The first parameter is the code, the second parameter is the number of the calculated variable
    def llvm_code(self) -> (str, int):
        return "ERROR"

    def get_neutral(self) -> str:
        # 0.0 if float
        return "0"

    def get_llvm_print_type(self) -> str:
        # The only moment when this returns something else is with floats
        return self.get_llvm_type()

    @staticmethod
    def comment_out(comments: str, comment_out: bool):
        if not comment_out:
            return comments
        comment: str = ""
        for line in comments:
            comment = "; " + line
        return comment + '\n'

    @staticmethod
    def variable(var: int):
        return "%" + str(var)

    @staticmethod
    def goto(label: str):
        return "br label " + label + "\n"

    @staticmethod
    def label(name: str):
        return name + ":\n"


# A sequence of statements
class StatementSequence(AST):
    def __init__(self):
        AST.__init__(self, "Statement Sequence")

    def comments(self, comment_out=True):
        return self.comment_out("Code Block", comment_out)

    def get_llvm_type(self):
        # A statement sequence has no type
        return None

    def llvm_code(self):
        code = self.comments()
        for child in self.children:
            code += child.llvm_code()[0]
        code += '\n'
        return code

    # def collapse_comment(self, ast):
    #     for child in ast.children:
    #         child.node.collapse_comment(child)
    #     return ""


class If(AST):
    def __init__(self):
        AST.__init__(self, "if")

    def comments(self, comment_out=True):
        comment = "if " + self.children[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)

    def get_llvm_type(self):
        # An if statement has no type
        return None

    def llvm_code(self):
        code = self.comments()
        condition = self.children[0]

        condition_code, conditon_var = condition.llvm_code()
        code += condition_code

        label_true = "iftrue"
        label_false = "iffalse"
        code += "br {type} {var}, label {label_true}, label {label_false}\n".format(type="i1",
                                                                                    var=self.variable(conditon_var),
                                                                                    label_true=label_true,
                                                                                    label_false=label_false)

        label_end = "end"
        statement_sequence = self.children[1]
        code += self.label(label_true) + statement_sequence.llvm_code() + self.goto(label_end)

        code += self.label(label_false) + self.goto(label_end)
        code += self.label(label_end)

        code += '\n'
        return code

    # def collapse_comment(self, ast):
    #     self.comment = "if " + ast.children[0].node.collapse_comment(ast.children[0])
    #     ast.children[1].node.collapse_comment(ast.children[1])


# TODO
class For(AST):
    def __init__(self):
        AST.__init__(self, "for")

    def collapse_comment(self, ast):
        self.comment = "for "
        is_first = True
        for child in ast.children:
            if is_first:
                self.comment += child.node.collapse_comment(child)
                is_first = False
                continue
            self.comment += "; " + child.node.collapse_comment(child)


class Operator(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '[label="Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def get_type(self):
        type = self.children[0].get_type
        for child in self.children:
            if child.get_type != type:
                return None  # Todo: e.g. float and int
        return type

    # Has no own specific functions, is specified further in binary/unary/...


class Binary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)

    def collapse_comment(self, ast):
        self.comment = ast.children[0].node.collapse_comment(ast.children[0]) + self.value + \
                       ast.children[1].node.collapse_comment(ast.children[1])
        return self.comment

    def comments(self, comment_out=True):
        comment = self.children[0].comments(comment_out=False) + self.value + \
                  self.children[1].comments(comment_out=False)
        return self.comment_out(comment, comment_out)

    def get_llvm_type(self):
        if self.children[0].get_llvm_type == self.children[1].get_llvm_type:
            return self.children[0].get_llvm_type



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
        # If The right side is a variable then take the variable name not the node type
        if isinstance(ast.children[1].node, UDeref):
            return ast.node.get_LLVM().format(ast.children[0].getLLVMType(), "@",
                                              str(ast.children[1].getNodeInfo()), ast.children[0].getLLVMType(),
                                              "@", str(ast.children[0].getNodeInfo()))
        else:  # If the node wasnt a variable take the node id
            return ast.node.get_LLVM().format(ast.children[0].getLLVMType(), "%", str(ast.children[1]),
                                              ast.children[0].getLLVMType(), "@",
                                              str(ast.children[0].getNodeInfo()))

    def collapse_comment(self, ast):
        self.comment = ast.children[0].node.collapse_comment(ast.children[0]) + self.value + \
                       ast.children[1].node.collapse_comment(ast.children[1])
        return self.comment

    def llvm_code(self):
        code = self.comments()

        code += "store "

        code += self.children[0].get_llvm_type + " "

        # If The right side is a variable then take the variable name not the node type
        if isinstance(self.children[1].node, UDeref):
            code += "@" + str(self.children[1].getNodeInfo())
        # If the node wasn't a variable take the node id
        else:
            code += "%" + str(self.children[1])

        code += ", "
        code += self.children[0].getLLVMType() + "* "
        code += "@" + str(self.children[0].getNodeInfo())

        return code



# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.constant import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Operate import *
from src.Node.Comments import *
