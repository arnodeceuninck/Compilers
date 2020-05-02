def llvm_variable(ast):
    llvm_default_variable(ast)


def llvm_type_variable(ast, ignore_array=False):
    if isinstance(ast, VInt):
        return llvm_type_v_int(ast, ignore_array)
    elif isinstance(ast, VFloat):
        return llvm_type_v_float(ast, ignore_array)
    elif isinstance(ast, VChar):
        return llvm_type_v_char(ast, ignore_array)
    else:
        raise Exception("Unknown Variable")


def llvm_type_v_char(ast, ignore_array=False):
    if not ignore_array and ast.array:
        return "[{size} x {type}]".format(size=ast.max_array_size(), type=get_llvm_type(ast, ignore_array=True))
    return "i8" + ("*" * ast.ptr)


def llvm_type_v_float(ast, ignore_array=False):
    if not ignore_array and ast.array:
        return "[{size} x {type}]".format(size=ast.max_array_size(), type=get_llvm_type(ast, ignore_array=True))
    return "float" + ("*" * ast.ptr)


def llvm_type_v_int(ast, ignore_array=False):
    if not ignore_array and ast.array:
        return "[{size} x {type}]".format(size=ast.max_array_size(), type=get_llvm_type(ast, ignore_array=True))
    return "i32" + ("*" * ast.ptr)


def llvm_default_variable(ast):
    # The llvm code for a variable will only be generated if the parent is a statement sequence,
    # because then we will have to allocate the variable

    if isinstance(ast.parent, StatementSequence) and \
            not ast.parent.symbol_table.get_symbol_table(ast.value)[ast.value].llvm_defined and \
            not ast.parent.symbol_table.is_global(ast.value):
        # Allocate the variable
        create_var = "\t{variable} = alloca {llvm_type}, align {align}\n".format(
            variable=variable(ast, store=True),
            llvm_type=get_llvm_type(ast),
            align=ast.get_align())
        llvm.output += create_var
        ast.parent.symbol_table.get_symbol_table(ast.value)[ast.value].llvm_defined = True


from src.LLVM.LLVM import llvm, llvm_code, variable, get_llvm_type
from src.Node.Variable import Variable, StatementSequence, VChar, VFloat, VInt
# from src.LLVM.LLVM import *
