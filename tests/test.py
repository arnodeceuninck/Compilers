import unittest
# from src.main import compile
from src.Node.AST import AST, to_LLVM, dot, compile
# from src.ErrorListener import *


class MyTestCase(unittest.TestCase):
    def compare(self, file1, file2):
        # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        file1 = open(file1)
        file2 = open(file2)
        self.assertListEqual(list(file1), list(file2))
        file1.close()
        file2.close()

    def helper_test_c(self, test_name: str, cmp=False, fold=False, catch_errors=True):
        # Reset node id because it causes errors in llvm creation
        AST.reset()

        input_file: str = "input/" + test_name + ".c"
        output_file: str = "output/" + test_name + ".dot"
        output_file_ll: str = "output/" + test_name + ".ll"
        output_file_folded: str = "output/" + test_name + ".folded.dot"
        output_file_folded_ll: str = "output/" + test_name + ".folded.ll"
        expected_output_file: str = "expected_output/" + test_name + ".dot"
        expected_output_file_ll: str = "expected_output/" + test_name + ".ll"
        expected_output_file_folded: str = "expected_output/" + test_name + ".folded.dot"
        expected_output_file_folded_ll: str = "expected_output/" + test_name + ".folded.ll"

        tree: AST = compile(input_file, catch_error=catch_errors)
        if tree:
            dot(tree, output_file)
            if fold and not cmp:
                tree.constant_folding()
                dot(tree, output_file_folded)
        else:
            print("No tree generated")

        if cmp:
            # insert_comments(tree)  # Generate comments for LLVM
            to_LLVM(tree, output_file_ll)
            self.compare(output_file, expected_output_file)
            self.compare(output_file_ll, expected_output_file_ll)
            if fold:
                tree.constant_folding()
                # insert_comments(tree)  # Generate comments for LLVM
                dot(tree, output_file_folded)
                self.compare(output_file_folded, expected_output_file_folded)
                to_LLVM(tree, output_file_folded_ll)
                self.compare(output_file_folded_ll, expected_output_file_folded_ll)

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
            self.assertEqual(len(child[0].children), 0)  # Must be removed after folding
            self.assertEqual(len(child[1].children), 0)
            self.assertEqual(child[0].type, "int")  # Must stay the same after folding
            self.assertTrue(isinstance(child[1], CInt))  # Type must be changed
        self.assertEqual(tree[0][1].value, 5)  # Values must match
        self.assertEqual(tree[1][1].value, 63)
        self.assertEqual(tree[2][1].value, 2)
        self.assertEqual(tree[3][1].value, 2)

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
        int_type = [i * 3 for i in range(4)]
        for i in int_type:
            self.assertTrue(isinstance(tree.children[i].node, VInt))

        # Check all float types
        float_type = [i + 1 for i in int_type]
        for i in float_type:
            self.assertTrue(isinstance(tree.children[i].node, VFloat))

        # Check all char types
        char_type = [i + 2 for i in int_type]
        for i in char_type:
            self.assertTrue(isinstance(tree.children[i].node, VChar))

        const = [3, 4, 5, 9, 10, 11]
        ptr = [6, 7, 8, 9, 10, 11]
        for i in range(len(tree.children)):
            self.assertEqual(tree.children[i].node.ptr, i in ptr)
            self.assertEqual(tree.children[i].node.const, i in const)
        pass

    def test_logicop(self):
        # Tests whether the folding has been done right
        tree = self.helper_test_c("logicop", fold=True, cmp=True)
        self.assertEqual(float(tree.children[0].children[1].node.value), 0)  # Values must match
        self.assertEqual(float(tree.children[1].children[1].node.value), 0)
        self.assertEqual(float(tree.children[2].children[1].node.value), 1)
        self.assertEqual(float(tree.children[3].children[1].node.value), 1)
        self.assertEqual(float(tree.children[4].children[1].node.value), 1)
        self.assertEqual(float(tree.children[5].children[1].node.value), 0)
        pass

    def test_unop_num(self):
        # Tests whether the unary operations on numbers (not logical) are successfully folded
        tree = self.helper_test_c("unop_num", fold=True, cmp=True)
        self.assertEqual(float(tree.children[0].children[1].node.value), 1)  # Values must match
        self.assertEqual(float(tree.children[1].children[1].node.value), -1)
        pass

    def test_operator_precedence_folding(self):
        # Tests whether the folding has been done right
        tree = self.helper_test_c("operator_precedence_folding", fold=True, cmp=True)
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
            tree = self.helper_test_c("ptr_test", catch_errors=False, cmp=True)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_comparisions(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("comparisions", catch_errors=False, cmp=True)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_types(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("types", catch_errors=False, cmp=True)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    # Sets cause inconsistent output need to find a fix
    def test_const_printf(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("const_printf", catch_errors=False, cmp=True)
        except CompilerError:
            # There shouldn't be any errors
            self.assertTrue(False)

    def test_if(self):
        # Tests whether the folding has been done right
        try:
            tree = self.helper_test_c("if", catch_errors=False, cmp=True)
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
            self.assertEqual(str(e), "[ERROR] Oh no!! Something went wrong at line 2, column 0: missing ';' at 'yeet'")
        self.assertTrue(error_given)

    # TODO fix test
    def test_div_zero(self):
        self.helper_test_c("div_zero", cmp=True)
        pass

    def test_really_long_var(self):
        tree = self.helper_test_c("long_var", cmp=True)
        # Values must match
        self.assertEqual(tree.children[0].children[0].node.value, "i_am_a_really_long_variable_withCamelCaseInBetween")
        self.assertEqual(tree.children[0].children[1].node.value, 0)

    def test_reref_mult_handling(self):
        tree = self.helper_test_c("mixing_reref_and_mult", cmp=True)
        # Values must match
        self.assertIsInstance(tree.children[2].children[1].node, Mult)
        self.assertIsInstance(tree.children[2].children[1].children[1].node, UReref)

    def test_reref_in_the_mix(self):
        tree = self.helper_test_c("reref_in_the_mix", cmp=True)
        # Values must match
        self.assertIsInstance(tree.children[2].children[1].node, BPlus)
        self.assertIsInstance(tree.children[2].children[1].children[1].node, UReref)

    def test_multiline_code(self):
        tree = self.helper_test_c("multiline_code", cmp=True)
        # Values must match
        self.assertIsInstance(tree.children[0].node, Assign)

    def test_comments(self):
        tree = self.helper_test_c("comments", cmp=True)
        # Values must match
        self.assertIsInstance(tree.children[0].node, Assign)


if __name__ == '__main__':
    unittest.main()
