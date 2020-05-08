def mips_compare(ast):
    if isinstance(ast, LogicAnd):
        mips_logic_and(ast)
    else:
        mips_default_compare(ast)


def mips_default_compare(ast):
    pass


def mips_logic_and(ast):
    pass


from src.MIPS.MIPS import mips_code, mips, variable, get_mips_type
