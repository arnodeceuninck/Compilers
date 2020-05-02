


def llvm_reserved_type(ast):
    if isinstance(ast, Break):
        llvm_break(ast)
    elif isinstance(ast, Continue):
        llvm_continue(ast)
    elif isinstance(ast, Return):
        llvm_return(ast)
    elif isinstance(ast, Void):
        llvm_void(ast)
    else:
        raise Exception("Unknown AST")
    pass


def llvm_break(ast):
    llvm.output += ast.comments()

    # The loop in which the user situates itast
    loop = ast
    # Get the loop in which the break situates itast, it can be situated in an if statement
    while not isinstance(loop, (While, For)):
        loop = loop.parent

    # Handle the break
    end_label = "end" + str(loop.id())
    goto(end_label)


def llvm_continue(ast):
    llvm.output += ast.comments()

    # The loop in which the user situates itast
    loop = ast
    # Get the loop in which the break situates itast, it can be situated in an if statement
    while not isinstance(loop, (While, For)):
        loop = loop.parent

    # Handle the continue
    loop_label = "loop" + str(loop.id())
    goto(loop_label)


def llvm_return(ast):
    # If we find that the return has no children then return a void type
    if not ast.children:
        llvm.output += ast.comments()
        llvm.output += "\tret void\n"
        return

    # Generate code for the only child of return
    llvm_code(ast[0])

    llvm.output += ast.comments()

    # The loop in which the user situates itast
    code = "\tret " + get_llvm_type(ast[0]) + " " + variable(ast[0])
    llvm.output += code


def llvm_void(ast):
    pass

from src.LLVM.LLVM import llvm, llvm_code, variable, goto, get_llvm_type
from src.Node.ReservedType import ReservedType, Break, Continue, Return, Void, While, For
# from src.LLVM.LLVM import *