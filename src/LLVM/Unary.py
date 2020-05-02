

def llvm_unary(ast):
    if isinstance(ast, UNot):
        llvm_u_not(ast)
    elif isinstance(ast, ArrayIndex):
        llvm_array_index(ast)
    elif isinstance(ast, Print):
        llvm_print(ast)
    elif isinstance(ast, UReref):
        llvm_u_reref(ast)
    elif isinstance(ast, UDeref):
        llvm_u_deref(ast)
    else:
        llvm_default_unary(ast)

def llvm_default_unary(ast):
    llvm_code(ast[0])

    llvm.output += ast.comments()

    type = ast.get_llvm_type()

    code = ast.get_llvm_template()
    code = code.format(result=variable(ast), type=type, value=variable(ast[0]))

    llvm.output += code

# Da klinkt echt als de brakke versie van "No U"
def llvm_u_not(ast):
    llvm_code(ast[0])

    llvm.output += ast.comments()

    type = ast.get_llvm_type()

    # We need to have the variable in order to have the correct translation when the parrent is the boolclasses
    # because we do not want to extend the i1 we have to keep it that way
    if isinstance(ast.parent, BoolClasses):
        temp = variable(ast, ast.id())
    else:
        temp = ast.get_temp()

    code = ast.get_llvm_template()
    code = code.format(result=temp, type=type, value=variable(ast[0]))
    llvm.output += code

    # if the parent is an if statement then do not convert the variable
    if isinstance(ast.parent, BoolClasses):
        return
    bool_to_type = CBool.convert_template(ast.get_type())
    bool_to_type = bool_to_type.format(result=variable(ast), value=temp)

    llvm.output += bool_to_type

def llvm_array_index(ast):
    llvm.output += ast.comments()

    llvm_code(ast[1])
    llvm_code(ast[0])

    code = ast.get_llvm_template()
    code = code.format(temp=ast.get_temp(), array_type=ast[0].get_llvm_type(), variable=variable(ast[0], store=True),
                       index=variable(ast[1]),
                       result=variable(ast), type=ast[0].get_llvm_type(ignore_array=True),
                       align=ast.get_align(), temp_index=ast.get_temp(), index_type=ast[1].get_llvm_type())

    llvm.output += code

def llvm_print(ast):
    AST.print = True

    # Generate LLVM for the node that needs to be printed
    llvm_code(ast[0])

    llvm.output += ast.comments()

    format_type = ast[0].get_format_type()
    print_type = ast[0].get_llvm_print_type()

    var = variable(ast[0])
    # Because you can't print floats
    if print_type == "double":
        convert_code = ast[0].convert_template("double")
        convert_code = convert_code.format(result=variable(ast), value=variable(ast[0]))
        var = variable(ast)
        llvm.output += convert_code

    print_code = printString.format(format_type=format_type, print_type=print_type, value=variable)
    llvm.output += print_code
    
def llvm_u_deref(ast):
    llvm_code(ast[0])
    variable(ast[0])
    pass  # TODO: fix it

def llvm_u_reref(ast):
    llvm_code(ast[0])
    type = ast.get_llvm_type()

    # Load the value into the ast node
    code = ast.llvm_load_template()
    code = code.format(result=variable(ast), type=type, var=variable(ast[0]))

    llvm.output += code

from src.LLVM.LLVM import llvm_code, llvm, variable
from src.Node.Unary import UNot, ArrayIndex, Unary, Print, UReref, UDeref, BoolClasses, CBool, printString, AST
# from src.LLVM.LLVM import *