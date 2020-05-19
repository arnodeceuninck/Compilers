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
    # 1. if we encounter an argument list then we need to add all the variables to it
    if isinstance(ast, LLVMArgumentList):
        for arg_idx in range(len(ast.children)):
            type = ast.children[arg_idx].type
            location = get_function_argument(ast.parent.name, arg_idx)

            try:
                ast.parent.symbol_table.insert(location, type)
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
    # the type of the operation
    elif isinstance(ast, LLVMVariable) \
            and isinstance(ast.parent, LLVMAssignment) \
            and isinstance(ast.parent[1], LLVMOperation) \
            and not isinstance(ast.parent[1], LLVMExtension):
        defined_var = ast.parent[1][0]
        symbol_table = ast.parent.parent.symbol_table
        location = ast.value
        type = ast.parent[1]
        # If we find that this so called variable is a constant then we need to seek the type
        if isinstance(defined_var, LLVMConst):
            type = defined_var.get_type()
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

    # 9. If the type is a fpext then use the correct type to assign
    elif isinstance(ast, LLVMVariable) and \
            isinstance(ast.parent, LLVMAssignment) and \
            isinstance(ast.parent[1], LLVMExtension):

        symbol_table = ast.parent.parent.symbol_table
        type = ast.parent[1].type_to
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
    # Do not delete a global scope variable but transform it
    if isinstance(ast.parent.parent, LLVMCode):
        # Create a new node
        new_node = get_const_node(str(ast.type), ast.get_default_val())
        new_node.parent = ast.parent
        new_node.parent.children.append(new_node)
        # Delete the old node
        del ast.parent.children[1]
        return

    # Store the operation sequence in order to use it to remove the allocate out of the tree
    operation_sequence = ast.parent.parent
    # Get the position of the allocate
    index = ast.get_position(1)
    # Delete this child
    del operation_sequence.children[index] # This is so f*cking dangerous, removing something while iterating over it

    # Find the top of the tree
    top = ast.parent.parent
    while top.parent:
        top = top.parent

    # Remove the link with the operation sequence by setting the parent node to None
    ast.parent.parent = None

    # Start removing again (because we delete a node while iterating)
    top.traverse(remove_allocate)


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
    const_ast = LLVMConstFloat(const, True)

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
    if not string_list or not isinstance(string_list[len(string_list) - 1], str):
        return string_list
    # Remove the last 3 null terminating characters
    string_list[len(string_list) - 1] = string_list[len(string_list) - 1][:-3]
    return string_list


def cut_format_string(string: str) -> list:
    string_list = list()
    element = ""
    idx = 0
    string = str(string[1:-1])
    # WARNING: When adding something here, also add it in AST.py
    translations = {"\\0A": "\\n", "\\08": "\\b", "\\1B": "\\e", "\\07": "\\a", "\\0C": "\\f", "\\0D": "\\r",
                    "\\09": "\\t", "\\0B": "\\v", "\\5C": "\\\\", "\\27": "\\'", "\\22": "\\\"", "\\3F": "\\?"}
    while idx < len(string):
        if string[idx] == "\\":
            # Should always be 2 chars after a backslash
            escaped = string[idx] + string[idx + 1] + string[idx + 2]
            to = translations.get(escaped)
            if to:
                string1 = string[:idx]
                string2 = string[idx + 3:]
                string = string1 + to + string2

        # We check for a format tag, because if there is then we need to split the string
        if string[idx] == '%':
            if string[idx - 1] == "\\":  # Huh? I'm confused, why doesn't this crash with the string "%"?
                idx += 1
                continue
            if len(element):
                string_list.append(element)
            element = ""
            if string[idx + 1] == "d":
                string_list.append(LLVMConstInt("d"))
            elif string[idx + 1] == "f":
                string_list.append(LLVMConstFloat("f"))
            elif string[idx + 1] == "s":
                variable = LLVMVariable("s")
                variable.type = "string"
                string_list.append(variable)
            elif string[idx + 1] == "c":
                string_list.append(LLVMConstChar("c"))

            idx += 2
            continue
        element += string[idx]
        idx += 1

    if len(element) and element != "\\00":
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
    var_ctr = 1
    for idx in range(len(cut_string)):
        if isinstance(cut_string[idx], str):
            string_id = make_string_id(str(ast.id()), str(idx))
            new_argument = LLVMVariable(string_id)
            new_argument.type = "String"
        else:
            if not idx:
                idx += 1
            new_argument = ast.children[0].children[var_ctr]
            var_ctr += 1
        new_argument.parent = ast
        arguments.append(new_argument)

    return arguments


def split_printf_arguments(ast: LLVMAst, cut_string):
    printf_arguments = create_printf_arguments(ast, cut_string)
    ast.children = printf_arguments


def search_string_ast(string_id, ast):
    root = get_root(ast)
    for child in root.children:
        if not isinstance(child, LLVMAssignment):
            continue
        elif not isinstance(child.children[1], LLVMPrintStr):
            continue
        elif child.children[0].name != string_id:
            continue
        return child.children[0]
    return None


def remove_original_string(ast):
    if not isinstance(ast, LLVMVariable):
        return
    if not ast.type != "original":
        return

    root = get_root(ast)

    node_to_remove = ast.parent
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
    mark_original_string(string_id, ast)


def mark_original_string(string_id, ast):
    string_ast = search_string_ast(string_id, ast)
    # Mark the string as original
    string_ast.original()


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


def make_print_string(string):
    if string[-1:] == "\"":
        string = string[1:-1]
    if string[-3:] == "\\00":
        string = string[:-3]
    return string


def rewrite_printstr(ast):
    if not isinstance(ast, LLVMPrintStr):
        return

    ast.printvar = make_print_string(ast.value)
    ast.value = ast.printvar


def get_const_val(type):
    if type == "int" or type == "i32":
        return 0
    elif type == "float" or type == "double":
        return 0.0
    elif type == "char" or type == "i8":
        return ' '


def get_var_node(type, name):
    variable = LLVMVariable(name)
    variable.type = type
    return variable


def get_const_node(type, value):
    const = None
    if type == "i32" or type == "int":
        const = LLVMConstInt(value)
    elif type == "double" or type == "float":
        const = LLVMConstFloat(value)
    elif type == "char" or type == "i8":
        const = LLVMConstChar(value)
    elif isinstance(type, LLVMArrayType):
        const = LLVMArrayType(type.size)
        const.type = type.type

    return const


def create_assignment(variable, var_name) -> LLVMAssignment:
    # Create the assignment
    _assignment = LLVMAssignment()
    _assignment.id()

    type = variable.type
    if isinstance(type, LLVMType) and not isinstance(type, LLVMArrayType):
        type = type.type

    # create the children
    variable_child = get_var_node(type, var_name)
    variable_child.id()
    const_val = get_const_val(type)
    const_child = get_const_node(type, const_val)

    # Set the children of the assignment
    _assignment.children.extend([variable_child, const_child])
    # Set the correct parent for both children
    variable_child.parent = _assignment
    variable_child.parent = _assignment

    return _assignment


def seek_constant(ast, value):
    retVal = False
    if not isinstance(ast, LLVMVariable):
        return False
    if value == ast.value:
        return ast.const

    for child in ast.children:
        retVal += seek_constant(child, value)
    return retVal


def move_global(root: LLVMCode):
    global_symbol_table = root.symbol_table
    total_table = root.symbol_table.total_table

    for key in total_table:
        try:
            # This line will error when it is not in the global table
            # Thus we will create the assignment on exception
            is_global = global_symbol_table[key]
        except:
            type = total_table[key].type
            if isinstance(type, LLVMType):
                type = type.type
            # If the variable is a string then it already is defined globally
            if type == "string":
                continue

            if type == "float" or type == "double":
                if seek_constant(root, key):
                    continue

            _assignment = create_assignment(total_table[key], key)
            # Because this variable is not global we need to append it to the children of the root
            root.children.append(_assignment)
            _assignment.parent = root


def make_correct_llvm_type(ast):
    if not isinstance(ast, LLVMVariable):
        return

    if ast.type == "String":
        ast.type = LLVMStringType(0)
    elif ast.type == "int":
        ast.type = "i32"
    elif ast.type == "char":
        ast.type = "i8"


def add_type_to_var(ast):
    if not isinstance(ast, LLVMVariable):
        return
    if ast.type:
        return
    symbol_table = ast.get_symbol_table()
    total_table = symbol_table.total_table
    if not (ast.value in total_table):
        ast.type = "j"
        return
    type = total_table[ast.value].type
    if isinstance(type, LLVMArgument):
        pass
    elif isinstance(type, LLVMType):
        ast.type = type
    elif type.lower() == "string" and not ast.type:
        ast.type = LLVMStringType(0)
    elif type.lower() == "string" and ast.type:
        pass
    else:
        ast.type = type


def convert_argument(ast):
    if not isinstance(ast, LLVMVariable):
        return
    try:
        arg_nr = str(int(ast.name))
        f_name = ast.parent.parent.parent.name
        ast.name = ".{f_name}.{arg_nr}".format(f_name=f_name, arg_nr=arg_nr)
        ast.value = ast.name
    except:
        return


def get_function_argument(f_name, idx):
    return "." + f_name + "." + str(idx)


# This will perform all the necessary steps to populate the ast
def make_llvm_ast(ast):
    # We need to remove printf as a function declaration because it causes all kind of issues
    ast.traverse(remove_printf_declaration)
    # Because load immediate for floats doesnt work
    ast.traverse(make_float_memory)
    # Cut the printf statement into pieces in order to be compilable in llvm
    ast.traverse(create_printf)
    # TODO Remove all the original printstrings
    # ast.traverse(remove_original_string)
    # Clean up all the strings such that they have a non " and non \00 appearance
    ast.traverse(rewrite_printstr)
    # Put all the global assignments in front of the root children
    # ast.traverse(reorder_root_children)
    reorder_root_children(ast)
    # # Make all the types to LLVMType in order to have a great consistency over the entire codebase
    # ast.traverse(make_correct_llvm_type)
    # This function is needed to convert all the arguments to custom unique arguments per function
    ast.traverse(convert_argument)

    #### SYMBOL TABLE GENERATION ####
    # Makes a tree of the symbol tables
    ast.traverse(connect_symbol_table)
    # seeks the types for all the variables in the tree
    ast.traverse(assignment)
    # We need to remove all the allocate expressions, cause they serve no purpose
    ast.traverse(remove_allocate)

    # merge all the symbol tables into 1 big dict this we can use for assigning variables
    ast.symbol_table.merge()

    # We need to move all the variable assignments to the global scope so we can use this
    move_global(ast)
    # Put all the global assignments in front of the root children
    # ast.traverse(reorder_root_children)
    reorder_root_children(ast)
    # # Make all the types to LLVMType in order to have a great consistency over the entire codebase
    # ast.traverse(make_correct_llvm_type)
    # Add a type to all the variable based on the symbol_table
    ast.traverse(add_type_to_var)


def generate_mips_code(javaForLife):
    # Generate the mips code
    mips_code(javaForLife)
    # We just need to add the exit in llvm
    mips.output += "exit:\n"
    mips.output += "\tjal main\n"
    mips.output += "\tli $v0, 10\n"
    mips.output += "\tsyscall\n"


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

    generate_mips_code(javaForLife)

    mips().to_file(output_file)
    # print(mips.output)
    return javaForLife
