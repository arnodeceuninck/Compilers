from src.LLVMAst.LLVMAst import LLVMOperationSequence, LLVMCode, LLVMArgumentList, LLVMAllocate, LLVMLoad, \
    LLVMFunction, LLVMVariable, LLVMConst, LLVMConstFloat, LLVMConstInt, LLVMAssignment, LLVMOperation, \
    LLVMStore
from src.Node.AST_utils import *
from src.symbolTable import *

has_symbol_table = (LLVMCode, LLVMOperationSequence, LLVMFunction)


# This will connect the symbol tables on itself
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
    # Return if we do not encounter a variable, argument list, allocate or load
    if not isinstance(ast, (LLVMArgumentList, LLVMAllocate, LLVMLoad, LLVMVariable)):
        return

    # Add symbol to symbol table
    # 1. if the current ast node is an argument list we need to add variables with 0-... to the symbol table of the function
    if isinstance(ast, LLVMArgumentList):
        # Iterate over all the children to add all the arguments to the function scope
        for i in range(len(ast.children)):
            location = str(i)
            type = ast.children[i].type
            ast.parent.symbol_table.insert(location, type)

    # 2. If the ast is an allocate, then we know that the right child of the parent will contain the type and its
    # left child the variable
    elif isinstance(ast, LLVMAllocate):
        variable = ast.parent[0]
        location = variable.value
        type = ast.type

        try:
            ast.parent.parent.symbol_table.insert(location, type)
        except:
            pass

    # 3. If the ast is a load then we know that we have the child as variable and the current node has the type
    elif isinstance(ast, LLVMLoad):
        variable = ast.children[0]
        location = variable.value
        type = ast.type
        try:
            ast.parent.parent.symbol_table.insert(location, type)
        except:
            pass

    # 4. If the parent is an assign and its right child is an operation then we need to define
    # the type of the left child
    elif isinstance(ast, LLVMVariable) and isinstance(ast.parent, LLVMAssignment) and isinstance(ast.parent[1],
                                                                                                 LLVMOperation):
        defined_var = ast.parent[1][0]
        symbol_table = ast.parent.parent.symbol_table
        location = ast.value
        type = None
        # If we find that this so called variable is a constant then we need to seek the type
        if isinstance(defined_var, LLVMConst):
            if isinstance(defined_var, LLVMConstFloat):
                type = "float"
            elif isinstance(defined_var, LLVMConstInt):
                type = "int"
        # Else if it is a variable then we need to get the type of the LLVMVariable from the table
        elif isinstance(defined_var, LLVMVariable):
            # Seek the variable in the symbol table
            symbol_table_element = symbol_table[defined_var.value]
            # Retrieve its type
            type = symbol_table_element.type

        # In order to avoid redeclaration errors of variables we put a try catch block arround this piece of code
        try:
            symbol_table.insert(location, type)
        except:
            pass

    # 5. if the operation is a store then we need to check if the current variable is on the
    # left handside or the righthandside in order to determine if we need to define it or not
    elif isinstance(ast, LLVMVariable) and isinstance(ast.parent, LLVMStore) and ast.parent[0] != ast:
        defined_var = ast.parent[0]
        symbol_table = ast.parent.parent.symbol_table
        symbol_table_element = symbol_table[defined_var.value]
        type = symbol_table_element.type
        location = ast.value

        # In order to avoid redeclaration errors of variables we put a try catch block arround this piece of code
        try:
            symbol_table.insert(location, type)
        except:
            pass

    # 6. If the right child of a parent is a load then we know what type the left child will be
    elif isinstance(ast, LLVMVariable) and \
            isinstance(ast.parent, LLVMAssignment) and \
            isinstance(ast.parent[1], LLVMLoad):
        symbol_table = ast.parent.parent.symbol_table
        type = ast.parent[1].type
        location = ast.value

        # In order to avoid redeclaration errors of variables we put a try catch block arround this piece of code
        try:
            symbol_table.insert(location, type)
        except:
            pass


# Converts all variables into the right type.
# e.g. int x = y, y will be a variable from the listener, but must be the right type
def convertVar(ast):
    # Returns when the ast is not a variable type
    if not isinstance(ast, Variable):
        return


# This will perform all the necessary steps to populate the ast
def make_llvm_ast(ast):
    # Makes a tree of the symbol tables
    ast.traverse(connect_symbol_table)
    # The two methods of below should be combined in order to make it one pass and apply error checking
    # Create symbol table
    ast.traverse(assignment)  # Symbol table checks
    # Convert Variables into their right type based on the symbol table
    ast.traverse(convertVar)
