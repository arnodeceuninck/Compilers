from src.symbolTable import SymbolTable
from src.Dot.colors import color
from src.LLVMAst.LLVMAst import LLVMAst


# Convert given ast into a dotfile and write it to filename
def dot(ast, filename: str):
    output = "Digraph G { \n"

    # Add the symbol table tree
    ast.symbol_table.to_dot(isinstance(ast, LLVMAst))  # TODO: Seperate from symbol table class
    output += ast.symbol_table.dot_output

    # if isinstance(ast, LLVMAst):
    #     output += "rankdir=LR\n"

    output += "subgraph cluster_1 {\n"
    output += "node [style=filled, shape=rectangle, penwidth=2];\n"

    output += dot_node(ast)
    output += dot_connections(ast)

    output += "label = \"AST\";\n"
    output += "}\n"
    output += "}"

    outputFile = open(filename, "w")
    outputFile.write(output)
    outputFile.close()


# Represent the nodes for the dotfile
def dot_node(ast):
    # The output needs to be the id + The label itself
    output = dot_str(ast)
    for child in ast.children:
        output += dot_node(child)
    return output


# represent the connections for the dotfile
def dot_connections(ast):
    output = ""
    for child in ast.children:
        output += str(ast.id()) + " -> " + str(child.id()) + "\n"
        output += dot_connections(child)
    return output


def dot_str(ast):
    value = str(ast)
    value = value.replace('\\', '\\\\')
    value = value.replace('"', '\\"')
    if isinstance(ast, Include):
        value = '<<font color="white">{value}</font>>'.format(value=value)
    else:
        value = "\"{value}\"".format(value=value)
    return '{name}[label={value}, fillcolor="{color}"] \n'.format(name=ast.id(), value=value,
                                                                  color=color(ast))


from src.Node.AST import Include, AST
