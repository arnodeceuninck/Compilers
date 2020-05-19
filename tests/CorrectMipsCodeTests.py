import unittest

from src.Node.AST_utils import *
from src.LLVMAst.LLVMAst_utils import compile_llvm, LLVMAst, SymbolTable
from src.ErrorListener import *
import inspect
import unittest
import subprocess
from src.LLVM.LLVM import to_LLVM


class CorrectMipsCodeTests(unittest.TestCase):
    def help_compare(self, file1, file2):
        # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
        file1 = open(file1)
        file2 = open(file2)

        # This function is written to ignore the extra zero's added behind a decimal point
        # Ahh yess, love the O(n^2)
        i = -1
        j = -1
        for line1 in file1:
            i += 1
            for line2 in file2:
                j += 1
                if i != j:
                    continue
                if line1 == line2:
                    continue
                if not "." in line1 and not "." in line2: # zero check is only for decimals
                    print(line1)
                    print(line2)
                    self.assertTrue(False)
                ii = -1
                ji = -1
                while ii < len(line1)-1 and ji < len(line2)-1:
                    ii += 1
                    ji += 1
                    if line1[ii] == line2[ji]:
                        continue
                    if line1[ii] == "0":
                        ji -= 1
                    elif line2[ji] == "0":
                        ii -= 1
                    else:
                        print(line1)
                        print(line2)
                        self.assertTrue(False)
            j = -1
        i = -1

        self.assertEqual(i, j)

        self.assertListEqual(list(file1), list(file2))
        file1.close()
        file2.close()

    def help_test(self):
        # Get the name of the function
        function_name = str(inspect.stack()[1][3])
        test_name = function_name.split('_')[1]

        AST.reset()
        # LLVMAst.reset()
        SymbolTable.reset()

        input_file: str = "CompilersBenchmark/CorrectCode/" + test_name + ".c"
        temp_file: str = "tests/output/CorrectCodeOutput.ll"
        output_file: str = "tests/output/CorrectMipsCodeOutput.asm"  # Required because some errors only get raised when compiling
        code_output: str = "tests/output/code_mips_result.txt"

        # Get the clang output
        clang_executable = "tests/output/clang_code"
        clang_output: str = "tests/output/clang_result.txt"

        pass_arg = ["sh", "tests/clang_compile.sh", input_file, clang_executable, clang_output]
        return_code = subprocess.call(pass_arg)
        expected_return_code = subprocess.call(pass_arg)

        # Get the output from our compiler
        tree: AST = compile(input_file, catch_error=False)
        # tree.constant_folding()
        to_LLVM(tree, temp_file)
        compile_llvm(temp_file, output_file, debug_dot=True)

        pass_arg = ["sh", "tests/CorrectMipsCode.sh", output_file, code_output]
        return_code = subprocess.call(pass_arg)

        # Check the outputs
        self.help_compare(clang_output, code_output)
        # self.assertEqual(expected_return_code, return_code)
        # TODO: can we get terminal return codes in MIPS?
        # Yup, it's possible with syscall 17:
        # exit2(terminate with value)
        # ----------------------------
        # $v0 = 17
        # $a0 = termination result

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

    # def test_y(self):
    #     self.help_test()


if __name__ == '__main__':
    unittest.main()
