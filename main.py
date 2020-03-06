import sys
from antlr4 import *
from gen import cLexer
from gen import cParser
from AST import AST
from gen.cVisitor import cVisitor

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    tree = parser.start_rule()
    communismRules = cVisitor().visitStart_rule(tree)

if __name__ == '__main__':
    main(sys.argv)