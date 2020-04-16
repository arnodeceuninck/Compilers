from gen import cParser, cLexer
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from src.ErrorListener import RerefError, CompilerError, ConstError, IncompatibleTypesError, CustomErrorListener
from src.Node.AST import *
from src.customListener import customListener
from src.Node.Variable import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.constant import *
from src.Node.Operate import *
from src.Node.Comments import *
from src.Node.ReservedType import *

def connect_symbol_table(ast):
    # If we know that the symbol table is at global level then we do not need to connect it to any table
    # Or if the ast node is not a statement sequence then we do not need to search for a parent
    if not ast.parent or not isinstance(ast, has_symbol_table):
        return
    # Checks wheter the ast is a function, if it is then we need to check if it defines a function
    # If the function does not define anything (it is used or declared), then there is no symbol table to be linked
    if isinstance(ast, Function):
        if ast.function_type == "declaration" or ast.function_type == "use":
            return

    # The supposedly statement sequence which we need to connect the current symbol table with
    parent = ast.parent
    # Search the nearest parent which has a statement sequence
    while not isinstance(parent, has_symbol_table):
        parent = parent.parent

    # Checks wheter the parent is a function, if it is then we need to check if it defines a function
    # If the function does not define anything (it is used or declared), then there is no symbol table to be linked
    if isinstance(parent, Function):
        if parent.function_type == "declaration" or parent.function_type == "use":
            return
    # Set the parent of the symbol table to the parent just found
    ast.symbol_table.parent = parent.symbol_table
    # Add a child to this parent
    parent.symbol_table.children.append(ast.symbol_table)


# An error checking functions to check whether all symbols are already in the symbol table
# (or insert them when declaring)
def assignment(ast):
    # Check whether any other symbol is already in the symbol table
    if isinstance(ast, Variable) and ast.parent and isinstance(ast.parent, Assign):
        # The supposedly statement sequence in which we need to put the variable
        parent = ast.parent
        # Insert the variable into the nearest parent ast symbol table that is a statement sequence
        # This is because they define scopes
        while not isinstance(parent, has_symbol_table):
            parent = parent.parent
        # Check if the parent is a function, if it is then check if it conflicts with one of the passed variables
        if isinstance(parent.parent, Function):
            pass
        # return not required here, but otherwise pycharm thinks the statement is useless
        return parent.symbol_table[ast.value]  # Raises an error if not yet declared

    # Add symbol to symbol table
    if ast.value == "=" and ast.declaration:
        # improve type without constant and ptr
        location = ast.children[0].value
        type = ast.children[0]
        # The supposedly statement sequence in which we need to put the variable
        parent = ast.parent
        # Insert the variable into the nearest parent ast symbol table that is a statement sequence
        # This is because they define scopes
        while not isinstance(parent, has_symbol_table):
            parent = parent.parent

        parent.symbol_table.insert(location, type)

    # Last minute fix before the evaluation
    # (already forgot what it does)
    if isinstance(ast, Variable) and ast.parent and not isinstance(ast.parent,
                                                                   (Assign, Print, If, Unary, Binary, Return)):
        location = ast.value
        type = ast
        # The supposedly statement sequence in which we need to put the variable
        parent = ast.parent
        # Insert the variable into the nearest parent ast symbol table that is a statement sequence
        # This is because they define scopes
        while not isinstance(parent, has_symbol_table):
            parent = parent.parent

        parent.symbol_table.insert(location, type)


# Converts all variables into the right type.
# e.g. int x = y, y will be a variable from the listener, but must be the right type
def convertVar(ast):
    if not isinstance(ast, Variable):
        return
    if isinstance(ast, Print):
        return
    element = ast.get_symbol_table()[ast.value].type
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
def make_ast(tree, optimize: bool = True):
    communismRules = customListener()
    walker = ParseTreeWalker()
    walker.walk(communismRules, tree)
    communismForLife = communismRules.trees[0]
    # Makes a tree of the symbol tables
    communismForLife.traverse(connect_symbol_table)
    # The two methods of below should be combined in order to make it one pass and apply error checking
    # Create symbol table
    communismForLife.traverse(assignment)  # Symbol table checks
    # Apply symbol table to all the variables
    communismForLife.traverse(convertVar)  # Qua de la fuck does this? -> Convert Variables into their right type
    communismForLife.traverse(checkAssigns)  # Check right type assigns, const assigns ...
    if optimize:
        communismForLife.optimize()
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
    if len(symbol_table) > 0:
        AST.llvm_output += "\n"
    if not AST.contains_function:
        AST.llvm_output += "define i32 @main() {\n\n"

    ast.llvm_code()

    if not AST.contains_function:
        AST.llvm_output += "\n"
        AST.llvm_output += "ret i32 0\n"
        AST.llvm_output += "}\n\n"

    # If we need to print then create the print function
    if AST.print:
        print = "@.strc = private unnamed_addr constant [3 x i8] c\"%c\\00\", align 1\n"
        print += "@.strd = private unnamed_addr constant [3 x i8] c\"%d\\00\", align 1\n"
        print += "@.strf = private unnamed_addr constant [3 x i8] c\"%f\\00\", align 1\n"
        print += "declare i32 @printf(i8*, ...)\n"
        AST.llvm_output += print

    # Write output to the outputfile
    outputFile = open(filename, "w")
    outputFile.write(AST.llvm_output)
    outputFile.close()
