"""
!
"""

from src.symbolTable import SymbolTable

# NOTE the parts referenced here are the parts described in the function get_llvm_print of the class Function
# This string belongs to the first part
stringVar = '@.str.{string_id} = private unnamed_addr constant [{string_len} x i8] c"{string_val}", align 1\n'
# This string belongs to the second part
stringArg = 'i8* getelementptr inbounds ([{string_len} x i8], [{string_len} x i8]* @.str.{string_id}, i32 0, i32 0)'
stringCall = '\tcall i32 (i8*, ...) @printf({string_arg})\n'

scanCall = "\tcall i32 (i8*, ...) @__isoc99_scanf({scan_arg})\n"


class AST:
    _id = 0
    # symbol_table = SymbolTable() Removing the symbol table from the ast as a static variable
    # -> found in the statement sequences
    # These two variables are necessary for supporting scanning and printing with stdio
    print = False
    scan = False
    main = False  # Value for if main is in the AST
    contains_function = False  # Check whether you have to manually add the int main()
    stdio = False  # Indicates if stdio is used
    functions = list()  # This list contains all the functions that it are declared on the pre-order traversal

    # Resets the global class variables (must be used with tests)
    @staticmethod
    def reset():
        AST.symbol_table = SymbolTable
        AST._id = 0
        # These two variables are necessary for supporting scanning and printing with stdio
        AST.print = False
        AST.scan = False
        # Value for if main is in the AST
        AST.main = False
        # Check whether you have to manually add the int main()
        AST.contains_function = False
        # Indicates if stdio is used
        AST.stdio = False
        # This list contains all the functions that it are declared on the pre-order traversal
        AST.functions = list()

    def get_llvm_string_len(self, string) -> int:
        nr_backslashes = 0
        # We need to count the \ in the string in order to get the right amount of characters
        for character in string:
            if character == "\\":
                nr_backslashes += 1
        # The total length will be the actual length of the string minus 2 * nr_backslashes
        # this is because each backslash sequence contains 3 characters which should in fact be 1
        return len(string) - 2 * nr_backslashes


    # This method tries to find the position of a node with respect to the first node with a symbol table in it
    # The parent nr is a way of saying which parent we need to use, first we seek the parent then we go digging
    def get_position(self, parent_nr=0):
        # Seek the position of this statement in the statement sequence, we need this because we
        # need to find the file
        parent = self.parent
        child = self
        while parent_nr:
            # If the current parent has a symbol table then we need to decrease the parent nr by 1
            if isinstance(parent, has_symbol_table):
                parent_nr -= 1
            child = parent
            parent = parent.parent
        position = 0

        # make the current child the previous parent in order to find the correct child to seek for a position
        while not isinstance(parent, has_symbol_table):
            child = parent
            parent = parent.parent
            # # When the parent is a use function then do not use its symbol table and quit this function
            # if isinstance(parent, Function) and parent.function_type == "use":
            #     return None

        # Iterate over all the children of the statement sequence and check if the ast node is met
        # If it is met then this will be the final position at which the variable is declared
        for _child in parent:
            if _child == child:
                break
            position += 1
        return position

    def is_declaration(self):
        return self.declaration

    def get_scope_count(self):
        if isinstance(self, has_symbol_table):
            return self.scope_count
        if not self.parent:
            return -1
        else:
            return self.parent.get_scope_count()

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

    def optimize(self):
        # Using a function inside the class and not the traverse function because this might delete objects
        #  and deleting inside the element were traversing over is often not the best idea
        # Iterating over i to prevent working with copies
        for i in range(len(self.children)):
            self.children[i].optimize()

    # Returns the first symbol table it finds on the way to the top
    def get_symbol_table(self):
        # If we find that this node is a statement sequence then return its symboltable
        if isinstance(self, has_symbol_table):
            return self.symbol_table
        # Otherwise we go to the first parent with that has a symbol_table
        cur_parent = self.parent
        # We go up in the AST searching for the first symbol table
        while cur_parent and not isinstance(cur_parent, has_symbol_table):
            cur_parent = cur_parent.parent
        return cur_parent.symbol_table

    # Pre-order traverse with a given function
    def traverse(self, func):
        func(self)
        for child in self.children:
            child.traverse(func)

    # Post-order traverse with a given function
    def traverse_post(self, func):
        for child in self.children:
            child.traverse(func)
        func(self)

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

    def get_neutral(self) -> str:
        # 0.0 if float
        if self.children:
            return self.children[0].get_neutral()
        return "0"

    def get_llvm_print_type(self) -> str:
        # The only moment when this returns something else is with floats
        if self.children:
            return self.children[0].get_llvm_print_type()
        return None

    # Comment out a given string if required
    @staticmethod
    def comment_out(comments: str, comment_out: bool):
        if not comment_out:
            return comments
        comments = "\t; " + comments
        return comments + '\n'

    # The llvm template for loading a variable from storage
    def llvm_load_template(self):
        # Code for loading a variable (default is no loading required)
        return "\t{result} = load {type}, {type}* {var}\n"

    # Get the unique ID of this subtree
    def id(self):
        if not self._id:
            self._id = self.get_unique_id()
        return self._id


    # Get a unique temp variable
    @staticmethod
    def get_temp():
        return "%.t" + str(AST.get_unique_id())

    # Create a new label
    @staticmethod
    def label(name: str):
        return name + ":\n"


# Convert given ast into a dotfile and write it to filename
def dot(ast: AST, filename: str):
    output = "Digraph G { \n"

    # Add the symbol table tree
    ast.symbol_table.to_dot()
    output += SymbolTable.dot_output

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
    def __init__(self, scope_count):
        AST.__init__(self, "Statement Sequence")
        self.scope_count = scope_count
        self.symbol_table = SymbolTable(self.id())  # An empty symbol table

    # returns the dot representation of a statement sequence
    def __str__(self):
        return '{name}[label="{value} ({id})", fillcolor="{color}"] \n'.format(name=self.id(), value=self.value,
                                                                               id=self.id(), color=self.color)

    def comments(self, comment_out=True):
        return self.comment_out("Code Block", comment_out)

    def get_llvm_type(self):
        # A statement sequence has no type
        return None

    def optimize(self):
        # Iterating over i to prevent working with copies
        i = 0
        # Using a while loop because in range doesn't update every iteration
        while i < len(self.children):
            if isinstance(self[i], (Return, Break, Continue)):
                # Remove all code after a return, break or continue
                self.children = self.children[:i + 1]
                break
            self[i].optimize()
            i += 1


class If(AST):
    def __init__(self):
        AST.__init__(self, "if")

    def comments(self, comment_out=True):
        comment = "if " + self.children[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)

    def get_llvm_type(self):
        # An if statement has no type
        return None


class For(AST):
    def __init__(self, scope_count):
        AST.__init__(self, "for")
        self.scope_count = scope_count
        self.symbol_table = SymbolTable(self.id())

    def comments(self, comment_out=True):
        comment = "for " + self[0].comments()  # only add comments for the condition, the comments for the statement
        # sequence will be added when visiting their code
        return self.comment_out(comment, comment_out)


class While(AST):
    def __init__(self):
        AST.__init__(self, "while")
        # self.scope_count = scope_count
        # self.symbol_table = SymbolTable(self.id())

    def comments(self, comment_out=True):
        comment = "while " + self[0].comments()  # only add comments for the condition, the comments for the statement
        # sequence will be added when visiting their code
        return self.comment_out(comment, comment_out)



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
        self.declaration = True  # TODO: hoezo staat dit hier? Ik zou eerder houden aan de declaration in Variable

    def __str__(self):
        if self.declaration:
            return '{name}[label="Assign Declaration", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)
        return '{name}[label="Assign", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)

    def get_llvm_template(self):
        return "\tstore {type} {temp}, {type}* {location}\n"

    def collapse_comment(self, ast):
        self.comment = ast.children[0].node.collapse_comment(ast.children[0]) + self.value + \
                       ast.children[1].node.collapse_comment(ast.children[1])
        return self.comment


class Function(AST):
    def __init__(self, value="", return_type="void", function_type="use"):
        AST.contains_function = True
        AST.__init__(self, value, "#ff6486")
        self.return_type = return_type  # The type the return value must be
        self.function_type = function_type  # The use of the function, declaration/definition/using a function
        self.scope_count = 0  # Scope count does nothing
        self.symbol_table = SymbolTable(self.id())  # Function does have its own symbol table

    def __str__(self):
        return '{name}[label="Function ({id}): {type}: {return_type} {func_name}", fillcolor="{color}"] \n'.format(
            name=self.id(),
            id=self.id(),
            type=self.function_type,
            return_type=self.return_type,
            func_name=self.value,
            color=self.color)

    def get_type(self):
        return self.return_type

    def get_llvm_type(self) -> str:
        if self.return_type == "int":
            return 'i32'
        elif self.return_type == "bool":
            return 'i1'
        elif self.return_type == "float":
            return 'float'
        elif self.return_type == "char":
            return 'i8'
        elif self.return_type == "void":
            return 'void'

    def comments(self, comment_out: bool = True) -> str:
        # Add the arguments for a function in a string
        function_arguments = ""
        for child in self.children[0]:
            if len(function_arguments):
                # Add a separator to the arguments, because there was a previous argument
                function_arguments += ", "
            # Add the type of the variable
            function_arguments += child.get_type()
            # Add space between the type and the arguments variable name
            function_arguments += " "
            # Add the value of the child
            function_arguments += str(child.value)
        if isinstance(self.parent, Binary) and self.parent.children[0] == self:
            return "; {function_name}({function_arguments})".format(function_name=self.value,
                                                                    function_arguments=function_arguments)
        else:
            return "; {function_name}({function_arguments})\n".format(function_name=self.value,
                                                                      function_arguments=function_arguments)

    def get_llvm_template(self):
        # if we declare a function then we that we declare it
        if self.function_type == "declaration":
            return "declare {return_type} @{name}({arg_list})\n"
        elif self.function_type == "use":  # We call a function
            return "\tcall {return_type} @{name}({arg_list})\n"
        return "define {return_type} @{name}({arg_list})"

    def to_llvm_string(self, string) -> str:
        i = 0
        ret_string = str()
        while i < len(string):
            # If we find that the string is a \ then we need to check what translation of it will be in llvm
            if string[i] == "\\":
                if string[i + 1] == "n":  # endl
                    ret_string += "\\0A"
                elif string[i + 1] == "b":  # backspace
                    ret_string += "\\08"
                elif string[i + 1] == "e":  # escape character
                    ret_string += "\\1B"
                elif string[i + 1] == "a":  # alert beep
                    ret_string += "\\07"
                elif string[i + 1] == "f":  # Formfeed pagebreak
                    ret_string += "\\0C"
                elif string[i + 1] == "r":  # carriage return
                    ret_string += "\\0D"
                elif string[i + 1] == "t":  # horizontal tab
                    ret_string += "\\09"
                elif string[i + 1] == "v":  # Vertical tab
                    ret_string += "\\0B"
                elif string[i + 1] == "\\":  # backslash
                    ret_string += "\\5C"
                elif string[i + 1] == "\'":  # apostrophe
                    ret_string += "\\27"
                elif string[i + 1] == "\"":  # double quotation mark
                    ret_string += "\\22"
                elif string[i + 1] == "?":  # questionmark
                    ret_string += "\\3F"
                # In all other cases just take the last letter
                else:
                    ret_string += string[i + 1]
                # Because we checked 2 letters we need to go one letter further to get to the next letter
                i += 1
            # If we just find a character then we need to add the character instead of a hexadecimal value
            else:
                ret_string += string[i]
            # Go one letter further
            i += 1
        # A \00 needs to be added in order to mark the end of the string because every string is null terminated
        ret_string += "\\00"
        return ret_string

    # Gets the total amount of format tags in a printf string
    def get_format_count(self, format_string):
        format_count = 0
        for character in format_string:
            if character == '%':
                format_count += 1
        return format_count



class Arguments(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#ff6486")

    def __str__(self):
        return '{name}[label="Argument List", fillcolor="{color}"] \n'.format(
            name=self.id(),
            color=self.color)

    def get_type(self):
        return None

    def comments(self, comment_out: bool = True) -> str:
        return ""

    def get_llvm_template(self):
        return ""


class Include(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#000000")

    def __str__(self):
        return '{name}[label= <<font color="white">include stdio.h</font>>, fillcolor="{color}"] \n'.format(
            name=self.id(),
            color=self.color)

    def get_type(self):
        return None

    def comments(self, comment_out: bool = True) -> str:
        return ""

    def get_llvm_template(self):
        return ""


# Variable to indicate that these classes need a bool for branching instead of original value
BoolClasses = (If, For, While)
has_symbol_table = (StatementSequence, For, Function)  # , If, For, While)

# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Constant import *
from src.Node.Operate import *
from src.Node.Comments import *
from src.Node.ReservedType import *
