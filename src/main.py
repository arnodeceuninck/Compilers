import sys
from antlr4 import *
from gen import cLexer
from gen import cParser
from src.customListener import customListener
from src.ErrorListener import CustomErrorListener
from src.ErrorListener import CompilerError, ConstError, IncompatibleTypesError
from src.Node.AST import dot, Variable, AST, Assign, Binary, Print, Unary, VInt, VFloat, VChar, to_LLVM


def assignment(ast):
    # Check whether any other symbol is already in the symbol table

    if isinstance(ast, Variable) and ast.parent and isinstance(ast.parent, Assign):
        # return not required here, but otherwise pycharm thinks the statement is useless
        return ast.symbol_table[ast.value]  # Raises an error if not yet declared

    # Add symbol to symbol table
    if ast.value == "=" and ast.declaration:
        # improve type without constant and ptr
        location = ast.children[0].value
        type = ast.children[0]
        ast.symbol_table.insert(location, type)

    if isinstance(ast, Variable) and ast.parent and not (
            isinstance(ast.parent, Assign) or isinstance(ast.parent, Print) or isinstance(ast.parent,
                                                                                                    Unary) or isinstance(
        ast.parent, Binary)):
        location = ast.value
        type = ast
        ast.symbol_table.insert(location, type)


def convertVar(ast):
    if not isinstance(ast, Variable):
        return
    if isinstance(ast, Print):
        return
    element = ast.symbol_table[ast.value].type
    if element.get_type() == 'int':
        ast_new = VInt(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast.parent.replace_child(ast, ast_new)
    elif element.get_type() == 'float':
        ast_new = VFloat(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast.parent.replace_child(ast, ast_new)
    elif element.get_type() == 'char':
        ast_new = VChar(ast.value)
        ast_new.const = element.const
        ast_new.ptr = element.ptr
        ast.parent.replace_child(ast, ast_new)


def checkAssigns(ast):
    # Check for const assigns
    # On assignments that are declarations, but the leftmost child is a const variable
    if isinstance(ast, Assign) and ast.children[0].const and not ast.declaration:
        raise ConstError(ast.children[0].value)
    if isinstance(ast, Assign):
        type_lvalue = ast.children[0].get_type()
        type_rvalue = ast.children[1].get_type()
        if type_lvalue == type_rvalue:
            pass
        elif type_lvalue == "float" and type_rvalue == "int":
            pass
        else:
            raise IncompatibleTypesError(type_lvalue, type_rvalue)


def compile(input_file: str, catch_error=True) -> AST:
    input_stream = FileStream(input_file)
    lexer = cLexer.cLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = cParser.cParser(stream)
    parser.addErrorListener(CustomErrorListener())
    tree = parser.start_rule()

    if catch_error:
        try:
            return make_ast(tree)
        except CompilerError as e:
            print(str(e))
            return None
    else:
        return make_ast(tree)


def make_ast(tree):
    communismRules = customListener()
    walker = ParseTreeWalker()
    walker.walk(communismRules, tree)
    communismForLife = communismRules.trees[0]
    # TODO: uncomment
    # The two methods of below should be combined in order to make it one pass and apply error checking
    # Create symbol table
    communismForLife.traverse(assignment)
    # # Apply symbol table to all the variables
    communismForLife.traverse(convertVar) # Qua de la fuck does this?
    communismForLife.traverse(checkAssigns)
    return communismForLife


def main(argv):
    communismForLife = compile(argv[1])
    if communismForLife:
        dot(communismForLife, "output/c_tree.dot")
        # communismForLife.constant_folding()
        # dot(communismForLife, "output/c_tree_folded.dot")
        # Creates comments for every assignment, for loop and if statement
        # insert_comments(communismForLife)
        to_LLVM(communismForLife, "output/communismForLife.ll")
        # communismForLife.to_LLVM("output/communismForLife.ll")

        print("Done")
    else:
        print("Had to stop because of an error")


if __name__ == '__main__':
    main(sys.argv)
