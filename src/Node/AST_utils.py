from gen import cParser, cLexer
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from src.ErrorListener import RerefError, CompilerError, ConstError, IncompatibleTypesError, CustomErrorListener, \
    SyntaxCompilerError, ReservedVariableOutOfScope
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
    # # Checks whether the ast is a function, if it is then we need to check if it defines a function
    # # If the function does not define anything (it is used or declared), then there is no symbol table to be linked
    # if isinstance(ast, Function):
    #     if ast.function_type == "declaration" or ast.function_type == "use":
    #         return

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
        # Check if the parent of the parent is a function, if it is then check if it conflicts with one of the passed variables
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
            # When the parent is a use function then do not use its symbol table and quit this function
            if isinstance(parent, Function) and parent.function_type == "use":
                return

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
        # elif type_lvalue == "float" and type_rvalue == "int":
        #     pass
        else:
            raise IncompatibleTypesError(type_lvalue, type_rvalue)


def match_function(function1: AST, function2: AST):
    # If one of the 2 ast trees isn't a function then do not proceed with matching
    if not isinstance(function1, Function) or not isinstance(function2, Function):
        return False
    elif function1.function_type == "use":  # If the type of the 1st function is use then do not proceed
        return False
    # Check if the names of the function match
    # If they do not match then return
    if function1.value != function2.value:
        return False
    # Check if both argument lists match
    arg_list1 = function1.children[0]
    arg_list2 = function2.children[0]
    # So we need to check if their lengths are the same if not return
    if len(arg_list1.children) != len(arg_list2.children):
        return False
    # Go over all the arguments and check if their types match
    for i in range(len(arg_list1.children)):
        # If their types do not match then return
        if arg_list1[i].get_type() != arg_list2[i].get_type():
            return False
    # The functions match!
    return True


# Will link the function use to its declaration to get the right type
def link_function(ast):
    # If the ast isn't a function then do nothing
    if not isinstance(ast, Function):
        return
    elif ast.function_type != "use":  # If the function is not a use then also return
        return

    # Begin with trying to link the function
    # Find the first statement sequence and search for a compatible declaration there, before this function
    prev_ast = ast
    cur_ast = ast.parent
    while True:
        while not isinstance(cur_ast, StatementSequence) and cur_ast:
            prev_ast = cur_ast
            cur_ast = cur_ast.parent
        if not cur_ast:
            break
        # Iterate over the children of the statement sequence
        for child in cur_ast.children:
            # If we surpass the child where we came from then continue
            if child == prev_ast:
                continue
            elif match_function(child, ast):  # This will try to match the two functions based on the arguments
                # Both functions match so we can give the return type of the found function to the
                # return type of the use function
                ast.return_type = child.return_type
                # We have linked the functions so we can return
                return
        # Go to the parents of the AST to search further
        prev_ast = cur_ast
        cur_ast = cur_ast.parent


def checkReserved(ast):
    # If the current instance is not a return break or continue then do not proceed with checking
    if not isinstance(ast, (Return, Break, Continue)):
        return
    # If the reserved type is used in an expression then also raise an error
    if not isinstance(ast.parent, StatementSequence):
        raise ReservedVariableOutOfScope(ast.value)

    cur_parent = ast.parent
    while cur_parent:
        # If the reserved type is of type return and we find ourselves in a function then return
        if isinstance(ast, Return) and isinstance(cur_parent, Function):
            return
        # If the reserved type is a continue or a break and we find ourselves in a function then raise an error
        elif isinstance(ast, (Continue, Break)) and isinstance(cur_parent, Function):
            raise ReservedVariableOutOfScope(ast.value)
        # If the reserved type is a continue or a break and we find ourselves in a for or while loop then return
        elif isinstance(ast, (Continue, Break)) and isinstance(cur_parent, (For, While)):
            return
        cur_parent = cur_parent.parent
    raise ReservedVariableOutOfScope(ast.value)


# return an ast tree from an input file
def compile(input_file: str, catch_error=True):
    input_stream = FileStream(input_file)
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    parser.addErrorListener(CustomErrorListener())

    if catch_error:
        try:
            tree = parser.start_rule()
            return make_ast(tree)
        except CompilerError as e:
            print(str(e))
            return None
    else:
        tree = parser.start_rule()
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
    # Convert Variables into their right type based on the symbol table
    communismForLife.traverse(convertVar)
    # Gives all the function uses correct return types
    communismForLife.traverse(link_function)
    communismForLife.traverse(checkAssigns)  # Check right type assigns, const assigns ...
    communismForLife.traverse(checkReserved)  # Checks if the reserved variables are used in the right scope
    # TODO: check if functions do end with a return when not void OPTIONAL!!!
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
