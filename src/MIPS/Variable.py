def mips_variable(ast):
    mips_default_variable(ast)


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
