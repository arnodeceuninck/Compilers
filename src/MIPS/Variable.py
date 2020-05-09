def mips_variable(ast):
    # If the parent is an assignment then we need to just return since we store it afterwards into that location
    if isinstance(ast.parent, LLVMAssignment):
        return

    # We need to check which side of the operation we are so we can load the variable into the correct register
    # Check if we are the left side of the parent
    if ast.parent[0] == ast:
        code = "lw $t0, {index_offset}($gp)\n"
    else:
        code = "lw $t1, {index_offset}($gp)\n"

    # Add the correct index offset to the statement
    code.format(index_offset=ast.get_index_offset())

    # Add the newly generated code to the mips code
    mips.output += code

def mips_type_variable(ast, ignore_array=False):
    if isinstance(ast, VInt):
        return mips_type_v_int(ast, ignore_array)
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


from src.MIPS.MIPS import mips, mips_code, variable, get_mips_type
from src.LLVMAst.LLVMAst import LLVMAssignment
