from src.symbolTable import SymbolTable


# TODO: limit all functions to an absolute maximum size of 20 lines (for readability)
class mips:
    output = ""

    def to_file(self, output_file):
        text_file = open(output_file, "w")
        n = text_file.write(mips.output)
        text_file.close()


def mips_code(mips_ast):

    if isinstance(mips_ast.parent, LLVMOperationSequence):
        mips.output += "\n"

    mips.output += "\t# {comment}\n".format(comment=mips_ast.comments())

    # generate the global mips along with the variables using it, like the constant floats
    if not mips_ast.parent:
        global_mips(mips_ast)
        mips.output += ".text\n"
        mips.output += "j exit\n"
    # Skip if the parent is llvm code because we are in the global scope
    if isinstance(mips_ast, LLVMAssignment) and isinstance(mips_ast.parent, LLVMCode):
        return

    if isinstance(mips_ast, (LLVMOperationSequence, LLVMCode)):
        mips_operation_sequence(mips_ast)
    if isinstance(mips_ast, LLVMAssignment):
        mips_assign(mips_ast)
    elif isinstance(mips_ast, LLVMOperation):
        mips_operator(mips_ast)
    elif isinstance(mips_ast, LLVMFunction):
        mips_function(mips_ast)
    elif isinstance(mips_ast, LLVMFunctionUse):
        mips_function_use(mips_ast)
    elif isinstance(mips_ast, LLVMArgumentList):
        mips_arguments(mips_ast)
    elif isinstance(mips_ast, LLVMConst):
        mips_constant(mips_ast)
    elif isinstance(mips_ast, LLVMReturn):
        mips_return(mips_ast)
    elif isinstance(mips_ast, LLVMVariable):
        mips_variable(mips_ast)
    elif isinstance(mips_ast, LLVMStore):
        mips_store(mips_ast)
    elif isinstance(mips_ast, LLVMLabel):
        mips_label(mips_ast)
    elif isinstance(mips_ast, LLVMBranch):
        mips_branch(mips_ast)
    elif isinstance(mips_ast, LLVMLoad):
        mips_load(mips_ast)
    else:
        return ""


def get_mips_type(mips_ast, ignore_array=False):
    if isinstance(mips_ast, Operator):
        return mips_type_operate(mips_ast)
    elif isinstance(mips_ast, Function):
        return mips_type_function(mips_ast)
    elif isinstance(mips_ast, Constant):
        return mips_type_constant(mips_ast)
    elif isinstance(mips_ast, Variable):
        return mips_type_variable(mips_ast, ignore_array)
    raise Exception("I didn't think the code would get this far")


def mips_type_function(mips_ast):
    if mips_ast.return_type == "int":
        return 'i32'
    elif mips_ast.return_type == "bool":
        return 'i1'
    elif mips_ast.return_type == "float":
        return 'float'
    elif mips_ast.return_type == "char":
        return 'i8'
    elif mips_ast.return_type == "void":
        return 'void'

def symbol_table_type(name, ast):
    while ast.parent:
        ast = ast.parent
    element = ast.symbol_table.total_table[name]
    if element:
        return element
    else:
        raise Exception("Type not found")

def mips_store(mips_ast):
    # New code
    if symbol_table_type(mips_ast[0].name, mips_ast).type.ptr:
        # Eerste is een pointer, dus we willen de waarde waarnaar dit element verwijst steken in het 2e
        mips.output += "\tla $t0, {var}\n".format(var=mips_ast[0].name)
        mips.output += "\tla $t1, {var}\n".format(var=mips_ast[1].name)
        mips.output += "\tsw $t0, 0($t1)\n".format(var=mips_ast[1].name)
    else:
        mips.output += "\tlw $t0, {var}\n".format(var=mips_ast[0].name)
        mips.output += "\tsw $t0, {var}\n".format(var=mips_ast[1].name)


    # Old code
    # # TODO pointervalues
    # # Load the variable to store into register $t0
    # # var_offset = mips_ast.parent.symbol_table.get_index_offset(str(mips_ast[0]))
    # # mips.output += "\tlw $t0, {offset}($gp)\n".format(offset=str(var_offset))
    #
    #
    # # Store this variable then on the location of the variable where the value needs to be stored
    # var_offset = mips_ast.parent.symbol_table.get_index_offset(str(mips_ast[1]))
    # mips.output += "\tsw $t0, {offset}($gp)\n".format(offset=str(var_offset))


def mips_label(mips_ast):
    mips.output += "{name}:\n".format(name=mips_ast.name)


def mips_branch(mips_ast):
    if isinstance(mips_ast, LLVMNormalBranch):
        mips_normal_branch(mips_ast)
    elif isinstance(mips_ast, LLVMConditionalBranch):
        mips_conditional_branch(mips_ast)


def mips_normal_branch(mips_ast):
    mips.output += "\tb {label}\n".format(label=mips_ast[0].name)


def mips_conditional_branch(mips_ast):
    # TODO: is the variable from mips_ast[0] loaded into $s0?
    # Jump to the false label if the var is zero
    mips.output += "\tbeqz {var}, {label}\n".format(var="$s0", label=mips_ast[2].name)
    # If not false, it must be true
    mips.output += "\tb {label}\n".format(label=mips_ast[1].name)


def mips_return(mips_ast):
    # If we do not return void then jump to the end and go to the stackframe part in mips
    if mips_ast.type.type == "void":
        mips.output += "\tj exit.{f_name}\n".format(f_name=mips_ast.parent.parent.value)
        return

    # Load the variable in $t0 or $f0 depending on the type
    mips_code(mips_ast[0])
    # TODO fix that all the types become int and float
    if type != "float":
        mips.output += "\tmove $v0, $t0\n"

    # Go to the stackframe part
    mips.output += "\tj exit.{f_name}\n".format(f_name=mips_ast.parent.parent.value)


def mips_operator(mips_ast):
    if isinstance(mips_ast, LLVMExtension):
        print("WARNING: LLVMExtension to MIPS code not yet supported, moving instead")
        mips_code(mips_ast[0])
        mips.output += "\tadd $s0, $t0, 0\n"
        return
    elif isinstance(mips_ast, LLVMBinaryOperation):
        mips_binary(mips_ast)


def mips_binary(mips_ast):
    assert isinstance(mips_ast, LLVMBinaryOperation)
    # TODO support float
    # This is valid for every equation
    # Generate mips code for the left and right side of the equation
    mips_code(mips_ast[0])
    mips_code(mips_ast[1])
    if mips_ast.operation == "add":
        mips_b_add(mips_ast)
    elif mips_ast.operation == "sub":
        mips_b_sub(mips_ast)
    elif mips_ast.operation == "sdiv":
        mips_b_div(mips_ast)
    elif mips_ast.operation == "mul":
        mips_b_mul(mips_ast)
    elif mips_ast.operation == "srem":
        mips_b_rem(mips_ast)
    elif isinstance(mips_ast, LLVMCompareOperation):
        mips_compare(mips_ast)
    else:
        raise Exception("Unknown Operation: {}".format(mips_ast.operation))


def mips_b_add(mips_ast):
    # TODO support float -> add.s
    mips.output += "\tadd $s0, $t0, $t1\n"


def mips_b_sub(mips_ast):
    # TODO support float -> sub.s
    mips.output += "\tsub $s0, $t0, $t1\n"


def mips_b_div(mips_ast):
    # TODO support float -> sub.s
    mips.output += "\tdiv $t0, $t1\n"
    mips.output += "\tmflo $s0\n"


def mips_b_mul(mips_ast):
    # TODO support float -> mult.s
    mips.output += "\tmult $t0, $t1\n"
    mips.output += "\tmflo $s0\n"


def mips_b_rem(mips_ast):
    mips.output += "\tdiv $t0, $t1\n"
    mips.output += "\tmfhi $s0\n"  # Division result in $LO, remainder in $HI


# Do nothing on a mips include
def mips_include(mips_ast):
    pass


def mips_arguments(mips_ast):
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
    stackframe_string += "\tsw $ra, -4($fp)\n"

    # We need to iterate over all the elements of the current symbol table in order to save all their values
    for i, v in enumerate(symbol_table.elements):
        # Add -4 to the frame offset because we advance 1 variable
        frame_offset += -4
        # load the variable into register $t0
        # old
        stackframe_string += "\tlw $t0, {var_label}\n".format(var_label=str(v))
        # new
        # stackframe_string += "\tlw $t0, {var}\n".format(var=v.name)
        # store this variable into the stack
        stackframe_string += "\tsw $t0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)

    stackframe_string += "\n"
    return stackframe_string


def build_end_stackframe(symbol_table: SymbolTable):
    stackframe_string = ""

    # The frame offset will be the size of the stored variable amount we need to start 4 offset lower
    frame_offset = -symbol_table.get_len() - 4

    # We need to iterate over all the elements of the current symbol table in order to save all their values
    for i, v in enumerate(symbol_table.elements):
        # load this variable from the stack
        stackframe_string += "\tlw $t0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)

        # store the variable into label
        stackframe_string += "\tsw $t0, {var_label}\n".format(var_label=str(v))

        # Add 4 to the frame offset because we advance 1 variable
        frame_offset += 4

    # We retrieve the return address from the stack
    stackframe_string += "\tsw $ra, -4($fp)\n"
    # Then we change the stackpointers location to the one before the previous function
    stackframe_string += "\tmove $fp, $sp\n"
    # We need to load the old framepointer on to the stack
    stackframe_string += "\tlw $fp, 0($sp)\n"
    # Lastly we return to the caller of this function
    stackframe_string += "\tjr $ra\n"
    return stackframe_string


def mips_print_string(mips_ast):
    mips_call_code = 4
    mips.output += "\n"
    mips.output += "\tla $a0, {string_label}\n".format(string_label=mips_ast.value)
    mips.output += "\tli $v0, {op_code}\n".format(op_code=mips_call_code)
    mips.output += "\tsyscall\n"


def mips_print_float(mips_ast):
    mips_call_code = 2


def mips_print_int(mips_ast):
    mips_code(mips_ast)

    # Get the place where the variable is saved
    var_save_location = "$t0"
    if mips_ast.parent.children.index(mips_ast):
        var_save_location = "$t1"

    mips_call_code = 1
    mips.output += "\n"
    mips.output += "\tmove $a0, {var_save_location}\n".format(var_save_location=var_save_location)
    mips.output += "\tli $v0, {op_code}\n".format(op_code=mips_call_code)
    mips.output += "\tsyscall\n"


def mips_print_char(mips_ast):
    mips_call_code = 11
    pass


def mips_print(mips_ast):
    location = mips_ast.value
    var_type = mips_ast.parent.parent.symbol_table.total_table[location].type
    mips_code(mips_ast)
    if isinstance(var_type, LLVMStringType):
        mips_print_string(mips_ast)
    elif var_type == "int" or str(var_type) == "i32":
        mips_print_int(mips_ast)
    elif var_type == "float":
        mips_print_float(mips_ast)
    elif var_type == "char" or str(var_type) == "i8":
        mips_print_char(mips_ast)


def mips_function_use(mips_ast):
    if mips_ast.name == "printf" and not isinstance(mips_ast.children[0], LLVMUseArgumentList):
        for child in mips_ast.children:
            mips_print(child)
    # Function call
    if isinstance(mips_ast.parent, LLVMOperationSequence):
        return ""


def mips_function(mips_ast):
    # Create the label for the current function
    mips.output += mips_ast.value + ":\n"

    # We need to construct the stack first in order to maintain the variables in the used variables in the callee
    mips.output += build_start_stackframe(mips_ast.symbol_table.children[0])

    # We need to generate mips code for all the corresponding children
    for child in mips_ast.children:
        mips_code(child)

    # We need to deconstruct the stackframe but first make a label in order to be able to jump to it
    mips.output += "exit.{function_name}:\n".format(function_name=mips_ast.value)
    mips.output += build_end_stackframe(mips_ast.symbol_table.children[0])


def global_mips(mips_ast):
    if not isinstance(mips_ast, LLVMCode):
        return
    mips.output = ".data\n"
    for child in mips_ast.children:
        # If we encounter a function we do not need to generate mips code for that
        if isinstance(child, LLVMFunction):
            continue
        var_name = child.children[0].name
        var_value = child.children[1].get_str_value()
        var_type = child.children[1].get_mips_type()
        mips.output += "\t" + var_name + ": " + var_type + " " + str(var_value) + "\n"


def mips_assign(mips_ast):
    # Generate the mips code for the right side
    mips_code(mips_ast[1])

    # TODO support floats
    # Store this value into the variable
    # mips.output += "\tsw $s0, {index_offset}($gp)\n".format(index_offset=str(mips_ast[0].get_index_offset()))

    mips.output += "\tsw $s0, {var}\n".format(var=mips_ast[0].name)


def mips_operation_sequence(mips_ast):
    # ATTENTION we do not need to generate llvm code for children that are defined in the global scope as variables
    # mips.output += mips_ast.comments()
    for child in mips_ast.children:
        # If there is no parent, we are the root statement sequence and the child is not a function
        # we do can not generate mips_code
        if not mips_ast.parent and isinstance(child, LLVMVariable):
            continue
        mips_code(child)
    mips.output += '\n'


# This piece of code will create a printf statement if it is necessary
def get_mips_print(mips_ast):
    return ""


# This piece of code will create the scan of the code
def get_mips_scan(mips_ast):
    return ""


# Get the variable for the node (and load it from memory if required)
# Store must be true when you want to store into the variable
def variable(mips_ast, store: bool = False, indexed: bool = False, index=0):
    return ""


# Jump to a given label
def goto(label: str):
    return ""


# Variable should be mips_formated, e.g. %1
def mips_load(mips_ast):

    mips.output += "\tlw $s0, {var}\n".format(var=mips_ast[0].name)
    return

    mips_code(mips_ast.children[0])
    # mips.output += "\tla $t0, {var}\n".format(var=mips_ast.children[0].name)
    if mips_ast.type.ptr:
        # pass
        # mips.output += "\tla $s0, 0($t0)\n"
        mips.output += "\tlw $s0, 0($t0)\n"
    # # We know that the child will be a variable so we need to load that value
    # mips_code(mips_ast.children[0])
    # # Then we need to put that value stored in $t0 into $s0
    # # so that we can store it in the variable that demands the load
    else:
        mips.output += "\tmove $s0, $t0\n"
    pass


def index_load(mips_ast, result, index):
    return ""


def mips_argument(mips_ast):
    return ""


# Write the llvm version of the mips_ast to the filename
def to_mips(mips_ast, filename):
    mips.output = ""

    mips_code(mips_ast)

    # Write output to the outputfile
    outputFile = open(filename, "w")
    outputFile.write(mips.output)
    outputFile.close()


from src.LLVMAst.LLVMAst import *
from src.MIPS.Compare import *
from src.MIPS.Constant import *
from src.MIPS.Operate import *
from src.MIPS.Variable import *
