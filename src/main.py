import sys
from antlr4 import *
from gen import cLexer
from gen import cParser
from src.Node import *
from src.customListener import customListener
from src.ErrorListener import CustomErrorListener
from src.ErrorListener import CompilerError, ConstError
from src.AST import AST

def assignment(ast):
    if ast.node.value == "=" and ast.node.declaration:
        # improve type without constant and ptr
        location = ast.children[0].node.value
        type = ast.children[0].node
        ast.symbol_table.insert(location, type)


def convertVar(ast):
    if type(Variable()) != type(ast.node):
        return
    if isinstance(ast.node, Print):
        return
    element = ast.symbol_table[ast.node.value].type
    if element.type == 'int':
        ast.node = VInt(ast.node.value)
        ast.node.const = element.const
        ast.node.ptr = element.ptr
    elif element.type == 'float':
        ast.node = VFloat(ast.node.value)
        ast.node.const = element.const
        ast.node.ptr = element.ptr
    elif element.type == 'char':
        ast.node = VChar(ast.node.value)
        ast.node.const = element.const
        ast.node.ptr = element.ptr

def checkConstAssigns(ast: AST):
    # On assignments that are declarations, but the leftmost child is a const variable
    if ast.node.value == "=" and ast.children[0].node.const and not ast.node.declaration:
        raise ConstError(ast.children[0].node.value)

def compile(input_file: str) -> AST:
    input_stream = FileStream(input_file)
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    parser.addErrorListener(CustomErrorListener())
    tree = parser.start_rule()

    try:
        communismRules = customListener()
        walker = ParseTreeWalker()
        walker.walk(communismRules, tree)

        communismForLife = communismRules.trees[0]

        # The two methods of below should be combined in order to make it one pass and apply error checking
        # Create symbol table
        communismForLife.traverse(assignment)
        # Apply symbol table to all the variables
        communismForLife.traverse(convertVar)
        communismForLife.traverse(checkConstAssigns)

        return communismForLife

    except CompilerError as e:
        print(str(e))
        return None


def main(argv):
    communismForLife = compile(argv[1])
    if communismForLife:
        communismForLife.to_dot("output/c_tree.dot")
        communismForLife.constant_folding()
        communismForLife.to_dot("output/c_tree_folded.dot")

        print("Done")
    else:
        print("Had to stop because of an error")

if __name__ == '__main__':
    main(sys.argv)
