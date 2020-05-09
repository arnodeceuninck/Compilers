from src.symbolTable import SymbolTable


# TODO: limit all functions to an absolute maximum size of 20 lines (for readability)
class mips:
    output = ""


def mips_code(mips_ast):
    # mips.output += mips_ast.comments()

    if isinstance(mips_ast, (LLVMOperationSequence, LLVMCode)):
        mips_operation_sequence(mips_ast)
    # elif isinstance(mips_ast, LLVMOperator):
    #     mips_operator(mips_ast)
    elif isinstance(mips_ast, LLVMFunction):
        mips_function(mips_ast)
    elif isinstance(mips_ast, LLVMArgumentList):
        mips_arguments(mips_ast)
    # elif isinstance(mips_ast, LLVMConstant):
    #     mips_constant(mips_ast)
    # elif isinstance(mips_ast, LLVMReservedType):
    #     mips_reserved_type(mips_ast)
    # elif isinstance(mips_ast, Variable):
    #     mips_variable(mips_ast)
    else:
        return ""
        raise Exception("Unknown AST")


def get_mips_type(ast, ignore_array=False):
    if isinstance(ast, Operator):
        return mips_type_operate(ast)
    elif isinstance(ast, Function):
        return mips_type_function(ast)
    elif isinstance(ast, Constant):
        return mips_type_constant(ast)
    elif isinstance(ast, Variable):
        return mips_type_variable(ast, ignore_array)
    raise Exception("I didn't think the code would get this far")


def mips_type_function(ast):
    if ast.return_type == "int":
        return 'i32'
    elif ast.return_type == "bool":
        return 'i1'
    elif ast.return_type == "float":
        return 'float'
    elif ast.return_type == "char":
        return 'i8'
    elif ast.return_type == "void":
        return 'void'


def mips_operator(ast):
    if isinstance(ast, LLVMBinary):
        mips_binary(ast)
    else:
        return ""
        raise Exception("Unknown AST")


def mips_binary(ast):
    if isinstance(ast, Assign):
        mips_assign(ast)
    elif isinstance(ast, Compare):
        mips_compare(ast)
    elif isinstance(ast, Operate):
        mips_operate(ast)
    else:
        raise Exception("Unknown AST")


def mips_include(ast):
    return ""


def mips_arguments(ast):
    return ""


def build_start_stackframe(symbol_table: SymbolTable):
    stackframe_string = ""
    # We first need to push the old framepointer on to the stack
    stackframe_string += "\tsw $fp, 0($sp)\n"
    # Then we change the framepointers location to the current one
    stackframe_string += "\tmove $fp, $sp\n"
    # Then we need to allocate the entire stack based on the amount of elements in the current function
    # we get this by getting the amount of elements in the symbol table
    # + 4 because we have the return address to take into account
    # another + 4 because we need to take the fp into account that is saved
    stackframe_size = symbol_table.get_len() + 4 + 4
    # We decide form the line for reserving the amount of space on the stack
    stackframe_string += "\tsubu $sp, $sp, {reserve_amount}\n".format(reserve_amount=str(stackframe_size))
    frame_offset = -4
    # We know that the first thing we need to store is the return address
    # So we store it first on the stack
    stackframe_string += "\tsw	$ra, -4($fp)\n"

    # We need to iterate over all the elements of the current symbol table in order to save all their values
    for i, v in enumerate(symbol_table.elements):
        # Add -4 to the frame offset because we advance 1 variable
        frame_offset += -4
        # Load the variable used into register t0
        # But first calculate its offset in the gp
        var_offset = symbol_table.get_index_offset(v)
        stackframe_string += "\tlw $t0, {offset}($gp)\n".format(offset=str(var_offset))
        # store this variable into the stack
        stackframe_string += "\tsw $t0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)
    return stackframe_string


def build_end_stackframe(symbol_table: SymbolTable):
    stackframe_string = ""

    # The frame offset will be the size of the stored variable amount we need to start 4 offset lower
    frame_offset = -symbol_table.get_len() - 4

    # We need to iterate over all the elements of the current symbol table in order to save all their values
    for i, v in enumerate(symbol_table.elements):
        # load this variable from the stack
        stackframe_string += "\tlw $t0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)

        # store the variable into register the gp because it was the previous one
        # But first calculate its offset in the gp
        var_offset = symbol_table.get_index_offset(v)
        stackframe_string += "\tsw $t0, {offset}($gp)\n".format(offset=str(var_offset))

        # Add 4 to the frame offset because we advance 1 variable
        frame_offset += 4

    # We retrieve the return address from the stack
    stackframe_string += "\tsw	$ra, -4($fp)\n"
    # Then we change the stackpointers location to the one before the previous function
    stackframe_string += "\tmove $fp, $sp\n"
    # We need to load the old framepointer on to the stack
    stackframe_string += "\tlw $fp, 0($sp)\n"
    # Lastly we return to the caller of this function
    stackframe_string += "\tjr $ra\n"
    return stackframe_string


def mips_function(ast):
    # Create the label for the current function
    mips.output += ast.value + ":"

    # We need to construct the stack first in order to maintain the variables in the used variables in the callee
    mips.output += build_start_stackframe(ast.symbol_table.children[0])

    # We need to generate mips code for all the corresponding children
    for child in ast.children:
        mips_code(child)

    # We need to deconstruct the stackframe
    mips.output += build_end_stackframe(ast.symbol_table.children[0])


def global_mips(ast):
    mips_output = mips.output
    mips.output = ".data"

    # The llvm code is stored in the llvm code variable of the ast, we need to remove it from
    # there and store it into another return variable for this function
    ret_val = mips.output
    mips.output = mips_output
    return ret_val


def mips_assign(ast):
    return ""


def mips_operation_sequence(ast):
    # ATTENTION we do not need to generate llvm code for children that are defined in the global scope as variables
    # mips.output += ast.comments()
    for child in ast.children:
        # If there is no parent, we are the root statement sequence and the child is not a function
        # we do can not generate mips_code
        if not ast.parent and isinstance(child, LLVMVariable):
            continue
        mips_code(child)
    mips.output += '\n'


# This piece of code will create a printf statement if it is necessary
def get_mips_print(ast):
    return ""


# This piece of code will create the scan of the code
def get_mips_scan(ast):
    return ""


# Get the variable for the node (and load it from memory if required)
# Store must be true when you want to store into the variable
def variable(ast, store: bool = False, indexed: bool = False, index=0):
    return ""


# Jump to a given label
def goto(label: str):
    return ""


# Variable should be mips_formated, e.g. %1
def mips_load(ast, var: str):
    return ""


def index_load(ast, result, index):
    return ""


def mips_argument(ast):
    return ""


# Write the llvm version of the ast to the filename
def to_mips(ast, filename):
    mips.output = ""

    mips_code(ast)

    # Write output to the outputfile
    outputFile = open(filename, "w")
    outputFile.write(mips.output)
    outputFile.close()


from src.LLVMAst.LLVMAst import *
