
def llvm_comments(ast):
    if isinstance(ast, SingleLine):
        llvm_single_line(ast)
    elif isinstance(ast, Multiline):
        llvm_multi_line(ast)
    else:
        raise Exception("Unknown AST")


def llvm_single_line(ast):
    code = ";; " + ast.value
    llvm.output += code


def llvm_multi_line(ast):
    code = ""
    for line in ast.code:
        code += ";; " + line
    llvm.output += code

from src.LLVM.LLVM import llvm_code, llvm
from src.Node.Comments import Comments, SingleLine, Multiline
# from src.LLVM.LLVM import *

