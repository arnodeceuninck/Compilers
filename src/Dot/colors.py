def color(ast):
    if isinstance(ast, Operator):
        return "#87f5ff"
    elif isinstance(ast, Function):
        return "#ff6486"
    elif isinstance(ast, Arguments):
        return "#ff6486"
    elif isinstance(ast, Include):
        return "#000000"
    elif isinstance(ast, Comments):
        return "#38A038"
    elif isinstance(ast, Constant):
        return "#ffd885"
    elif isinstance(ast, ReservedType):
        return "#adff76"
    elif isinstance(ast, Variable):
        return "#af93ff"
    else:
        return "#9f9f9f"

from src.Node.AST import Operator, Function, Arguments, Include, Comments, Constant, ReservedType, Variable