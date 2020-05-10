from src.LLVMAst.LLVMAst import LLVMOperationSequence, LLVMCode, LLVMArgumentList, LLVMAllocate, LLVMLoad, \
    LLVMFunction, LLVMVariable, LLVMConst, LLVMConstFloat, LLVMConstInt, LLVMAssignment, LLVMOperation, \
    LLVMStore
from src.Node.AST_utils import *
from src.symbolTable import *
from src.Dot.dot import dot
import sys
from gen_llvm import llvmLexer, llvmParser
from src.LLVMAst.LLVMAst_utils import *
from src.LLVMAst.LLVMAst import *
# import gen_llvm.llvmLexer
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from src.LLVMAst.LLVMListener import LLVMListener
from src.MIPS.MIPS import mips_code, mips

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
        if ast.children and isinstance(ast[0], LLVMUseArgumentList):
            return
        # Iterate over all the children to add all the arguments to the function scope
        for i in range(len(ast.children)):
            location = str(i)
            type = ast.children[i]
            try:
                ast.parent.parent.symbol_table.insert(location, type)
            except:
                pass

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
        try:
            symbol_table_element = symbol_table[defined_var.value]
        except:
            return
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

    # 7. If the right hand side is a function call then we need to take the return value and set it
    elif isinstance(ast, LLVMVariable) and \
            isinstance(ast.parent, LLVMAssignment) and \
            isinstance(ast.parent[1], LLVMFunctionUse):
        symbol_table = ast.parent.parent.symbol_table
        type = ast.parent[1].rettype
        location = ast.value

        # In order to avoid redeclaration errors of variables we put a try catch block arround this piece of code
        try:
            symbol_table.insert(location, type)
        except:
            pass


def remove_allocate(ast):
    # If the current variable is not an allocate then do proceed without doing anything
    if not isinstance(ast, LLVMAllocate):
        return

    # Store the operation sequence in order to use it to remove the allocate out of the tree
    operation_sequence = ast.parent.parent
    # Get the position of the allocate
    index = ast.get_position(1)
    # Delete this child
    del operation_sequence.children[index]

    # Remove the link with the operation sequence by setting the parent node to None
    ast.parent.parent = None


def remove_printf_declaration(ast):
    # TODO Check if the printf declaration is the one of stdio
    if not isinstance(ast, LLVMDeclare):
        return
    elif ast.name != "printf":
        return

    # Remove the parents link to its child
    index = ast.get_position(0)
    # Set the link of this child to none in order to remove it
    del ast.parent.children[index]
    # Then its parent so it can be deleted by python itself
    ast.parent = None


# This will perform all the necessary steps to populate the ast
def make_llvm_ast(ast):
    # We need to remove printf as a function declaration because it causes all kind of issues
    ast.traverse(remove_printf_declaration)
    # Makes a tree of the symbol tables
    ast.traverse(connect_symbol_table)
    # seeks the types for all the variables in the tree
    ast.traverse(assignment)
    # We need to remove all the allocate expressions, cause they serve no purpose
    ast.traverse(remove_allocate)

    # merge all the symbol tables into 1 big dict this we can use for assigning variables
    ast.symbol_table.merge()


def compile_llvm(input_file):
    input_stream = FileStream(input_file)
    lexer = llvmLexer.llvmLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = llvmParser.llvmParser(stream)
    tree = parser.start_rule()
    customListener = LLVMListener()
    walker = ParseTreeWalker()
    walker.walk(customListener, tree)
    javaForLife = customListener.trees[0]

    # Make the llvm ast complete
    make_llvm_ast(javaForLife)
    # Generate the mips code
    mips_code(javaForLife)
    # We just need to add the exit in llvm
    mips.output += "exit:\n"
    mips.output += "\tjal main\n"
    mips.output += "\tli $v0, 10\n"
    mips.output += "\tsyscall\n"
    print(mips.output)
    return javaForLife
