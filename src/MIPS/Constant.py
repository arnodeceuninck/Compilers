def mips_constant(ast):
    if isinstance(ast, LLVMConstFloat):
        mips_c_float(ast)
    elif isinstance(ast, LLVMConstInt):
        mips_c_int(ast)
    else:
        mips_default_constant(ast)


def mips_c_float(ast):
    # If the parent is an assignment then we need to just return since we store it afterwards into that location
    if isinstance(ast.parent, LLVMAssignment):
        return

    # We need to check which side of the equation we are so we can load the variable into the correct register
    # Check if we are the left side of the parent
    if ast.parent[0] == ast:
        code = "lw $t0, {index_offset}($gp)\n"
    else:
        code = "lw $t1, {index_offset}($gp)\n"

    # Add the correct index offset to the statement
    code.format(index_offset=ast.get_index_offset())

    # Add the newly generated code to the mips code
    mips.output += code


def mips_c_int(ast):
    # We need to check which side of the operation we are so we can load the variable into the correct register

    # Check if we are the left side of the parent
    if ast.parent[0] == ast:
        code = "li $t0, {load_value}\n".format(load_value=str(ast.value))
    else:
        code = "li $t1, {load_value}\n".format(load_value=str(ast.value))

    # Add the newly generated code to the mips code
    mips.output += code


def mips_type_constant(ast):
    if isinstance(ast, CArray):
        return mips_type_c_array(ast)
    elif isinstance(ast, CInt):
        return mips_type_c_int(ast)
    elif isinstance(ast, CFloat):
        return mips_type_c_float(ast)
    elif isinstance(ast, CChar):
        return mips_type_c_char(ast)
    elif isinstance(ast, CBool):
        return mips_type_c_bool(ast)
    elif isinstance(ast, CString):
        return mips_type_c_string(ast)
    else:
        raise Exception("Unknown Constant")


def mips_type_c_string(ast):
    return ""


def mips_type_c_bool(ast):
    return "i1"


def mips_type_c_char(ast):
    return "i8"


def mips_type_c_float(ast):
    return "float"


def mips_type_c_int(ast):
    return "i32"


def mips_type_c_array(ast):
    if len(ast.children) == 0:
        return None
    type = get_mips_type(ast[0])
    for child in ast.children:
        if type != child.get_mips_type():
            return None
    return type


def mips_default_constant(ast):
    return ""


def mips_c_array(ast):
    raise Exception("Constant Array not (yet?) supported")


def mips_c_char(ast):
    return ""


def mips_c_string(ast):
    return ""


from src.MIPS.MIPS import mips_code, mips, variable, get_mips_type
from src.LLVMAst.LLVMAst import LLVMConst, LLVMConstFloat, LLVMConstInt
