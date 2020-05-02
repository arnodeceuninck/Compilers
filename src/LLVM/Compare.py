

def llvm_compare(ast):
    if isinstance(ast, LogicAnd):
        llvm_logic_and(ast)
    else:
        llvm_default_compare(ast)

def llvm_default_compare(ast):
    llvm_code(ast[0])
    llvm_code(ast[1])

    output = ast.comments()

    llvm_type = get_llvm_type(ast)

    # We need to have the variable in order to have the correct translation when the parrent is the BoolClasses
    # because we do not want to extend the i1 we have to keep it that way
    if isinstance(ast.parent, BoolClasses):
        temp = variable(ast, ast.id())
    else:
        temp = ast.get_temp()

    comp_output = ast.get_llvm_template()

    comp_output = comp_output.format(result=temp, type=llvm_type,
                                     lvalue=variable(ast[0]),
                                     rvalue=variable(ast[1]))

    output += comp_output

    # if the parent is an if statement then do not convert the variable
    if isinstance(ast.parent, BoolClasses):
        llvm.output += output
        return
    # Now convert the output (i1) we got to the type we need
    bool_to_type = CBool.convert_template(ast.get_type())
    bool_to_type = bool_to_type.format(result=variable(ast, ast.id()), value=temp)

    output += bool_to_type

    llvm.output += output

def llvm_logic_and(ast):
    llvm_code(ast[0])
    llvm_code(ast[1])

    output = ast.comments()

    llvm_type = get_llvm_type(ast)

    temp1 = ast.get_temp()
    # We need to have the variable in order to have the correct translation when the parrent is the BoolClasses
    # because we do not want to extend the i1 we have to keep it that way
    if isinstance(ast.parent, BoolClasses):
        temp2 = variable(ast, ast.id())
    else:
        temp2 = ast.get_temp()

    comp_output = ast.get_llvm_template()

    comp_output = comp_output.format(result_temp=temp1, type=llvm_type,
                                     lvalue=variable(ast[0]),
                                     rvalue=variable(ast[1]), result=temp2)

    output += comp_output

    # if the parent is an if statement then do not convert the variable
    if isinstance(ast.parent, BoolClasses):
        llvm.output += output
        return
    # Now convert the output (i1) we got to the type we need
    bool_to_type = CBool.convert_template(ast.get_type())
    bool_to_type = bool_to_type.format(result=variable(ast), value=temp2)

    output += bool_to_type

    llvm.output += output

from src.LLVM.LLVM import llvm_code, llvm, variable, get_llvm_type
from src.Node.Compare import LogicAnd, Compare, BoolClasses, CBool
# from src.LLVM.LLVM import *