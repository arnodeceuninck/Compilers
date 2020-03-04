import sys
from antlr4 import *
from gen import cLexer
from gen import cParser
from AST import AST

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    tree = parser.start_rule()
    our_tree = AST(tree)
    our_tree.simplifyTree()
    our_tree.simplifyTree()
    our_tree.print_dot()

if __name__ == '__main__':
    main(sys.argv)