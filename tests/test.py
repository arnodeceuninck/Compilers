import unittest
import filecmp
from src.main import compile
from src.AST import AST
from src.Node import *


class MyTestCase(unittest.TestCase):
    def compare(self, file1, file2):
        # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        file1 = open(file1)
        file2 = open(file2)
        self.assertListEqual(list(file1), list(file2))
        file1.close()
        file2.close()

    def helper_test_c(self, test_name: str, cmp=False, fold=False):
        input_file: str = "input/" + test_name + ".c"
        output_file: str = "output/" + test_name + ".dot"
        output_file_folded: str = "output/" + test_name + ".folded.dot"
        expected_output_file: str = "expected_output/" + test_name + ".dot"
        expected_output_file_folded: str = "expected_output/" + test_name + ".folded.dot"

        tree: AST = compile(input_file)
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
        self.helper_test_c("logicop")
        pass

    def test_unop_num(self):
        self.helper_test_c("unop_num")
        pass

    # def test_div_zero(self):
    #     self.helper_test_c("div_zero")
    #     pass


if __name__ == '__main__':
    unittest.main()
