
def llvm_constant(ast):
    if isinstance(ast, CArray):
        llvm_c_array(ast)
    elif isinstance(ast, CChar):
        llvm_c_char(ast)
    else:
        llvm_default_constant(ast)

def llvm_default_constant(ast):
    output = ast.comments()
    code = ast.get_llvm_template()

    # Get the result of the result in the case the parent being an if statement then we need to store
    # it into a temporary variable in order to convert the result to i1 afterwards
    result = variable(ast)
    if isinstance(ast.parent, BoolClasses):
        result = ast.get_temp()

    code = code.format(result=result, type=ast.get_llvm_type(), lvalue=ast.value,
                       rvalue=ast.get_neutral())
    # Convert the constant into a i1 if the parent is an if statement
    if isinstance(ast.parent, BoolClasses):
        type_to_bool = ast.convert_template("bool")
        type_to_bool = type_to_bool.format(result=variable(ast), value=result)
        code += type_to_bool

    output += code
    llvm.output += output

def llvm_c_array(ast):
    raise Exception("Constant Array not (yet?) supported")

def llvm_c_char(ast):
    output = ast.comments()
    code = ast.get_llvm_template()
    code = code.format(result=variable(ast), type=ast.get_llvm_type(), lvalue=str(ord(ast.value)),
                       rvalue=ast.get_neutral())
    output += code
    llvm.output += output

def llvm_c_string(ast):
    # We need to prepend the variable to the AST output llvm code
    temp_llvm_code = llvm.output
    llvm.output = stringVar.format(string_id=ast.variable(True)[2:],
                                       string_len=str(ast.get_llvm_string_len(ast.value) + 1),
                                       string_val=ast.value + "\\00")
    llvm.output += temp_llvm_code

from src.LLVM.LLVM import llvm_code, llvm, variable
from src.Node.Constant import CArray, CChar, BoolClasses, stringVar, Constant
# from src.LLVM.LLVM import *
