def mips_variable(ast):
    # If the parent is an assignment then we need to just return since we store it afterwards into that location
    if isinstance(ast.parent, LLVMAssignment):
        return
    if isinstance(ast.type, LLVMStringType) or ast.type == "String":
        return

    # We need to check which side of the operation we are so we can load the variable into the correct register
    # Check if we are the left side of the parent
    if ast.parent[0] == ast:
        mips_load(ast, 0, ast.name)
    else:
        mips_load(ast, 1, ast.name)


def mips_load(mips_ast, idx=0, var_label=""):
    # Gets complicated because of our mips variable structure:
    # e.g. int x, is an i32, but gets stored in memory, so is actually an i32*,
    # This makes that an i32* can be two things:
    # A storage location for a number or a storage location for a pointer

    # If we want to load a pointer
    if mips_ast.type.ptr:
        # And the first child contains a pointer, you can just load the word
        if pointer_child(mips_ast, 1):
            mips.output += "\tlw $s0, {var}\n".format(var=var_label)
        # Else you have to load the address
        else:
            mips.output += "\tla $s0, {var}\n".format(var=var_label)
            # mips.output += "\tlw $s0, 0($s0)\n"

    # If we don't want to load a pointer (but the value itself)
    else:
        # If it is a storage location for the pointer, load the pointer first
        if pointer_child(mips_ast, 1):
            mips.output += "\tlw $s0, {var}\n".format(var=var_label)
            var_label = "0($s0)"

        if str(mips_ast.type) == "float" or str(mips_ast.type) == "double":
            mips_load_float(idx, var_label)
        elif str(mips_ast.type) == "i32":
            mips_load_int(idx, var_label)
        elif str(mips_ast.type) == "i8":
            mips_load_char(idx, var_label)


def mips_load_float(idx, var_label):
    mips.output += "\tl.s $f{idx}, {var_label}\n".format(idx=idx, var_label=var_label)


def mips_load_int(idx, var_label):
    mips.output += "\tlw $t{idx}, {var_label}\n".format(idx=idx, var_label=var_label)


def mips_load_char(idx, var_label):
    mips.output += "\tlw $t{idx}, {var_label}\n".format(idx=idx, var_label=var_label)


def mips_type_variable(ast):
    if isinstance(ast, LLVMVariable):
        return ast.type
    elif isinstance(ast, VFloat):
        return mips_type_v_float(ast, ignore_array)
    elif isinstance(ast, VChar):
        return mips_type_v_char(ast, ignore_array)
    else:
        raise Exception("Unknown Variable")


def mips_type_v_char(ast, ignore_array=False):
    return ""


def mips_type_v_float(ast, ignore_array=False):
    return ""


def mips_type_v_int(ast, ignore_array=False):
    return ""


def mips_default_variable(ast):
    return ""


from src.MIPS.MIPS import mips, mips_code, variable, get_mips_type, symbol_table_type, pointer_child
from src.LLVMAst.LLVMAst import *
