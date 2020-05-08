# TODO: limit all functions to an absolute maximum size of 20 lines (for readability)
class mips:
    output = ""


def mips_code(mips_ast):
    mips.output += mips_ast.comments()

    if isinstance(mips_ast, LLVMOperationSequence):
        mips_operation_sequence(mips_ast)
    elif isinstance(mips_ast, LLVMOperator):
        mips_operator(mips_ast)
    elif isinstance(mips_ast, LLVMFunction):
        mips_function(mips_ast)
    elif isinstance(mips_ast, LLVMArguments):
        mips_arguments(mips_ast)
    elif isinstance(mips_ast, LLVMConstant):
        mips_constant(mips_ast)
    elif isinstance(mips_ast, LLVMReservedType):
        mips_reserved_type(mips_ast)
    elif isinstance(mips_ast, Variable):
        mips_variable(mips_ast)
    else:
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
    pass


def mips_arguments(ast):
    pass


def mips_function(ast):
    mips.output += ast.value + ":"
    # We need to construct the stack first in order to maintain the variables in the used variables in the callee

    # We need to generate mips code for all the corresponding children
    for child in ast.children:
        mips.output += mips_code(child)
    pass


def global_mips(ast):
    mips_output = mips.output
    mips.output = ".data"

    # The llvm code is stored in the llvm code variable of the ast, we need to remove it from
    # there and store it into another return variable for this function
    ret_val = mips.output
    mips.output = mips_output
    return ret_val


def mips_assign(ast):
    pass


def mips_operation_sequence(ast):
    # ATTENTION we do not need to generate llvm code for children that are defined in the global scope as variables
    mips.output += ast.comments()
    for child in ast.children:
        # If there is no parent, we are the root statement sequence and the child is not a function
        # we do can not generate mips_code
        if not ast.parent and isinstance(child, LLVMVariable):
            continue
        mips_code(child)
    mips.output += '\n'


# This piece of code will create a printf statement if it is necessary
def get_mips_print(ast):
    pass


# This piece of code will create the scan of the code
def get_mips_scan(ast):
    pass


# Get the variable for the node (and load it from memory if required)
# Store must be true when you want to store into the variable
def variable(ast, store: bool = False, indexed: bool = False, index=0):
    pass


# Jump to a given label
def goto(label: str):
    pass


# Variable should be mips_formated, e.g. %1
def mips_load(ast, var: str):
    pass


def index_load(ast, result, index):
    pass


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


from src.LLVMAst import *
