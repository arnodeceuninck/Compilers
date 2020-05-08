def color(ast):
    if isinstance(ast, (Operator, LLVMOperation, LLVMAssignment, LLVMStore)):
        return "#87f5ff"
    elif isinstance(ast, (Function, LLVMFunctionUse, LLVMFunction)):
        return "#ff6486"
    elif isinstance(ast, (Arguments, LLVMArgumentList, LLVMArgument)):
        return "#ff6486"
    elif isinstance(ast, Include):
        return "#000000"
    elif isinstance(ast, Comments):
        return "#38A038"
    elif isinstance(ast, (Constant, LLVMConst)):
        return "#ffd885"
    elif isinstance(ast, ReservedType):
        return "#adff76"
    elif isinstance(ast, (Variable, LLVMVariable, LLVMLabel)):
        return "#af93ff"
    elif isinstance(ast, LLVMBranch):
        return "#e09957"
    elif isinstance(ast, (LLVMLoad, LLVMAllocate)):
        return "#fdee37"
    else:
        return "#9f9f9f"

from src.Node.AST import Operator, Function, Arguments, Include, Comments, Constant, ReservedType, Variable
from src.LLVMAst.LLVMAst import *