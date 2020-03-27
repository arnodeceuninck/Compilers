import unittest
import filecmp
from src.main import compile
from src.AST import AST
from src.Node import *
from src.ErrorListener import *


class MyTestCase(unittest.TestCase):
    def compare(self, file1, file2):
        # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        file1 = open(file1)
        file2 = open(file2)
        self.assertListEqual(list(file1), list(file2))
        file1.close()
        file2.close()

    def helper_test_c(self, test_name: str, cmp=False, fold=False, catch_errors=True):
        input_file: str = "input/" + test_name + ".c"
        output_file: str = "output/" + test_name + ".dot"
        output_file_folded: str = "output/" + test_name + ".folded.dot"
        expected_output_file: str = "expected_output/" + test_name + ".dot"
        expected_output_file_folded: str = "expected_output/" + test_name + ".folded.dot"

        tree: AST = compile(input_file, catch_error=catch_errors)
        if tree:
            tree.to_dot(output_file)
            if fold:
                tree.constant_folding()
                tree.to_dot(output_file_folded)
        else:
            print("No tree generated")

        if cmp:
            self.compare(output_file, expected_output_file)
            if fold:
                self.compare(output_file_folded, expected_output_file_folded)

        return tree

    def test_binop_folding(self):
        # Test whether binop folding gives the correct answers and removes all additional subtrees
        tree = self.helper_test_c("binop_folding", fold=True)
        # self.assertEqual(len(tree.children), 4)
        # self.assertEqual(tree.node.value, "Statement Sequence")
        for child in tree.children:
            # self.assertEqual(child.node.value, "=")
            # self.assertTrue(isinstance(child.node, Assign))
            # self.assertTrue(child.node.declaration)
            self.assertEqual(len(child.children), 2)
            self.assertEqual(len(child.children[0].children), 0)  # Must be removed after folding
            self.assertEqual(len(child.children[1].children), 0)
            self.assertEqual(child.children[0].node.type, "float")  # Must stay the same after folding
            self.assertTrue(isinstance(child.children[1].node, CInt))  # Type must be changed
        self.assertEqual(float(tree.children[0].children[1].node.value), 5)  # Values must match
        self.assertEqual(float(tree.children[1].children[1].node.value), 63)
        self.assertEqual(float(tree.children[2].children[1].node.value), 2)
        self.assertEqual(float(tree.children[3].children[1].node.value), 2)
        pass

    def test_declaration(self):
        # Test whether all info from the declaration has been kept
        tree = self.helper_test_c("declaration")
        for child in tree.children:
            # self.assertEqual(child.node.value, "=")
            # self.assertTrue(isinstance(child.node, Assign))
            # self.assertTrue(child.node.declaration)
            self.assertEqual(len(child.children), 0)
            self.assertTrue(isinstance(child.node, Variable))

        # Check all int types
        self.assertTrue(isinstance(tree.children[0].node, VInt))
        self.assertTrue(isinstance(tree.children[3].node, VInt))
        self.assertTrue(isinstance(tree.children[6].node, VInt))
        self.assertTrue(isinstance(tree.children[9].node, VInt))

        # Check all float types
        self.assertTrue(isinstance(tree.children[1].node, VFloat))
        self.assertTrue(isinstance(tree.children[4].node, VFloat))
        self.assertTrue(isinstance(tree.children[7].node, VFloat))
        self.assertTrue(isinstance(tree.children[10].node, VFloat))

        # Check all char types
        self.assertTrue(isinstance(tree.children[2].node, VChar))
        self.assertTrue(isinstance(tree.children[5].node, VChar))
        self.assertTrue(isinstance(tree.children[8].node, VChar))
        self.assertTrue(isinstance(tree.children[11].node, VChar))

        const = [3, 4, 5, 9, 10, 11]
        ptr = [6, 7, 8, 9, 10, 11]
        for i in range(len(tree.children)):
            self.assertEqual(tree.children[i].node.ptr, i in ptr)
            self.assertEqual(tree.children[i].node.const, i in const)
        pass

    def test_logicop(self):
        # Tests whether the folding has been done right
        tree = self.helper_test_c("logicop", fold=True)
        self.assertEqual(float(tree.children[0].children[1].node.value), 0)  # Values must match
        self.assertEqual(float(tree.children[1].children[1].node.value), 0)
        self.assertEqual(float(tree.children[2].children[1].node.value), 1)
        self.assertEqual(float(tree.children[3].children[1].node.value), 1)
        self.assertEqual(float(tree.children[4].children[1].node.value), 1)
        self.assertEqual(float(tree.children[5].children[1].node.value), 0)
        pass

    def test_unop_num(self):
        # Tests whether the unary operations on numbers (not logical) are successfully folded
        tree = self.helper_test_c("unop_num", fold=True)
        self.assertEqual(float(tree.children[0].children[1].node.value), 1)  # Values must match
        self.assertEqual(float(tree.children[1].children[1].node.value), -1)
        pass

    def test_operator_precedence_folding(self):
        # Tests whether the folding has been done right
        tree = self.helper_test_c("operator_precedence_folding", fold=True)
        self.assertEqual(float(tree.children[0].children[1].node.value), 6)  # Values must match
        self.assertEqual(float(tree.children[1].children[1].node.value), 3)
        self.assertEqual(float(tree.children[2].children[1].node.value), 13)
        self.assertEqual(float(tree.children[3].children[1].node.value), 1)
        self.assertEqual(float(tree.children[4].children[1].node.value), 69)
        pass

    def test_redeclaration_error(self):
        # Tests whether the folding has been done right
        error_given = False
        try:
            tree = self.helper_test_c("redeclaration_error", catch_errors=False)
        except VariableRedeclarationError as e:
            error_given = True
            self.assertEqual(e.variable, "x")
            self.assertEqual(str(e), "[ERROR] Variable x already declared")
        self.assertTrue(error_given)
        pass

    def test_ptr_test(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("ptr_test", catch_errors=False)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_comparisions(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("comparisions", catch_errors=False)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_types(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("types", catch_errors=False)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_const_printf(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("const_printf", catch_errors=False)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_if(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("if", catch_errors=False)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_const_error(self):
        error = False
        try:
            tree = self.helper_test_c("const_error", catch_errors=False)
        except ConstError as e:
            self.assertEqual(str(e), "[ERROR] Variable x is const and can't be assigned after declaration")
            error = True
        self.assertTrue(error)

    def test_error_undeclared(self):
        # Tests whether the folding has been done right
        error_given = False
        try:
            tree = self.helper_test_c("error_undeclared", catch_errors=False)
        except UndeclaredVariableError as e:
            error_given = True
            self.assertEqual(e.variable, "x")
            self.assertEqual(str(e), "[ERROR] Variable x hasn't been declared yet")
        self.assertTrue(error_given)
        pass

    def test_error_incompatible_types(self):
        # Tests whether the folding has been done right
        error_given = False
        try:
            tree = self.helper_test_c("error_incompatible_types", catch_errors=False)
        except IncompatibleTypesError as e:
            error_given = True
            self.assertEqual(e.ltype, "int")
            self.assertEqual(e.rtype, "float")
            self.assertEqual(str(e), "[ERROR] Type int is incompatible with float")
        self.assertTrue(error_given)
        pass

    def test_error_reref(self):
        # Tests whether the folding has been done right
        error_given = False
        try:
            tree = self.helper_test_c("error_reref", catch_errors=False)
        except RerefError as e:
            error_given = True
            self.assertEqual(str(e), "[ERROR] trying to rereference something that's not a pointer")
        self.assertTrue(error_given)

    def test_error_grammar(self):
        # Tests whether the folding has been done right
        error_given = False
        try:
            tree = self.helper_test_c("error_grammar", catch_errors=False)
        except SyntaxCompilerError as e:
            error_given = True
            self.assertEqual(str(e), "[ERROR] Oh no!! Something went wrong at line 1, column 4: missing ';' at '<EOF>'")
        self.assertTrue(error_given)

    # def test_div_zero(self):
    #     self.helper_test_c("div_zero")
    #     pass

if __name__ == '__main__':
    unittest.main()
