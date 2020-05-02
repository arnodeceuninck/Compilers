

def llvm_variable(ast):
    llvm_default_variable(ast)

def llvm_default_variable(ast):
    # The llvm code for a variable will only be generated if the parent is a statement sequence,
    # because then we will have to allocate the variable
    
    if isinstance(ast.parent, StatementSequence) and \
            not ast.parent.symbol_table.get_symbol_table(ast.value)[ast.value].llvm_defined and \
            not ast.parent.symbol_table.is_global(ast.value):
        # Allocate the variable
        create_var = "\t{variable} = alloca {llvm_type}, align {align}\n".format(
            variable=variable(ast, store=True),
            llvm_type=ast.get_llvm_type(),
            align=ast.get_align())
        llvm.output += create_var
        ast.parent.symbol_table.get_symbol_table(ast.value)[ast.value].llvm_defined = True

from src.LLVM.LLVM import llvm, llvm_code, variable
from src.Node.Variable import Variable, StatementSequence
# from src.LLVM.LLVM import *