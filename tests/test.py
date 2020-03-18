import unittest
import filecmp
from src.main import compile
from src.AST import AST




class MyTestCase(unittest.TestCase):
    def helper_test_c(self, test_name: str):
        input_file: str = "input/" + test_name + ".c"
        output_file: str = "output/" + test_name + ".dot"
        output_file_folded: str = "output/" + test_name + ".folded.dot"
        expected_output_file: str = "expected_output/" + test_name + ".dot"
        expected_output_file_folded: str = "expected_output/" + test_name + ".folded.dot"

        tree: AST = compile(input_file)
        tree.print_dot(output_file)
        tree.constant_folding()
        tree.print_dot(output_file_folded)

        # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        self.assertListEqual(list(open(output_file)), list(open(expected_output_file)))
        self.assertListEqual(list(open(output_file_folded)), list(open(expected_output_file_folded)))

    def test_binop_folding(self):
        self.helper_test_c("binop_folding")


if __name__ == '__main__':
    unittest.main()