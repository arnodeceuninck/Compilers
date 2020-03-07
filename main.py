import sys
from antlr4 import *
from gen import cLexer
from gen import cParser
from AST import AST
from customVisitor import customVisitor
from customListener import customListener

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

    communismForLife.print_dot("c_tree.dot")

    communismForLife.constant_folding()
    communismForLife.print_dot("c_tree_folded.dot")

    print("Done")

if __name__ == '__main__':
    main(sys.argv)