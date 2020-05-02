def llvm_operate(ast):
    llvm_default_operate(ast)


def llvm_type_operate(ast):
    if isinstance(ast, Binary):
        return llvm_type_binary(ast)
    elif isinstance(ast, Unary):
        return llvm_type_unary(ast)
    else:
        return llvm_type_default_operate(ast)


def llvm_type_binary(ast):
    if get_llvm_type(ast.children[0]) == get_llvm_type(ast.children[1]):
        return get_llvm_type(ast.children[0])
    else:
        return None


def llvm_type_default_operate(ast):
    type = get_llvm_type(ast.children[0])
    for child in ast.children:
        if get_llvm_type(child) != type:
            return None
    return type


def llvm_default_operate(ast):
    llvm_code(ast[0])
    llvm_code(ast[1])

    output = ast.comments()

    llvm_type = get_llvm_type(ast)

    result = variable(ast)
    # If the parent is a bool class entity then we need to store the code into a temporary variable and then convert it
    if isinstance(ast.parent, BoolClasses):
        result = ast.get_temp()

    code = ast.get_llvm_template()
    code = code.format(result=result, type=llvm_type, lvalue=variable(ast[0]),
                       rvalue=variable(ast[1]))

    output += code

    # We need to convert this node into a bool type (i1), because the node above it is an if statement
    if isinstance(ast.parent, BoolClasses):
        constant_type = Constant().create_constant(ast.get_type())
        type_to_bool = constant_type.convert_template("bool")
        type_to_bool = type_to_bool.format(result=variable(ast), value=result)
        output += type_to_bool

    llvm.output += output


from src.LLVM.LLVM import llvm_code, llvm, variable, get_llvm_type
from src.Node.Operate import Operate, BoolClasses, Constant, Binary
from src.Node.Unary import Unary
from src.LLVM.Unary import llvm_type_unary
# from src.LLVM.LLVM import *
