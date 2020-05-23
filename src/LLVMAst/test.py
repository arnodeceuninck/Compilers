from src.Dot.dot import dot
import sys
from gen_llvm import llvmLexer, llvmParser
from src.LLVMAst.LLVMAst_utils import *
# import gen_llvm.llvmLexer
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from src.LLVMAst.LLVMListener import LLVMListener

input_stream = FileStream(sys.argv[1])
lexer = llvmLexer.llvmLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = llvmParser.llvmParser(stream)
tree = parser.start_rule()
customListener = LLVMListener()
walker = ParseTreeWalker()
walker.walk(customListener, tree)
javaForLife = customListener.trees[0]
make_llvm_ast(javaForLife)
dot(javaForLife, "output/llvm_tree.dot")
