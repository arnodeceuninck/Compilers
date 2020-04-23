from test import *
from src.ErrorListener import *
import inspect
import unittest
import subprocess


class CorrectCodeTests(unittest.TestCase):
    def help_compare(self, file1, file2):
        # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        file1 = open(file1)
        file2 = open(file2)
        self.assertListEqual(list(file1), list(file2))
        file1.close()
        file2.close()

    def help_test(self):
        # Get the name of the function
        function_name = str(inspect.stack()[1][3])
        test_name = function_name.split('_')[1]

        AST.reset()

        input_file: str = "../CompilersBenchmark/CorrectCode/" + test_name + ".c"
        output_file: str = "output/CorrectCodeOutput.ll"  # Required because some errors only get raised when compiling
        code_output: str = "output/code_result.txt"

        # Get the clang output
        clang_executable = "output/clang_code"
        clang_output: str = "output/clang_result.txt"

        pass_arg = ["sh", "clang_compile.sh", input_file, clang_executable, clang_output]
        return_code = subprocess.call(pass_arg)
        expected_return_code = subprocess.call(pass_arg)

        # Get the output from our compiler
        tree: AST = compile(input_file, catch_error=False)
        # tree.constant_folding()
        to_LLVM(tree, output_file)

        pass_arg = ["sh", "CorrectCode.sh", output_file, code_output]
        return_code = subprocess.call(pass_arg)

        # Check the outputs
        self.help_compare(clang_output, code_output)
        self.assertEqual(expected_return_code, return_code)

    def test_binaryOperations1(self):
        self.help_test()

    def test_binaryOperations2(self):
        self.help_test()

    def test_breakAndContinue(self):
        # ++ unsupported
        self.help_test()

    def test_comparisons1(self):
        # wrong neutral value for float
        self.help_test()

    def test_comparisons2(self):
        # last number is wrong
        self.help_test()

    def test_dereferenceAssignment(self):
        # ++ not supported
        self.help_test()

    def test_fibonacciRecursive(self):
        # ++ not supported
        return
        self.help_test()

    def test_floatToIntConversion(self):
        self.help_test()

    def test_for(self):
        # ++ not supported
        self.help_test()

    def test_forwardDeclaration(self):
        self.help_test()

    def test_if(self):
        self.help_test()

    def test_ifElse(self):
        self.help_test()

    def test_intToFloatConversion(self):
        self.help_test()

    def test_modulo(self):
        self.help_test()

    def test_pointerArgument(self):
        self.help_test()

    def test_prime(self):
        return
        self.help_test()

    def test_printf1(self):
        self.help_test()

    def test_printf2(self):
        self.help_test()

    def test_printf3(self):
        self.help_test()

    def test_scanf1(self):
        return
        self.help_test()

    def test_scanf2(self):
        return
        self.help_test()

    def test_scoping(self):
        self.help_test()

    def test_unaryOperations(self):
        self.help_test()

    def test_variables1(self):
        self.help_test()

    def test_variables2(self):
        self.help_test()

    def test_variables3(self):
        self.help_test()

    def test_variables4(self):
        self.help_test()

    def test_variables5(self):
        self.help_test()

    def test_variables6(self):
        self.help_test()

    def test_variables7(self):
        self.help_test()

    def test_variables8(self):
        self.help_test()

    def test_while(self):
        self.help_test()
