"""
!
"""
from src.ErrorListener import RerefError, CompilerError, ConstError, IncompatibleTypesError, CustomErrorListener
from src.symbolTable import SymbolTable
from gen import cParser, cLexer
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker


# An error checking functions to check whether all symbols are already in the symbol table (or insert them when declaring)
def assignment(ast):
    # Check whether any other symbol is already in the symbol table

    if isinstance(ast, Variable) and ast.parent and isinstance(ast.parent, Assign):
        # return not required here, but otherwise pycharm thinks the statement is useless
        return ast.symbol_table[ast.value]  # Raises an error if not yet declared

    # Add symbol to symbol table
    if ast.value == "=" and ast.declaration:
        # improve type without constant and ptr
        location = ast.children[0].value
        type = ast.children[0]
        ast.symbol_table.insert(location, type)

    # Last minute fix before the evaluation
    # (already forgot what it does)
    if isinstance(ast, Variable) and ast.parent and not (
            isinstance(ast.parent, Assign) or isinstance(ast.parent, Print) or isinstance(ast.parent,
                                                                                          Unary) or isinstance(
        ast.parent, Binary)):
        location = ast.value
        type = ast
        ast.symbol_table.insert(location, type)


# Converts all variables into the right type.
# e.g. int x = y, y will be a variable from the listener, but must be the right type
# (correct me if I'm wrong)
def convertVar(ast):
    if not isinstance(ast, Variable):
        return
    if isinstance(ast, Print):
        return
    element = ast.symbol_table[ast.value].type
    # TODO: This should be done from the listener
    type = element.get_type()
    while type[len(type) - 1] == "*":
        type = type[:len(type) - 1]
    if type == 'int':
        ast_new = VInt(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast.parent.replace_child(ast, ast_new)
    elif type == 'float':
        ast_new = VFloat(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast.parent.replace_child(ast, ast_new)
    elif type == 'char':
        ast_new = VChar(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast.parent.replace_child(ast, ast_new)


# A function to check whether you're always assigning to the right type and not to a const value
def checkAssigns(ast):
    # Check for const assigns
    # On assignments that are declarations, but the leftmost child is a const variable
    if isinstance(ast, Assign) and ast.children[0].const and not ast.declaration:
        raise ConstError(ast.children[0].value)
    if isinstance(ast, Assign):
        type_lvalue = ast.children[0].get_type()
        type_rvalue = ast.children[1].get_type()
        if type_lvalue == type_rvalue:
            pass
        elif type_lvalue == "float" and type_rvalue == "int":
            pass
        else:
            raise IncompatibleTypesError(type_lvalue, type_rvalue)


# return an ast tree from an input file
def compile(input_file: str, catch_error=True):
    input_stream = FileStream(input_file)
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    parser.addErrorListener(CustomErrorListener())
    tree = parser.start_rule()

    if catch_error:
        try:
            return make_ast(tree)
        except CompilerError as e:
            print(str(e))
            return None
    else:
        return make_ast(tree)


# Convert an antlr tree into our own AST
def make_ast(tree):
    communismRules = customListener()
    walker = ParseTreeWalker()
    walker.walk(communismRules, tree)
    communismForLife = communismRules.trees[0]
    # The two methods of below should be combined in order to make it one pass and apply error checking
    # Create symbol table
    communismForLife.traverse(assignment)  # Symbol table checks
    # # Apply symbol table to all the variables
    communismForLife.traverse(convertVar)  # Qua de la fuck does this? -> Convert Variables into their right type
    communismForLife.traverse(checkAssigns)  # Check right type assigns, const assigns ...
    return communismForLife


# Write the llvm version of the ast to the filename
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

    # Resets the global class variables (must be used with tests)
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

    # Get the child at index item using self[item]
    def __getitem__(self, item: int):  # -> AST
        return self.children[item]

    # Preorder traverse with a given funciton
    def traverse(self, func):
        func(self)
        for child in self.children:
            child.traverse(func)

    # Fold the constants where possible
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

    # Represent the nodes for the dotfile
    def dot_node(self):
        # The output needs to be the id + The label itself
        output = str(self)

        for child in self.children:
            output += child.dot_node()

        return output

    # represent the connections for the dotfile
    def dot_connections(self):
        output = ""
        for child in self.children:
            output += str(self.id()) + " -> " + str(child.id()) + "\n"
            output += child.dot_connections()
        return output

    # Replace the child tree_from with tree_to
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

    # returns the c_type
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

    # Comment out a given string if required
    @staticmethod
    def comment_out(comments: str, comment_out: bool):
        if not comment_out:
            return comments
        comments = "; " + comments
        return comments + '\n'

    # The llvm template for loading a variable from storage
    def llvm_load_template(self):
        # Code for loading a variable (default is no loading required)
        return "{result} = load {type}, {type}* {var}\n"

    # Get the unique ID of this subtree
    def id(self):
        if not self._id:
            self._id = self.get_unique_id()
        return self._id

    # Get the variable for the node (and load it from memory if required)
    # Store must be true when you want to store into the variable
    def variable(self, store: bool = False):
        # TOdo: move this to their own classes (virtual functions)
        if isinstance(self, Variable):
            if store:
                return "@" + self.value
            var = "%" + str(self.get_unique_id())
            self.llvm_load(var)  # Loads the variable in storage into the variable var
            return var
        elif isinstance(self, UDeref) and store:
            return self[0].variable(store)

        var = self.id()

        return "%v" + str(var)

    # Get a unique temp variable
    @staticmethod
    def get_temp():
        return "%t" + str(AST.get_unique_id())

    # Jump to a given label
    @staticmethod
    def goto(label: str):
        AST.llvm_output += "br label " + label + "\n"

    # Create a new label
    @staticmethod
    def label(name: str):
        return name + ":\n"


# Convert given ast into a dotfile and write it to filename
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
        # TODO: fix
        AST.llvm_output += self.comments()

        condition = self.children[0]
        condition.llvm_code()

        label_true = "iftrue"
        label_false = "iffalse"
        code = "br {type} {var}, label {label_true}, label {label_false}\n"
        code = code.format(type="i1",
                           var=condition.variable(),
                           label_true=label_true,
                           label_false=label_false)
        AST.llvm_output += code

        label_end = "end"
        statement_sequence = self.children[1]
        AST.llvm_output += self.label(label_true) + "\n"
        statement_sequence.llvm_code()
        self.goto(label_end)

        AST.llvm_output += self.label(label_false) + "\n"
        self.goto(label_end)
        AST.llvm_output += self.label(label_end) + '\n'


# TODO
class For(AST):
    def __init__(self):
        AST.__init__(self, "for")

    def comments(self, comment_out=True):
        comment = "for " + self[0].comments()  # only add comments for the condition, the comments for the statement
        # sequence will be added when visiting their code
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        AST.llvm_output += self.comments()


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
        return '{name}[label="Binary Operator: {value}", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                         value=self.value,
                                                                                         color=self.color)

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
        code = code.format(type=self[0].get_llvm_type(), temp=self[1].variable(store=True),
                           location=self[0].variable(store=True))

        output += code

        AST.llvm_output += output


# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.constant import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Operate import *
from src.Node.Comments import *
from src.customListener import customListener
