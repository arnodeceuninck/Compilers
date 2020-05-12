import sys

from src.ErrorListener import CompilerError
from src.Node.AST_utils import dot, compile
from src.LLVMAst.LLVMAst_utils import compile_llvm
from src.LLVM.LLVM import to_LLVM


def main(argv):
    # try:
    javaForLife = compile(argv[1])
    if javaForLife:
        dot(javaForLife, "output/c_tree.dot")
        javaForLife.constant_folding()
        dot(javaForLife, "output/c_tree_folded.dot")
        # Creates comments for every assignment, for loop and if statement
        # insert_comments(communismForLife)
        to_LLVM(javaForLife, "output/compiled.ll")

        # We now convert this llvm to mips by using the previously generated llvm code
        llvmForLife = compile_llvm("output/compiled.ll", "output/compiled.asm", debug_dot=True)
        dot(llvmForLife, "output/llvm_tree.dot")
        print("Done")
    else:
        print("Had to stop because of an error")
    # except CompilerError as e:
    #     print(str(e))
    # except:
    #     print(str(sys.exc_info()[0]))


if __name__ == '__main__':
    main(sys.argv)
