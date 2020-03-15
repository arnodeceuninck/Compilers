import sys
from antlr4 import *
from gen import cLexer
from gen import cParser
from src.Node import *
from src.customListener import customListener


def assignment(ast):
    if ast.node.value == "=":
        # improve type without constant and ptr
        location = ast.children[0].node.value
        type = ast.children[0].node.type
        value = ast.children[1].node.value
        ast.symbol_table.insert(location, type, value)


def convertVar(ast):
    if type(ast.node) != type(Variable()):
        return
    element = ast.symbol_table.elements[ast.node.value]
    if element.type == 'int':
        ast.node = VInt(ast.node.value)
    elif element.type == 'float':
        ast.node = VFloat(ast.node.value)
    elif element.type == 'char':
        ast.node = VChar(ast.node.value)


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    tree = parser.start_rule()
    communismRules = customListener()
    walker = ParseTreeWalker()
    walker.walk(communismRules, tree)

    communismForLife = communismRules.trees[0]

    communismForLife.traverse(assignment)
    communismForLife.traverse(convertVar)
    communismForLife.print_dot("output/c_tree.dot")
    # communismForLife.constant_folding()
    # communismForLife.print_dot("c_tree_folded.dot")

    print("Done")


if __name__ == '__main__':
    main(sys.argv)
