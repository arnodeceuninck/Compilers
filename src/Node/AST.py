"""
!
"""

from src.symbolTable import SymbolTable


class AST:
    _id = 0
    llvm_output = ""
    # symbol_table = SymbolTable() Removing the symbol table from the ast as a static variable -> found in the statement sequences
    print = False
    contains_function = False  # Check whether you have to manually add the int main()

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
                # We need to check if the variable is a global one or a local one
                # If the symbol table is global then we need to return a global variable form
                if self.get_symbol_table().is_global(self.value):
                    return "@" + self.value
                return "%" + self.value + "." + str(self.get_symbol_table().get_symbol_table_id(self.value))
            var = "%.t" + str(self.get_unique_id())
            self.llvm_load(var)  # Loads the variable in storage into the variable var
            return var
        elif isinstance(self, UDeref) and store:
            return self[0].variable(store)

        var = self.id()

        return "%.v" + str(var)

    # Get a unique temp variable
    @staticmethod
    def get_temp():
        return "%.t" + str(AST.get_unique_id())

    # Jump to a given label
    @staticmethod
    def goto(label: str):
        AST.llvm_output += "br label %" + label + "\n"

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

    def llvm_code(self):
        AST.llvm_output += self.comments()
        for child in self.children:
            child.llvm_code()
        AST.llvm_output += '\n'

    def optimize(self):
        # Iterating over i to prevent working with copies
        i = 0
        # Using a while loop because in range doesn't update every iteration
        while i < len(self.children):
            if isinstance(self[i], Return):
                # Remove all code after a return
                self.children = self.children[:len(self.children) - i + 1]  # TODO: Check whether +1 required
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

    def llvm_code(self):
        # TODO: fix else
        AST.llvm_output += self.comments()

        condition = self.children[0]
        condition.llvm_code()

        # Make both labels unique
        label_true = "iftrue" + str(self.id())
        label_false = "iffalse" + str(self.id())
        code = "br {type} {var}, label %{label_true}, label %{label_false}\n"
        code = code.format(type="i1",
                           var=condition.variable(),
                           label_true=label_true,
                           label_false=label_false)
        AST.llvm_output += code

        # Make a unique label for the end
        label_end = "end" + str(self.id())
        if_statement_sequence = self.children[1]
        AST.llvm_output += self.label(label_true) + "\n"
        if_statement_sequence.llvm_code()
        self.goto(label_end)

        AST.llvm_output += self.label(label_false) + "\n"
        # If we have 3 children and an else statement, then generate the LLVM code for it
        if len(self.children) == 3:
            else_statement_sequence = self.children[2]
            else_statement_sequence.llvm_code()
        self.goto(label_end)
        AST.llvm_output += self.label(label_end) + '\n'


# TODO
class For(AST):
    def __init__(self, scope_count):
        AST.__init__(self, "for")
        self.scope_count = scope_count
        self.symbol_table = SymbolTable(self.id())

    def comments(self, comment_out=True):
        comment = "for " + self[0].comments()  # only add comments for the condition, the comments for the statement
        # sequence will be added when visiting their code
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # Initialize the for loop
        initialize = self.children[0]
        initialize.llvm_code()

        # Make for loop label unique
        label_for = "loop" + str(self.id())
        # This is to avoid a bug in llvm, just dont delete!
        self.goto(label_for)

        # Make while loop label unique for just after the condition
        label_after_check = "afterCheck" + str(self.id())
        # Create the label
        AST.llvm_output += self.label(label_for) + "\n"

        condition = self.children[1]
        condition.llvm_code()

        # Make a unique label for the end
        label_end = "end" + str(self.id())
        # Check if we can go further with the loop
        code = "br {type} {var}, label %{label_while}, label %{label_end}\n"
        code = code.format(type="i1",
                           var=condition.variable(),
                           label_while=label_after_check,
                           label_end=label_end)
        AST.llvm_output += code
        # Label necessary after the check
        AST.llvm_output += self.label(label_after_check) + "\n"

        statement_sequence = self.children[3]
        statement_sequence.llvm_code()

        # Calculate the next step
        iterate = self.children[2]
        iterate.llvm_code()

        # Loop back to the beginning
        self.goto(label_for)
        # Make the end of the loop
        AST.llvm_output += self.label(label_end) + "\n"


class While(AST):
    def __init__(self):
        AST.__init__(self, "while")

    def comments(self, comment_out=True):
        comment = "while " + self[0].comments()  # only add comments for the condition, the comments for the statement
        # sequence will be added when visiting their code
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # Make while loop label unique
        label_while = "loop" + str(self.id())
        # This is to avoid a bug in llvm, just dont delete!
        self.goto(label_while)

        # Make while loop label unique for just after the check condition
        label_after_check = "afterCheck" + str(self.id())
        # Create the label
        AST.llvm_output += self.label(label_while) + "\n"

        condition = self.children[0]
        condition.llvm_code()

        # Make a unique label for the end
        label_end = "end" + str(self.id())
        # Check if we can go further with the loop
        code = "br {type} {var}, label %{label_while}, label %{label_end}\n"
        code = code.format(type="i1",
                           var=condition.variable(),
                           label_while=label_after_check,
                           label_end=label_end)
        AST.llvm_output += code
        # Label necessary after the check
        AST.llvm_output += self.label(label_after_check) + "\n"

        statement_sequence = self.children[1]

        statement_sequence.llvm_code()
        # Loop back to the beginning
        self.goto(label_while)
        # Make the end of the loop
        AST.llvm_output += self.label(label_end) + "\n"


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

        # If the variable is not in the global scope then we need to make a variable
        # And check if the corresponding item has already been defined in llvm
        if not self.get_symbol_table().is_global(self[0].value) and not \
                self.get_symbol_table().get_symbol_table(self[0].value)[self[0].value].llvm_defined:
            create_var = "{variable} = alloca {llvm_type}, align {align}\n".format(
                variable=self[0].variable(store=True),
                llvm_type=self[0].get_llvm_type(),
                align=self[0].get_align())
            output += create_var
            # The variable has been defined in llvm, so no more generating hereafter
            self.get_symbol_table().get_symbol_table(self[0].value)[self[0].value].llvm_defined = True
        code = self.get_llvm_template()
        code = code.format(type=self[0].get_llvm_type(), temp=self[1].variable(store=True),
                           location=self[0].variable(store=True))

        output += code

        AST.llvm_output += output


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
            function_arguments += child.value

        return "; {function_name}({function_arguments})\n".format(function_name=self.value,
                                                                  function_arguments=function_arguments)

    def get_llvm_template(self):
        return "define {return_type} @{name}({arg_list}) #0"

    # The llvm code needs to be generated a special way and not in the main function
    # TODO: Duplicate functions are possible so naming scheme needs to change
    # TODO: Functions declarations/use need to point to the definition in order to call the correct function
    # TODO: Forward declaring
    def llvm_code(self):
        AST.llvm_output += self.comments()

        # Add the arguments for a function in a string
        # TODO: Check llvm arguments structure
        function_arguments = ""
        for child in self.children[0]:
            if len(function_arguments):
                # Add a separator to the arguments, because there was a previous argument
                function_arguments += ", "
            # Add the type of the variable
            function_arguments += child.get_llvm_type()

        initialization_line = self.get_llvm_template()
        initialization_line = initialization_line.format(return_type="i32", name=self.value,
                                                         arg_list=function_arguments)
        AST.llvm_output += initialization_line

        AST.llvm_output += " {\n"

        # First get all arguments
        if len(self[0].children):
            AST.llvm_output += "; fetching all arguments\n"
        for i in range(len(self[0].children)):
            code = "{variable} = alloca {type}, align {align}\n"
            code += "store {type} %{arg_nr}, {type}* {variable}\n"
            code = code.format(
                variable=self[0][i].variable(store=True),
                type=self[0][i].get_llvm_type(),
                align=self[0][i].get_align(),
                arg_nr=str(i))

            AST.llvm_output += code

        for child in self.children:
            child.llvm_code()
        AST.llvm_output += "}\n"


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

    def llvm_code(self):
        AST.llvm_output += self.comments()


# Variable to indicate that these classes need a bool for branching instead of original value
BoolClasses = (If, For, While)
has_symbol_table = (StatementSequence, For, Function)

# Use these imports to make these classes appear here
from src.Node.Variable import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.constant import *
from src.Node.Operate import *
from src.Node.Comments import *
from src.Node.ReservedType import *
