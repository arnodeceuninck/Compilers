"""
!
"""
from src.ErrorListener import RerefError
from src.Utils import *
from abc import ABC, abstractmethod
from src.symbolTable import SymbolTable


def to_LLVM(ast, filename):
    AST.llvm_output = ""

    symbol_table = ast.symbol_table.elements
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
        LLVM_type += " {} undef".format(symbol_table[var].type.get_llvm_type())
        LLVM_align += " {}".format(symbol_table[var].type.get_align())
        AST.llvm_output += LLVM_var_name + " = {}, {}\n".format(LLVM_type, LLVM_align)
    AST.llvm_output += "\n"
    AST.llvm_output += "define i32 @main() {\n\n"

    ast.llvm_code()

    AST.llvm_output += "\n"
    AST.llvm_output += "ret i32 0\n"
    AST.llvm_output += "}\n\n"

    # If we need to print then create the print function
    if AST.print:
        print = "@.strc = private unnamed_addr constant [4 x i8] c\"%c\\0A\\00\", align 1\n"
        print += "@.strd = private unnamed_addr constant [4 x i8] c\"%d\\0A\\00\", align 1\n"
        print += "@.strf = private unnamed_addr constant [4 x i8] c\"%f\\0A\\00\", align 1\n"
        print += "declare i32 @printf(i8*, ...)\n"
        AST.llvm_output += print

    # Write output to the outputfile
    outputFile = open(filename, "w")
    outputFile.write(AST.llvm_output)
    outputFile.close()


class AST:
    _id = 0
    llvm_output = ""
    symbol_table = SymbolTable()
    print = False

    @staticmethod
    def reset():
        AST.llvm_output = ""
        AST.symbol_table = SymbolTable
        AST._id = 0

    def __init__(self, value: str = "", color: str = "#9f9f9f"):

        self._id = 0

        self.parent: AST = None
        self.children: list = list()

        self.value: str = value  # The text that's displayed in the dot tree
        self.color: str = color  # The color that's displayed in the dot tree
        self.funct = None  # The function that is applied for constant folding
        self.comment: str = ""  # Additional information as comment in the LLVM file

    def __getitem__(self, item: int):  # -> AST
        return self.children[item]

    def traverse(self, func):
        func(self)
        for child in self.children:
            child.traverse(func)

    def constant_folding(self):
        ready_to_continue_folding = True  # Only ready to continue if all children are
        for i in range(len(self.children)):
            # must iterate over i, because for child in self.children doesn't work by reference
            ready_to_continue_folding = self.children[i].constant_folding() and ready_to_continue_folding

        if not ready_to_continue_folding:
            # Can only continue folding if all children have folded properly
            return False

        funct = self.funct

        if funct is None:
            return False  # Can't continue folding if the function is unknown for folding

        args = list()
        # We need the right type of node, because compiling wrong type can cause issues
        child_tree = None
        for child in self.children:
            try:
                args.append(float(child.value))
                # Set the type of the node to one of the children
                child_tree = child
            except ValueError:
                return False  # Can't continue folding if one of the children isn't a float

        # Set the node type to the correct value
        child_tree.parent = self.parent
        child_tree.set_value(float(funct(args)))
        child_tree.children = list()
        self.parent.replace_child(self, child_tree)

        return True

    def dot_node(self):
        # The output needs to be the id + The label itself
        output = str(self)

        for child in self.children:
            output += child.dot_node()

        return output

    def dot_connections(self):
        output = ""
        for child in self.children:
            output += str(self.id()) + " -> " + str(child.id()) + "\n"
            output += child.dot_connections()
        return output

    def replace_child(self, tree_from, tree_to):
        if tree_from.parent != self:
            raise Exception("ast should be my child")
        for i in range(len(self.children)):
            if self[i] == tree_from:
                self.children[i] = tree_to
                tree_to.parent = self
                break


    # Returns always a unique number
    @staticmethod
    def get_unique_id() -> int:
        AST._id += 1
        return AST._id

    # returns the dot representation of the given node
    def __str__(self):
        return '{name}[label="{value}", fillcolor="{color}"] \n'.format(name=self.id(), value=self.value,
                                                                        color=self.color)

    # Returns the type of the tree in LLVM
    def get_llvm_type(self) -> str:
        return "NONE"

    def get_type(self) -> str:
        return ""

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
        comments = "; " + comments
        return comments + '\n'

    def llvm_load_template(self):
        # Code for loading a variable (default is no loading required)
        return "{result} = load {type}, {type}* {var}\n"

    def id(self):
        if not self._id:
            self._id = self.get_unique_id()
        return self._id

    # Get the variable for the node (and load it from memory if required)
    # Store must be true when you want to store into the variable
    def variable(self, store: bool=False):
        if isinstance(self, Variable):
            if store:
                return "@" + self.value
            var = "%" + str(self.get_unique_id())
            self.llvm_load(var) # Loads the variable in storage into the variable var
            return var

        var = self.id()

        return "%v" + str(var)

    @staticmethod
    def get_temp():
        return "%t" + str(AST.get_unique_id())

    @staticmethod
    def goto(label: str):
        return "br label " + label + "\n"

    @staticmethod
    def label(name: str):
        return name + ":\n"


def dot(ast: AST, filename: str):
    output = "Digraph G { \n"

    # Add symbol table
    output += str(ast.symbol_table)
    output += "subgraph cluster_1 {\n"
    output += "node [style=filled, shape=rectangle, penwidth=2];\n"

    output += ast.dot_node()
    output += ast.dot_connections()

    output += "label = \"AST\";\n"
    output += "}\n"
    output += "}"

    outputFile = open(filename, "w")
    outputFile.write(output)
    outputFile.close()


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
        AST.llvm_output += self.comments()
        for child in self.children:
            child.llvm_code()
        AST.llvm_output += '\n'

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
        AST.llvm_output += code

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
        return '{name}[label="Operator: {value}", fillcolor="{color}"] \n'.format(name=self.id(), value=self.value,
                                                                                  color=self.color)

    def get_type(self):
        type = self.children[0].get_type()
        for child in self.children:
            if child.get_type() != type:
                return None
        return type

    def get_llvm_type(self):
        type = self.children[0].get_llvm_type()
        for child in self.children:
            if child.get_llvm_type() != type:
                return None
        return type

    # Has no own specific functions, is specified further in binary/unary/...


class Binary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '{name}[label="Binary Operator: {value}", fillcolor="{color}"] \n'.format(name=self.id(), value=self.value, color=self.color)

    def comments(self, comment_out=True):
        comment = self[0].comments(comment_out=False) + self.value + \
                  self[1].comments(comment_out=False)
        return self.comment_out(comment, comment_out)

    def get_llvm_type(self):
        if self.children[0].get_llvm_type() == self.children[1].get_llvm_type():
            return self.children[0].get_llvm_type()


class Assign(Binary):
    def __init__(self, value="="):
        Binary.__init__(self, value)
        self.declaration = True

    def __str__(self):
        if self.declaration:
            return '{name}[label="Assign Declaration", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)
        return '{name}[label="Assign", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)

    def get_llvm_template(self):
        return "store {type} {temp}, {type}* {location}\n"


    def collapse_comment(self, ast):
        self.comment = ast.children[0].node.collapse_comment(ast.children[0]) + self.value + \
                       ast.children[1].node.collapse_comment(ast.children[1])
        return self.comment

    def llvm_code(self):

        # First calculate the value to store
        self[1].llvm_code()

        output = self.comments()

        code = self.get_llvm_template()
        code = code.format(type=self[0].get_llvm_type(), temp=self[1].variable(), location=self[0].variable(store=True))

        output += code

        AST.llvm_output += output


# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.constant import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Operate import *
from src.Node.Comments import *
