import sys
from src.Node.AST import dot, compile, to_LLVM



def main(argv):
    communismForLife = compile(argv[1])
    if communismForLife:
        dot(communismForLife, "output/c_tree.dot")
        communismForLife.constant_folding()
        dot(communismForLife, "output/c_tree_folded.dot")
        # Creates comments for every assignment, for loop and if statement
        # insert_comments(communismForLife)
        to_LLVM(communismForLife, "output/communismForLife.ll")
        print("Done")
    else:
        print("Had to stop because of an error")


if __name__ == '__main__':
    main(sys.argv)
