from gen import cParser, cLexer
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from src.ErrorListener import RerefError, CompilerError, ConstError, IncompatibleTypesError, CustomErrorListener, \
    SyntaxCompilerError, ReservedVariableOutOfScope, VariableRedeclarationError, ExpressionOutOfScope, \
    FunctionRedeclarationError, FunctionUndefinedError, DerefError, ReturnValueError, FunctionWrongDefinedError, \
    FunctionDefinitionOutOfScope, FunctionRedefinitionError, MainNotFoundError, ArrayIndexError, NoArrayError, \
    VariableRedefinitionError
from src.Node.AST import Function, has_symbol_table, Include
from src.CustomListener import CustomListener
from src.Node.Variable import *
from src.Node.Unary import *
from src.Node.Compare import *
from src.Node.Constant import *
from src.Node.Operate import *
from src.Node.Comments import *
from src.Node.ReservedType import *
from src.Dot.dot import dot


def connect_symbol_table(ast):
    # If we know that the symbol table is at global level then we do not need to connect it to any table
    # Or if the ast node is not a statement sequence then we do not need to search for a parent
    if not ast.parent or not isinstance(ast, has_symbol_table):
        return

    # The supposedly statement sequence which we need to connect the current symbol table with
    parent = ast.parent
    # Search the nearest parent which has a statement sequence
    while not isinstance(parent, has_symbol_table):
        parent = parent.parent

    # Set the parent of the symbol table to the parent just found
    ast.symbol_table.parent = parent.symbol_table
    # Add a child to this parent
    parent.symbol_table.children.append(ast.symbol_table)


# An error checking functions to check whether all symbols are already in the symbol table
# (or insert them when declaring)
def assignment(ast):
    # Return if we do not encounter a variable or an assign
    if not isinstance(ast, Variable) and not isinstance(ast, Assign):
        return

    # Check whether any other symbol is already in the symbol table
    if (not ast.is_declaration() and isinstance(ast, Variable) and not isinstance(ast.parent, Assign)) or \
            (ast.is_declaration() and isinstance(ast, Variable) and isinstance(ast.parent, Assign)):
        # Fetch the symbol table of the ast node
        symbol_table = ast.get_symbol_table()
        # We need to get the position of the variable as a child of the symbol_table node which is somewhere a parent
        var_position = ast.get_position()
        symbol_table_position = symbol_table[ast.value].position
        parent_nr = 1
        # We iterate over all the symbol tables and check if the item is already in the symbol table or not
        # we do this by checking if the position of the variable is before the declaration. If that is the case
        # Then we need to check the parent of the symbol table and so on so forth
        while var_position < symbol_table_position:
            var_position = ast.get_position(parent_nr)
            # Get the previous symbol table and get its parent to seek there
            symbol_table = symbol_table.parent
            # If we do not ge the right symbol table then we need to look for the parent
            if symbol_table != symbol_table.get_symbol_table(ast.value):
                # Assure that we get the next symbol table
                var_position = -1
                parent_nr += 1
                continue
            symbol_table_position = symbol_table[ast.value].position
            # Increase the parent_nr so it will seek 1 parent deeper
            parent_nr += 1
        # return not required here, but otherwise pycharm thinks the statement is useless
        return symbol_table[ast.value]  # Raises an error if not yet declared

    # Check if the child is a declaration
    is_declaration = False
    if ast.children:
        if ast[0].is_declaration():
            is_declaration = True

    # Add symbol to symbol table
    if isinstance(ast, Assign) and (ast.is_declaration() or is_declaration):
        # TODO improve type without constant and ptr
        location = ast.children[0].value
        type = ast.children[0]
        # This variable is needed to indicate when we have declared the variable
        # If we have assignments and use the variable we can then check the parent instead
        position = ast.get_position()

        # When the left child is a * then we need to look at it's child which is the real location
        if location == "*":
            location = ast.children[0][0].value
            type = ast.children[0][0]

        # The supposedly statement sequence in which we need to put the variable
        parent = ast.parent
        # Insert the variable into the nearest parent ast symbol table that is a statement sequence
        # This is because they define scopes
        while not isinstance(parent, has_symbol_table):
            parent = parent.parent

        # Check if the parent of the parent is a function,
        # if it is then check if it conflicts with one of the passed variables
        if isinstance(parent.parent, Function):
            if parent.parent.function_type == 'use':
                return
            # Store the symbol table of the function
            function_symbol_table = parent.parent.symbol_table
            # If the value is in the symbol table of the function then it we will get true otherwise false
            double_declared = function_symbol_table.in_this(ast[0].value)

            # We raise an error because the variable is double declared
            if double_declared:
                raise VariableRedeclarationError(location)

        parent.symbol_table.insert(location, type, position)

    # Last minute fix before the evaluation
    # This checks if the variable is declared, like int x; without a definition
    # And then adds it to the syntax tree
    if isinstance(ast, Variable) and ast.declaration:  # ast.parent and not isinstance(ast.parent,
        #       (Assign, Print, If, Unary, Binary, Return)):
        location = ast.value
        type = ast
        symbol_table = ast.get_symbol_table()
        # This variable is needed to indicate when we have declared the variable
        # If we have assignments and use the variable we can then check the parent instead
        position = ast.get_position()
        if position is None:
            return

        # If we have an array declaration then we need to take the index position to the array size
        if type.array:
            type.array_size = type.array_number

        symbol_table.insert(location, type, position)


# Converts all variables into the right type.
# e.g. int x = y, y will be a variable from the listener, but must be the right type
def convertVar(ast):
    if not isinstance(ast, Variable):
        return
    if isinstance(ast, Print):
        return
    element = ast.get_symbol_table()[ast.value].type

    array_size = element.array_number
    type = element.get_type()
    while type[len(type) - 1] == "*":
        type = type[:len(type) - 1]
    if type == 'int':
        ast_new = VInt(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast_new.array = element.array
        ast_new.array_number = ast.array_number
        ast_new.array_indexed = ast.array_indexed
        ast_new.array_size = element.array_number
        if isinstance(element.parent, ArrayIndex):
            ast_new.array_number = element.parent.index
        ast_new.declaration = ast.declaration
        ast.parent.replace_child(ast, ast_new)
    elif type == 'float':
        ast_new = VFloat(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast_new.array = element.array
        ast_new.array_number = ast.array_number
        ast_new.array_size = element.array_number
        ast_new.array_indexed = ast.array_indexed
        ast_new.declaration = ast.declaration
        ast.parent.replace_child(ast, ast_new)
    elif type == 'char':
        ast_new = VChar(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast_new.array = element.array
        ast_new.array_indexed = ast.array_indexed
        ast_new.array_number = ast.array_number
        ast_new.array_size = element.array_number
        ast_new.declaration = ast.declaration
        ast.parent.replace_child(ast, ast_new)
    else:
        print("[WARNING] Unsupported variable type")


def check_supported_operations(ast):
    if isinstance(ast, (Assign, ArrayIndex, UReref, UDeref)):
        return  # Already checked in Check Assigns
    if isinstance(ast, Unary):
        supported_types = ["int", "float", "char"]
        if ast[0].get_type() not in supported_types:
            raise UnknownOperationError(ast.value, ast[0].get_type())
    elif isinstance(ast, Binary):
        supported_types = [("int", "int"), ("float", "float"), ("char", "char")]
        if (ast[0].get_type(), ast[1].get_type()) not in supported_types:
            raise UnknownOperationError(ast.value, ast[0].get_type(), ast[1].get_type())


# A function to check whether you're always assigning to the right type and not to a const value
def checkAssigns(ast):
    # Check for const assigns
    # If the child is of the type * then we need to take the child of UReref
    if isinstance(ast, Assign) and isinstance(ast[0], UReref):
        ast = ast[0]
    # On assignments that are declarations, but the leftmost child is a const variable
    if isinstance(ast, Assign) and ast[0].const and not ast.declaration:
        raise ConstError(ast[0].value)
    if isinstance(ast, Assign):
        type_lvalue = ast[0].get_type()
        type_rvalue = ast[1].get_type()
        if type_lvalue == type_rvalue:
            pass
        elif type_lvalue == "char*" and type_rvalue == "char":
            pass
        # elif type_lvalue == "float" and type_rvalue == "int":
        #     pass
        else:
            raise IncompatibleTypesError(type_lvalue, type_rvalue)


def match_function(function1: AST, function2: AST):
    # If one of the 2 ast trees isn't a function then do not proceed with matching
    if not isinstance(function1, Function) or not isinstance(function2, Function):
        return False
    # Check if the names of the function match
    # If they do not match then return
    if function1.value != function2.value:
        return False
    # Check the return types of both functions
    if function1.return_type != function2.return_type:
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


def soft_match_function(function1: AST, function2: AST):
    # If one of the 2 ast trees isn't a function then do not proceed with matching
    if not isinstance(function1, Function) or not isinstance(function2, Function):
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


# We check if the return type of a return matches the one of the function definition return value
def return_check(ast):
    # Checks for a return
    if not isinstance(ast, Return):
        return

    return_type = ast.get_type()
    cur_parent = ast.parent
    # Climb up the syntax tree in order to get to the function we have a function
    while not isinstance(cur_parent, Function):
        cur_parent = cur_parent.parent

    # Store the functions return type
    function_return_type = cur_parent.return_type
    # If the two values do not match then raise an error
    if return_type != function_return_type:
        raise ReturnValueError(return_type, function_return_type)


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
        # The next break means that we need to stop with iterating over the children
        # Because we surpassed from where we came from
        next_break = False
        # Iterate over the children of the statement sequence
        for child in cur_ast.children:
            # Break now, previous loop asked for it
            if next_break:
                break
            # If we surpass the child where we came from then the next child we need to break
            if child == prev_ast:
                next_break = True
            # This will try to match the two functions based on the arguments
            # and the function name
            if soft_match_function(child, ast):
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


# The goal of this function is trying to fix add a return to the end of every function so
# that llvm can correctly generate functions and do it without an error
def adding_return(ast):
    # If the ast parent isn't a function and the current ast is not a statement sequence then do nothing
    if not isinstance(ast, StatementSequence) or not isinstance(ast.parent, Function):
        return
    elif ast.parent.function_type != "definition":  # If the function type is not a definition then return
        return

    # Take the last child and check if it is a return
    try:
        last_child = ast.children[len(ast.children) - 1]
        if isinstance(last_child, Return):
            return
    except IndexError:
        # Empty main
        pass

    # If the last child is not a return then we need to add the return
    # First we need to construct the return node
    return_node = Return()
    # Then we put create the return value if there is any
    if ast.parent.return_type != "void":
        return_value_node = Constant().create_constant(ast.parent.return_type)
        # Link the two nodes together to form a return node
        return_node.children.append(return_value_node)
        return_value_node.parent = return_node
    # Link the function statement together
    return_node.parent = ast
    ast.children.append(return_node)


# Checks the ast for variables
def has_variable(ast):
    has_var = isinstance(ast, (Variable, Function))
    for child in ast.children:
        has_var += has_variable(child)
    return has_var


def has_been_included_stdio(ast):
    for child in ast.children:
        if isinstance(child, Include):
            return True
    return False


def check_global_scope(ast):
    # If the ast is not the global scope then just return
    if ast.parent:
        return
    # Iterate over every child to check if it belongs to the global scope
    for child in ast.children:
        # If the code is a function then check if it is not a use, otherwise just continue
        if isinstance(child, Function):
            if child.function_type == "use":
                if child.value == "printf":
                    continue
                raise ExpressionOutOfScope(child.value)
        # When you encounter an assign things get more complicated. The rhs of an assign can only contain
        # constants and no variables
        elif isinstance(child, Assign):
            # Check if the rhs has a variable in the expression
            if has_variable(child[1]):
                raise ExpressionOutOfScope(child.value)
        else:  # The child that doesnt belong here should raise an error
            raise ExpressionOutOfScope(child.value)


# This function will store all the declared and defined functions in order to check for the use functions
# if no declared or defined function is found for the use function then there needs to be an error
# if at the end the list does not only exist of defined functions then there is also an error
def check_function(ast):
    # We need to check if the ast is a function otherwise it will be useless to proceed in this function
    if not isinstance(ast, Function):
        return
    # Next we need to check of which type the function is depending on its use we execute different
    # actions
    function_type = ast.function_type
    if function_type == "use":
        # If stdio is included then do not worry about the implementation of printf
        if (ast.value == "printf" or ast.value == "scanf") and AST.stdio:
            return
        matched_function = False
        # Iterate over the functions to check if they are defined
        for function in AST.functions:
            # Once we found a match we do not throw an error
            if soft_match_function(function, ast) and not matched_function:
                matched_function = True
        # If the function is not defined yet the throw an undefined error
        if not matched_function:
            raise FunctionUndefinedError(ast.value)
    elif function_type == "definition":
        # We need to check if the Function definition only has 1 parent and is defined in the global scope
        if ast.parent.parent:
            raise FunctionDefinitionOutOfScope(ast.value)
        # If stdio is included then we need to throw an error because we try to redefine the stdio
        if (ast.value == "printf" or ast.value == "scanf") and AST.stdio:
            raise FunctionRedeclarationError(ast.value)
        # We need to find put this defined function at the back of the AST functions if it  not found in the
        # array of functions
        in_array = False  # Variable for indicating if the function is in the array
        for function in AST.functions:
            function_matched = match_function(function, ast)
            # If the functions did not match while the names are the same then raise an error
            if not function_matched and function.value == ast.value:
                raise FunctionWrongDefinedError(ast.value)
            elif function_matched:  # If the functions matched then we will put it in the array
                # but first check if the function is not already defined
                # We will achieve this by checking if the function that is matched against is not a defined function
                # if it is then raise an error
                if function.function_type == "definition":
                    raise FunctionRedefinitionError(function.value)
                in_array = True
                break
        # We did not find the function in the array so append it to the other functions
        if not in_array:
            AST.functions.append(ast)
    elif function_type == "declaration":
        # If stdio is included then we need to throw an error because we try to redeclare the stdio
        if (ast.value == "printf" or ast.value == "scanf") and AST.stdio:
            raise FunctionRedeclarationError(ast.value)
        # We need to find put this declared function at the back of the AST functions if it  not found in the
        # array of functions
        in_array = False  # Variable for indicating if the function is in the array
        for function in AST.functions:
            function_matched = match_function(function, ast)
            # If the functions did not match while the names are the same then raise an error
            if not function_matched and function.value == ast.value:
                raise FunctionRedeclarationError(ast.value)
            elif function_matched:  # If the functions matched then we will put it in the array
                in_array = True
                break
        # We did not find the function in the array so append it to the other functions
        if not in_array:
            AST.functions.append(ast)


def check_only_dereference_lvalues(ast: AST):
    if not isinstance(ast, UDeref):
        return
    child = ast[0]
    # TODO: Make this work for arrays
    if not isinstance(child, Variable):
        raise DerefError()


def check_arrays(ast: AST):
    if isinstance(ast, ArrayIndex):
        if not ast[1].get_type() == "int":
            raise ArrayIndexError()

        if not ast[0].array:
            raise NoArrayError()


# Checks if there is a main defined in the AST
def check_main(ast: AST):
    if not isinstance(ast, Function):
        return
    if ast.function_type == "definition":
        if ast.value == "main":
            if ast.return_type == "int":
                AST.main = True  # Main has been defined
            else:  # Main has the wrong return type
                raise ReturnValueError(ast.value, "int")


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
    customListener = CustomListener()
    walker = ParseTreeWalker()
    walker.walk(customListener, tree)
    javaForLife = customListener.trees[0]
    # Makes a tree of the symbol tables
    javaForLife.traverse(connect_symbol_table)
    # The two methods of below should be combined in order to make it one pass and apply error checking
    # Create symbol table
    javaForLife.traverse(assignment)  # Symbol table checks
    # Convert Variables into their right type based on the symbol table
    javaForLife.traverse(convertVar)
    dot(javaForLife, "output/debug.dot")
    # Gives all the function uses correct return types
    javaForLife.traverse(link_function)
    javaForLife.traverse(checkAssigns)  # Check right type assigns, const assigns ...
    javaForLife.traverse(checkReserved)  # Checks if the reserved variables are used in the right scope
    javaForLife.traverse(adding_return)  # Adds a return to every function that has none on the end
    javaForLife.traverse(check_only_dereference_lvalues)
    javaForLife.traverse(check_main)  # Checks if there is a main defined
    javaForLife.traverse(return_check)
    javaForLife.traverse(check_arrays)
    javaForLife.traverse(check_supported_operations)
    AST.stdio = has_been_included_stdio(javaForLife)  # Adds if the stdio is included
    javaForLife.traverse(check_function)  # Checks if all the functions are defined
    if not AST.main:
        raise MainNotFoundError()
    # TODO: check if functions do end with a return when not void OPTIONAL!!!
    if optimize:
        javaForLife.optimize()
    return javaForLife
