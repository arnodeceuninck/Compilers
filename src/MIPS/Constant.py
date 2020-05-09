def mips_constant(ast):
    if isinstance(ast, CArray):
        mips_c_array(ast)
    elif isinstance(ast, CChar):
        mips_c_char(ast)
    elif isinstance(ast, CString):
        mips_c_string(ast)
    else:
        mips_default_constant(ast)


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
