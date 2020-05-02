
def llvm_operate(ast):
    llvm_default_operate(ast)

def llvm_default_operate(ast):
    llvm_code(ast[0])
    llvm_code(ast[1])

    output = ast.comments()

    llvm_type = ast.get_llvm_type()

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

from src.LLVM.LLVM import llvm_code, llvm, variable
from src.Node.Operate import Operate, BoolClasses, Constant
# from src.LLVM.LLVM import *
