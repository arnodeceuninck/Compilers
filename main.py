import sys
from antlr4 import *
from gen import cLexer
from gen import cParser


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser(stream)
    tree = parser.start_rule()



if __name__ == '__main__':
    main(sys.argv)