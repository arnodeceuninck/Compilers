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
    # Return if we encounter a variable, argument list, allocate or load
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

    # 8. If we are in the global scope no operation is used for directly assigning constant values to variables
    elif isinstance(ast, LLVMVariable) and \
            isinstance(ast.parent, LLVMAssignment) and \
            (isinstance(ast.parent[1], LLVMConst) or isinstance(ast.parent[1], LLVMPrintStr)):

        symbol_table = ast.parent.parent.symbol_table
        type = ast.parent[1].get_type()
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
    elif ast.name not in ["printf", "__isoc99_scanf"]:
        return

    # Remove the parents link to its child
    index = ast.get_position(0)
    # Set the link of this child to none in order to remove it
    del ast.parent.children[index]
    # Then its parent so it can be deleted by python itself
    ast.parent = None


# We seek the root of the ast here
def get_root(ast):
    root = ast
    # Because the root has no parent we can use this in our advantage and seek the root like this
    while root.parent:
        root = root.parent
    return root


# We generate global code because we cant load floats directly so a intermediate step is required
def make_float_memory(ast):
    # If the statement is not a float then do not continue
    if not isinstance(ast, LLVMConstFloat):
        return
    # If the parent of the assign is llvmcode then we are in the global scope and we do not need to do anything
    if isinstance(ast.parent.parent, LLVMCode):
        return

    root = get_root(ast)
    # We need to make a new variable to identify the const floats
    var = ".f" + str(ast.id())
    var_ast = LLVMVariable(var)
    # We need the constant
    const = ast.value
    const_ast = LLVMConstFloat(const)

    # Generate the global variable for the const float
    const_float_ast = LLVMAssignment()
    const_float_ast.children.append(var_ast)
    const_float_ast.children.append(const_ast)
    # Set the correct parent of both children
    var_ast.parent = const_float_ast
    const_ast.parent = const_float_ast

    # Prepend it to the children of the root
    root_children = root.children.copy()
    root.children.clear()
    root.children.append(const_float_ast)
    root.children += root_children
    # Set the root as parent
    const_float_ast.parent = root

    # TODO make a copy of this in the LLVMAst class
    # Convert the current ast node into a variable so we can load it next time
    cur_ast = ast
    ast = LLVMVariable(var)
    ast.parent = cur_ast.parent
    ast.parent.children[ast.parent.children.index(cur_ast)] = ast
    return ast


def remove_null(string_list: list) -> list:
    # Remove the last 3 null terminating characters
    string_list[len(string_list) - 1] = string_list[len(string_list) - 1][:-3]
    return string_list


def cut_format_string(string: str) -> list:
    string_list = list()
    element = ""
    idx = 0
    string = str(string[1:-1])
    while idx < len(string):
        # We check for a format tag, because if there is then we need to split the string
        if string[idx] == '%':
            if string[idx - 1] == "\\":
                idx += 1
                continue
            string_list.append(element)
            element = ""
            if string[idx + 1] == "d":
                string_list.append(LLVMConstInt("d"))
            elif string[idx + 1] == "f":
                string_list.append(LLVMConstFloat("f"))
            elif string[idx + 1] == "s":
                pass
            elif string[idx + 1] == "c":
                pass

            idx += 2
            continue
        element += string[idx]
        idx += 1

    if len(element):
        string_list.append(element)
    return remove_null(string_list)


def search_string(string_id: str, ast: LLVMAst) -> str:
    root = get_root(ast)
    for child in root.children:
        if isinstance(child, LLVMFunction):
            return ""
        if child.children[0].name == string_id:
            return child.children[1].printvar


def make_string_id(node_id: str, string_id: str) -> str:
    return ".str." + node_id + "." + string_id


def make_string_global(string: str, string_id, ast) -> None:
    root = get_root(ast)
    var_ast = LLVMVariable(string_id)
    const_ast = LLVMPrintStr(string, len(string))

    # Generate the global variable for the const float
    assignment_ast = LLVMAssignment()
    assignment_ast.children.append(var_ast)
    assignment_ast.children.append(const_ast)
    # Set the correct parent of both children
    var_ast.parent = assignment_ast
    const_ast.parent = assignment_ast

    # append it to the children of the root
    root.children.append(assignment_ast)
    # Set the root as parent
    assignment_ast.parent = root


def make_printf_global(cut_string: list, ast: LLVMAst):
    for idx in range(len(cut_string)):
        if isinstance(cut_string[idx], str):
            string_id = make_string_id(str(ast.id()), str(idx))
            make_string_global(cut_string[idx], string_id, ast)


def create_printf_arguments(ast, cut_string):
    arguments = list()
    for idx in range(len(cut_string)):
        if isinstance(cut_string[idx], str):
            string_id = make_string_id(str(ast.id()), str(idx))
            new_argument = LLVMVariable(string_id)
            new_argument.type = "String"
        else:
            new_argument = cut_string[idx]
        new_argument.parent = ast
        arguments.append(new_argument)

    return arguments


def split_printf_arguments(ast: LLVMAst, cut_string):
    printf_arguments = create_printf_arguments(ast, cut_string)
    ast.children = printf_arguments


def search_string_ast(string, ast):
    root = get_root(ast)
    for child in root.children:
        if not isinstance(child, LLVMAssignment):
            continue
        elif not isinstance(child.children[1], LLVMPrintStr):
            continue
        elif child.children[1].printvar != string:
            continue
        return child.children[1]
    return None


def remove_original_string(string, ast):
    root = get_root(ast)

    string_ast = search_string_ast(string, ast)
    node_to_remove = string_ast.parent
    del root.children[root.children.index(node_to_remove)]


def create_printf(ast):
    if not isinstance(ast, LLVMFunctionUse):
        return
    elif ast.name not in ["printf", "__isoc99_scanf"]:
        return

    string_id = ast.children[0].children[0].name
    string = search_string(string_id, ast)
    cut_string = cut_format_string(string)

    # Make correct children out of the printf statement on the global scope
    make_printf_global(cut_string, ast)
    split_printf_arguments(ast, cut_string)
    remove_original_string(string, ast)


def get_llvm_node_type(root, type) -> list:
    ret_list = list()
    for child in root.children:
        if isinstance(child, type):
            ret_list.append(child)
    return ret_list


def get_assignments(root) -> list:
    return get_llvm_node_type(root, LLVMAssignment)


def get_functions(root) -> list:
    return get_llvm_node_type(root, LLVMFunction)


def reorder_root_children(ast):
    root = get_root(ast)
    first_children = get_assignments(root)
    last_children = get_functions(root)
    root.children.clear()
    root.children = first_children + last_children


# This will perform all the necessary steps to populate the ast
def make_llvm_ast(ast):
    # We need to remove printf as a function declaration because it causes all kind of issues
    ast.traverse(remove_printf_declaration)
    # Because load immediate for floats doesnt work
    ast.traverse(make_float_memory)
    # Cut the printf statement into pieces in order to be compilable in llvm
    ast.traverse(create_printf)
    # Put all the global assignments in front of the root children
    ast.traverse(reorder_root_children)

    # Makes a tree of the symbol tables
    ast.traverse(connect_symbol_table)
    # seeks the types for all the variables in the tree
    ast.traverse(assignment)
    # We need to remove all the allocate expressions, cause they serve no purpose
    ast.traverse(remove_allocate)

    # merge all the symbol tables into 1 big dict this we can use for assigning variables
    ast.symbol_table.merge()


def compile_llvm(input_file, output_file, debug_dot=False):
    input_stream = FileStream(input_file)
    lexer = llvmLexer.llvmLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = llvmParser.llvmParser(stream)
    tree = parser.start_rule()
    customListener = LLVMListener()
    walker = ParseTreeWalker()
    walker.walk(customListener, tree)
    javaForLife = customListener.trees[0]

    if debug_dot:
        dot(javaForLife, "output/llvm_debug_tree.dot")

    # Make the llvm ast complete
    make_llvm_ast(javaForLife)

    # Generate the mips code
    mips_code(javaForLife)
    # We just need to add the exit in llvm
    mips.output += "exit:\n"
    mips.output += "\tjal main\n"
    mips.output += "\tli $v0, 10\n"
    mips.output += "\tsyscall\n"
    text_file = open(output_file, "w")
    n = text_file.write(mips.output)
    text_file.close()
    # print(mips.output)
    return javaForLife
