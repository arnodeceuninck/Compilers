from src.symbolTable import SymbolTable


# TODO: limit all functions to an absolute maximum size of 20 lines (for readability)
class mips:
    output = ""

    def to_file(self, output_file):
        text_file = open(output_file, "w")
        n = text_file.write(mips.output)
        text_file.close()


def get_function_argument(f_name, idx):
    return "." + f_name + "." + str(idx)


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
    elif isinstance(mips_ast, LLVMFunctionUse):
        mips_function_use(mips_ast)
    elif isinstance(mips_ast, LLVMFunction):
        mips_function(mips_ast)
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
        mips_load(mips_ast, var_label=mips_ast[0].value)
    elif isinstance(mips_ast, LLVMArrayIndex):
        mips_array_index(mips_ast)
    elif isinstance(mips_ast, (LLVMOperationSequence, LLVMCode)):
        return ""
    else:
        raise Exception("Type not supported")


def mips_array_index(mips_ast):
    assert isinstance(mips_ast, LLVMArrayIndex)
    assert isinstance(mips_ast[0].type, LLVMArrayType)

    mips.output += "\tla $s0, {var}\n".format(var=mips_ast[0].name)

    if isinstance(mips_ast[1], LLVMConstInt):
        mips.output += "\tla $t0, {index}($s0)\n".format(index=mips_ast.get_offset())
    elif isinstance(mips_ast[1], LLVMVariable):
        mips_code(mips_ast[1])  # loads in $t1 (because variable is not on the left side of assignment
        size = mips_ast.type.type.get_size()
        mips.output += "\tli $t0, {val}\n".format(val=size)
        mips.output += "\tmul $t1, $t0, $t1\n"
        mips.output += "\tadd $t1, $t1, $s0\n"
        mips.output += "\tla $t0, 0($t1)\n"
        pass
    elif isinstance(mips_ast[1], LLVMConstChar):
        mips_ast.children[1].constval = int(str(mips_ast.children[1].constval))
        mips.output += "\tla $t0, {index}($s0)\n".format(index=mips_ast.get_offset())
        pass
    else:
        raise Exception("Type not found :-/")


def get_mips_type(mips_ast):
    if isinstance(mips_ast, LLVMOperation):
        return mips_type_operation(mips_ast)
    elif isinstance(mips_ast, LLVMFunction):
        return mips_type_function(mips_ast)
    elif isinstance(mips_ast, LLVMConst):
        return mips_type_constant(mips_ast)
    elif isinstance(mips_ast, LLVMVariable):
        return mips_type_variable(mips_ast)
    elif isinstance(mips_ast, LLVMLoad):
        return mips_type_load(mips_ast)
    elif isinstance(mips_ast, LLVMArgument):
        return mips_type_argument(mips_ast)
    elif isinstance(mips_ast, LLVMFunctionUse):
        return mips_type_function(mips_ast)
    elif isinstance(mips_ast, LLVMArrayIndex):
        return mips_type_array_index(mips_ast)
    raise Exception("I didn't think the code would get this far")


def mips_type_array_index(mips_ast):
    return mips_ast.type.type  # This throws away the information about pointers :-(


def mips_type_argument(mips_ast):
    print()
    pass


def mips_type_load(mips_ast):
    return mips_ast.type.type


def mips_type_operation(mips_ast):
    if isinstance(mips_ast, LLVMExtension):
        return mips_ast.type_to.type
    return mips_ast[0].type.type


def mips_type_function(mips_ast):
    if mips_ast.rettype == "int":
        return 'i32'
    elif mips_ast.rettype == "bool":
        return 'i1'
    elif mips_ast.rettype == "float":
        return 'float'
    elif mips_ast.rettype == "char":
        return 'i8'
    elif mips_ast.rettype == "void":
        return 'void'
    return str(mips_ast.rettype)


def symbol_table_type(name, ast):
    while ast.parent:
        ast = ast.parent
    element = ast.symbol_table.total_table[name]
    if element:
        return element.type
    else:
        raise Exception("Type not found")


def mips_extension(mips_ast):
    # print("WARNING: LLVMExtension to MIPS code not yet supported, moving instead")
    mips_code(mips_ast[0])
    # mips.output += "\tadd $s0, $t0, 0\n"
    return


def pointer_child(mips_ast, child):
    if len(mips_ast.children) > child:
        return symbol_table_type(mips_ast[child].name, mips_ast).ptr
    else:
        return 0


def mips_store(mips_ast):
    label = mips_ast[1].name

    # If the type is a pointer, and we want to store it in the pointer
    if pointer_child(mips_ast, 1) and mips_ast[1].type.ptr and not mips_ast[0].type.ptr:
        mips.output += "\tlw $t1, {name}\n".format(name=label)
    else:
        mips.output += "\tla $t1, {var}\n".format(var=label)

    to = "0($t1)"

    # We want to store a pointer, so get the pointer of the variable first
    if mips_ast[0].type.ptr and not pointer_child(mips_ast,
                                                  0):  # symbol_table_type(mips_ast[0].name, mips_ast).type.ptr:
        # Eerste is een pointer, dus we willen de waarde waarnaar dit element verwijst steken in het 2e
        mips.output += "\tla $t0, {var}\n".format(var=mips_ast[0].name)
        mips.output += "\tsw $t0, {var}\n".format(var=to)
    elif str(mips_ast[0].type) == "i8":
        mips.output += "\tlb $t0, {var}\n".format(var=mips_ast[0].name)
        mips.output += "\tsb $t0, {var}\n".format(var=to)
    else:
        mips.output += "\tlw $t0, {var}\n".format(var=mips_ast[0].name)
        mips.output += "\tsw $t0, {var}\n".format(var=to)


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
    # TODO: is the variable from mips_ast[0] loaded into $s0? support float
    # Jump to the false label if the var is zero
    mips.output += "\tbeqz {var}, {label}\n".format(var="$s0", label=mips_ast[2].name)
    # If not false, it must be true
    mips.output += "\tb {label}\n".format(label=mips_ast[1].name)


def mips_return(mips_ast):
    # If we do not return void then jump to the end and go to the stackframe part in mips
    if str(mips_ast.type) == "void":
        mips.output += "\tj exit.{f_name}\n".format(f_name=mips_ast.parent.parent.value)
        return

    # Load the variable in $t0 or $f0 depending on the type
    mips_code(mips_ast[0])
    # TODO fix that all the types become int and float
    if str(mips_ast.type) != "float":
        mips.output += "\tmove $v0, $t0\n"
    else:
        mips.output += "\tmov.s $f12, $f0\n"

    # Go to the stackframe part
    mips.output += "\tj exit.{f_name}\n".format(f_name=mips_ast.parent.parent.value)


def mips_operator(mips_ast):
    if isinstance(mips_ast, LLVMExtension):
        mips_extension(mips_ast)
    elif isinstance(mips_ast, LLVMBinaryOperation):
        mips_binary(mips_ast)


def mips_binary(mips_ast):
    assert isinstance(mips_ast, LLVMBinaryOperation)
    # TODO support float
    # This is valid for every equation
    # Generate mips code for the left and right side of the equation
    mips_code(mips_ast[0])
    mips_code(mips_ast[1])
    if mips_ast.operation == "add" or mips_ast.operation == "fadd":
        mips_b_add(mips_ast)
    elif mips_ast.operation == "sub" or mips_ast.operation == "fsub":
        mips_b_sub(mips_ast)
    elif mips_ast.operation == "sdiv" or mips_ast.operation == "fdiv":
        mips_b_div(mips_ast)
    elif mips_ast.operation == "mul" or mips_ast.operation == "fmul":
        mips_b_mul(mips_ast)
    elif mips_ast.operation == "srem" or mips_ast.operation == "frem":
        mips_b_rem(mips_ast)
    elif isinstance(mips_ast, LLVMCompareOperation):
        mips_compare(mips_ast)
    else:
        raise Exception("Unknown Operation: {}".format(mips_ast.operation))


def mips_b_add(mips_ast):
    if mips_ast.operation == "fadd":
        mips.output += "\tadd.s $f2, $f0, $f1\n"
    else:
        mips.output += "\tadd $s0, $t0, $t1\n"


def mips_b_sub(mips_ast):
    # TODO support float -> sub.s
    if mips_ast.operation == "fsub":
        mips.output += "\tsub.s $f2, $f0, $f1\n"
    else:
        mips.output += "\tsub $s0, $t0, $t1\n"


def mips_b_div(mips_ast):
    # TODO support float -> sub.s
    if mips_ast.operation == "fdiv":
        mips.output += "\tdiv.s $f2, $f0, $f1\n"
    else:
        mips.output += "\tdiv $t0, $t1\n"
        mips.output += "\tmflo $s0\n"


def mips_b_mul(mips_ast):
    if mips_ast.operation == "fmul":
        mips.output += "\tmul.s $f2, $f0, $f1\n"
    else:
        mips.output += "\tmul $s0, $t0, $t1\n"


def mips_b_rem(mips_ast):
    mips.output += "\tdiv $t0, $t1\n"
    mips.output += "\tmfhi $s0\n"  # Division result in $LO, remainder in $HI


# Do nothing on a mips include
def mips_include(mips_ast):
    pass


def mips_arguments(mips_ast):
    return ""


def get_reg_type(mips_ast):
    if "float" in str(mips_ast) or "double" in str(mips_ast):
        return "f"
    else:
        return "t"


def get_load_store_type(mips_ast):
    if "*" in str(mips_ast) and isinstance(mips_ast, LLVMArrayType):
        return "a"
    elif "i8" in str(mips_ast):
        return "b"
    elif "i32" in str(mips_ast) or "i64" in str(mips_ast):
        return "w"
    elif "float" in str(mips_ast) or "double" in str(mips_ast):
        return ".s"
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
        # Hieronder code van Basil na merge conflict
        # Hieronder code van Arno na merge conflict
        symbol_table_element = symbol_table.elements[v].type
        load_store = get_load_store_type(symbol_table_element)
        reg_type = get_reg_type(symbol_table_element)
        if isinstance(symbol_table.elements[v].type, LLVMArrayType):
            length = symbol_table_element.size
            for idx in range(length):
                stackframe_string += "\tl{load_store_type} ${reg_type}0, {var_label}+{idx}\n".format(
                    load_store_type=load_store,
                    reg_type=reg_type,
                    var_label=str(v),
                    idx=idx * 4)
                # stackframe_string += "\tlw $t0, 0($t0)\n" # Why doesn't this work
                stackframe_string += "\ts{load_store_type} ${reg_type}0, {frame_offset}($fp)\n".format(
                    load_store_type=load_store,
                    reg_type=reg_type,
                    frame_offset=frame_offset)
                if idx + 1 != length:
                    frame_offset -= 4  # + 4 to undo the -4
        # if symbol_table.elements[v].type == "float":
        #     # load the variable into register $f0
        #     # old
        #     stackframe_string += "\tl.s $f0, {var_label}\n".format(var_label=str(v))
        #     # new
        #     # stackframe_string += "\tlw $t0, {var}\n".format(var=v.name)
        #     # store this variable into the stack
        #     stackframe_string += "\ts.s $f0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)
        # elif str(symbol_table.elements[v].type) == "i8":
        #     # load the variable into register $t0
        #     # old
        #     stackframe_string += "\tlb $t0, {var_label}\n".format(var_label=str(v))
        #     # new
        #     # stackframe_string += "\tlw $t0, {var}\n".format(var=v.name)
        #     # store this variable into the stack
        #     stackframe_string += "\tsb $t0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)
        # elif isinstance(symbol_table.elements[v].type, LLVMArrayType):
        #     # TODO: this is not the way to do it, but I have no idea how to do it otherwise
        #     stackframe_string += "\tla $t0, {var_label}\n".format(var_label=str(v))
        #     # stackframe_string += "\tlw $t0, 0($t0)\n" # Why doesn't this work
        #     stackframe_string += "\tsw $t0, {frame_offset}($fp)\n".format(frame_offset=frame_offset)
        #     array = symbol_table.elements[v].type
        #     frame_offset += -array.size * 4 + 4 # + 4 to undo the -4
        else:
            stackframe_string += "\tl{load_store_type} ${reg_type}0, {var_label}\n".format(var_label=str(v),
                                                                                           load_store_type=load_store,
                                                                                           reg_type=reg_type)
            stackframe_string += "\ts{load_store_type} ${reg_type}0, {frame_offset}($fp)\n".format(
                frame_offset=frame_offset,
                load_store_type=load_store,
                reg_type=reg_type)
    stackframe_string += "\n"
    return stackframe_string


def build_end_stackframe(symbol_table: SymbolTable):
    # TODO: Must anything with Arrays happen?

    stackframe_string = ""

    # The frame offset will be the size of the stored variable amount we need to start 4 offset lower
    frame_offset = -symbol_table.get_len() - 4

    # We need to iterate over all the elements of the current symbol table in order to save all their values in reverse
    for i, v in list(reversed(list(enumerate(symbol_table.elements)))):
        symbol_table_element = symbol_table.elements[v].type
        load_store = get_load_store_type(symbol_table_element)
        reg_type = get_reg_type(symbol_table_element)
        if isinstance(symbol_table.elements[v].type, LLVMArrayType):
            length = symbol_table_element.size
            for idx in range(length - 1, 0 - 1, -1):
                stackframe_string += "\tl{load_store_type} ${reg_type}0, {frame_offset}($fp)\n".format(
                    load_store_type=load_store,
                    reg_type=reg_type,
                    frame_offset=frame_offset)
                # stackframe_string += "\tlw $t0, 0($t0)\n" # Why doesn't this work
                stackframe_string += "\ts{load_store_type} ${reg_type}0, {var_label}+{idx}\n".format(
                    load_store_type=load_store,
                    reg_type=reg_type,
                    var_label=str(v),
                    idx=idx * 4)
                if idx:
                    frame_offset += 4  # + 4 to undo the -4
            continue
        else:
            stackframe_string += "\tl{load_store_type} ${reg_type}0, {frame_offset}($fp)\n".format(
                frame_offset=frame_offset,
                load_store_type=load_store,
                reg_type=reg_type)
            stackframe_string += "\ts{load_store_type} ${reg_type}0, {var_label}\n".format(var_label=str(v),
                                                                                           load_store_type=load_store,
                                                                                           reg_type=reg_type)

        # Add 4 to the frame offset because we advance 1 variable
        frame_offset += 4

    # We retrieve the return address from the stack
    stackframe_string += "\tlw $ra, -4($fp)\n"
    # Then we change the stackpointers location to the one before the previous function
    stackframe_string += "\tmove $sp, $fp\n"
    # We need to load the old framepointer on to the stack
    stackframe_string += "\tlw $fp, 0($sp)\n"
    # Lastly we return to the caller of this function
    stackframe_string += "\tjr $ra\n"
    return stackframe_string

class data:
    RESULT = None
    LABEL = None

def find_assignment(mips_ast):
    if not isinstance(mips_ast, LLVMAssignment):
        return
    if mips_ast[0].value == data.LABEL:
        data.RESULT = mips_ast

def determine_array_size(label, mips_ast):
    while mips_ast.parent:
        mips_ast = mips_ast.parent
    data.LABEL = label
    mips_ast.traverse(find_assignment)
    return data.RESULT[1].type.size


def mips_print_string(mips_ast):
    mips_call_code = 4
    mips.output += "\n"
    label = None
    if mips_ast.value == "Pointer index":
        label = mips_ast[0].value
    elif isinstance(symbol_table_type(mips_ast.value, mips_ast), LLVMArrayType) or str(mips_ast.type) == "i8*":
        array = symbol_table_type(mips_ast.value, mips_ast)
        label = mips_ast.value
        mips.output += "\tlw $t0, {string_label}\n".format(string_label=label)
        mips.output += "\tli $v0, {op_code}\n".format(op_code=11)
        size = determine_array_size(label, mips_ast)
        for i in range(size): # TODO: determine size: range(array.size):
            mips.output += "\tlb $a0, {index}($t0)\n".format(index=i)
            mips.output += "\tsyscall\n"
        return
    else:
        label = mips_ast.value
    mips.output += "\tla $a0, {string_label}\n".format(string_label=label)
    mips.output += "\tli $v0, {op_code}\n".format(op_code=mips_call_code)
    mips.output += "\tsyscall\n"


def mips_print_float(mips_ast):
    mips_call_code = 2
    mips.output += "\n"
    mips.output += "\tl.s $f12, {string_label}\n".format(string_label=mips_ast.value)
    mips.output += "\tli $v0, {op_code}\n".format(op_code=mips_call_code)
    mips.output += "\tsyscall\n"


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
    mips.output += "\n"
    mips.output += "\tlb $a0, {var_name}\n".format(var_name=mips_ast.name)
    mips.output += "\tli $v0, {op_code}\n".format(op_code=mips_call_code)
    mips.output += "\tsyscall\n"


def mips_print(mips_ast):
    if isinstance(mips_ast, LLVMArrayIndex):
        # In case of array
        location = mips_ast[0].name
    else:
        location = mips_ast.value
    var_type = mips_ast.parent.parent.symbol_table.total_table[location].type
    mips_code(mips_ast)
    if isinstance(var_type, LLVMStringType) or str(mips_ast.type) == "i8*" or isinstance(mips_ast.type, LLVMArrayType):
        mips_print_string(mips_ast)
    elif var_type == "int" or str(var_type) == "i32":
        mips_print_int(mips_ast)
    elif var_type == "float" or str(var_type) == "double":
        mips_print_float(mips_ast)
    elif var_type == "char" or str(var_type) == "i8":
        mips_print_char(mips_ast)
    else:
        raise Exception("Type not supported")


def mips_scan(mips_ast):
    location = mips_ast.name
    if str(mips_ast.type) == "i8*" or isinstance(mips_ast.type, LLVMArrayType):
        type = symbol_table_type(location, mips_ast)
        # src: https://stackoverflow.com/questions/7969565/mips-how-to-store-user-input-string
        mips.output += "\tli $v0, 8\t# Take in input\n"
        mips.output += "\tla $a0, {buffer}\t# load byte space into address\n".format(buffer=location)
        mips.output += "\tli $a1, {bytes}\t# allocate the byte space for string\n".format(bytes=type.size + 1)
        mips.output += "\tmove $t0, $a0\t# save string to t0\n"
        mips.output += "\tsyscall\n"
    elif isinstance(mips_ast, LLVMVariable):
        # For some reason was the string not of my string class
        var_type = mips_ast.type.type
        if var_type == "int" or str(var_type) == "i32":
            mips.output += "\tli $v0, 5\n"
            mips.output += "\tsyscall\n"
            mips.output += "\tsw $v0, {location}\n".format(location=location)
        elif var_type == "float" or str(var_type) == "double":
            mips.output += "\tli $v0, 6\n"
            mips.output += "\tsyscall\n"
            mips.output += "\tsw $f0, {location}\n".format(location=location)
        elif var_type == "char" or str(var_type) == "i8":
            mips.output += "\tli $v0, 12\n"
            mips.output += "\tsyscall\n"
            mips.output += "\tsw $v0, {location}\n".format(location=location)


def mips_function_use(mips_ast):
    if mips_ast.name == "printf" and not isinstance(mips_ast.children[0], LLVMUseArgumentList):
        for child in mips_ast.children:
            mips_print(child)
        return
    if mips_ast.name == "__isoc99_scanf" and not isinstance(mips_ast.children[0], LLVMUseArgumentList):
        for child in mips_ast.children:
            mips_scan(child)
        return
    # If it is a function call then we need to take all the variables out of them
    # and store them in the arguments of the function
    # TODO fix this for arrays and check if characters work too
    for idx in range(len(mips_ast[0].children)):
        if str(mips_ast[0].children[idx].type) == "i8":
            mips.output += "\tlb $s0, {var_name}\n".format(var_name=mips_ast[0].children[idx].value)
            mips.output += "\tsb $s0, {var_name}\n".format(var_name=get_function_argument(mips_ast.name, idx))
            continue
        mips.output += "\tlw $s0, {var_name}\n".format(var_name=mips_ast[0].children[idx].value)
        mips.output += "\tsw $s0, {var_name}\n".format(var_name=get_function_argument(mips_ast.name, idx))

    mips.output += "\tjal {f_name}\n".format(f_name=mips_ast.name)


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
        if isinstance(child[0].type, LLVMType) and child[0].type.ptr:
            var_value = 0
            var_type = ".word"
        mips.output += "\t" + var_name + ": " + var_type + " " + str(var_value) + "\n"


def mips_assign(mips_ast):
    # Generate the mips code for the right side
    mips_code(mips_ast[1])
    label = mips_ast[0].name

    # If we encounter a function
    if isinstance(mips_ast[1], LLVMFunctionUse):
        # TODO add more types
        if str(mips_ast[0].type) == "float":
            mips.output += "\ts.s $f12, {var}".format(var=mips_ast[0].name)
        else:
            mips.output += "\tsw $v0, {var}".format(var=mips_ast[0].name)
        return
    # Store this value into the variable
    if get_mips_type(mips_ast[1]) == "float" or get_mips_type(mips_ast[1]) == "double":
        if isinstance(mips_ast[1], LLVMOperation):
            mips.output += "\ts.s $f2, {var}\n".format(var=label)
        else:
            mips.output += "\ts.s $f0, {var}\n".format(var=label)
    elif str(get_mips_type(mips_ast[1])) == "i8":
        if isinstance(mips_ast[1], LLVMOperation):
            mips.output += "\tsb $s0, {var}\n".format(var=label)
        else:
            mips.output += "\tsb $t0, {var}\n".format(var=label)
    else:
        if isinstance(mips_ast[1], LLVMOperation):
            mips.output += "\tsw $s0, {var}\n".format(var=label)
        else:
            mips.output += "\tsw $t0, {var}\n".format(var=label)


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
