from src.LLVM.LLVM import to_LLVM
from src.ErrorListener import *
from src.Node.AST_utils import *
import inspect
import unittest


class SemanticErrorTests(unittest.TestCase):
    def help_test(self, expected_error, expected_message: str):

        # Get the name of the function
        function_name = str(inspect.stack()[1][3])
        test_name = function_name.split('_')[1]

        AST.reset()

        input_file: str = "CompilersBenchmark/SemanticErrors/" + test_name + ".c"
        # Required because some errors only get raised when compiling
        output_file: str = "tests/output/SemanticErrorOutput.ll"

        errored = False
        try:
            tree: AST = compile(input_file, catch_error=False)
            to_LLVM(tree, output_file)
        except expected_error as e:
            errored = True
            self.assertEqual(expected_message, str(e))
        except CompilerError as e:
            print(str(e))
            print(type(e))

        self.assertTrue(errored)

    def test_arrayAccessTypeMismatch(self):
        self.help_test(ArrayIndexError, "[ERROR] Array index must be int")

    def test_arrayAccessTypeMismatch2(self):
        self.help_test(NoArrayError, "[ERROR] Trying to take the index of something that's not an array")

    def test_arrayCompareError(self):
        self.help_test(UnknownOperationError, "[ERROR] Undified operation '==' between 'int*' and 'int*'")

    def test_arraySizeTypeMismatch(self):
        self.help_test(ArrayIndexError, "[ERROR] Array index must be int")

    def test_declarationDeclarationMismatch1(self):
        self.help_test(FunctionRedeclarationError, "[ERROR] Function f already declared")

    def test_declarationDeclarationMismatch2(self):
        self.help_test(FunctionRedeclarationError, "[ERROR] Function f already declared")

    def test_declarationDeclarationMismatch3(self):
        self.help_test(FunctionRedeclarationError, "[ERROR] Function f already declared")

    def test_declarationDefinitionMismatch1(self):
        self.help_test(FunctionWrongDefinedError, "[ERROR] Function f not defined correctly")

    def test_declarationDefinitionMismatch2(self):
        self.help_test(FunctionWrongDefinedError, "[ERROR] Function f not defined correctly")

    def test_declarationDefinitionMismatch3(self):
        self.help_test(FunctionWrongDefinedError, "[ERROR] Function f not defined correctly")

    def test_definitionInLocalScope(self):
        self.help_test(FunctionDefinitionOutOfScope, "[ERROR] Function f defined out of scope")

    def test_dereferenceTypeMismatch1(self):
        # Not allowed because of the grammar
        self.help_test(SyntaxCompilerError,
                       "[ERROR] Oh no!! You've used the wrong syntax at line 2, column 5: "
                       "no viable alternative at input '*5'")

    def test_dereferenceTypeMismatch2(self):
        self.help_test(DerefError, "[ERROR] trying to take the address of something that's not a variable")

    def test_functionCallargumentMismatch1(self):
        self.help_test(CallAmountMismatchError, "[ERROR] Function f expects 2 operators but gets 1 instead")

    def test_functionCallargumentMismatch2(self):
        self.help_test(CallAmountMismatchError, "[ERROR] Function f expects 1 operators but gets 2 instead")

    def test_functionCallargumentMismatch3(self):
        self.help_test(CallAmountMismatchError, "[ERROR] Function printf expects 2 operators but gets 1 instead")

    def test_functionCallargumentMismatch4(self):
        self.help_test(CallAmountMismatchError, "[ERROR] Function printf expects 2 operators but gets 3 instead")

    def test_functionRedefinition1(self):
        self.help_test(FunctionRedefinitionError, "[ERROR] Function f is redefined")

    def test_functionRedefinition2(self):
        self.help_test(FunctionRedefinitionError, "[ERROR] Function f is redefined")

    def test_functionRedefinition3(self):
        self.help_test(FunctionRedefinitionError, "[ERROR] Function f is redefined")

    def test_incompatibleTypes1(self):
        self.help_test(UnknownOperationError, "[ERROR] Undified operation '+' between 'int' and 'char'")

    def test_incompatibleTypes2(self):
        self.help_test(UnknownOperationError, "[ERROR] Undified operation '+' between 'int' and 'char'")

    def test_incompatibleTypes3(self):
        self.help_test(IncompatibleTypesError, "[ERROR] Type int is incompatible with void")

    def test_incompatibleTypes4(self):
        self.help_test(UnknownOperationError, "[ERROR] Undified operation '+' between 'int' and 'int*'")

    def test_incompatibleTypes5(self):
        self.help_test(UnknownOperationError, "[ERROR] Undified operation '+' between 'char' and 'int'")

    def test_incompatibleTypes6(self):
        self.help_test(IncompatibleFunctionType, "[ERROR] Function printf with type 'string' "
                                                 "is incompatible with 'int'")

    # TODO fix this code
    def test_incompatibleTypes7(self):
        self.help_test(IncompatibleFunctionType, "[ERROR] Function f with type 'int' is incompatible with 'char'")

    def test_invalidIncludeError(self):
        self.help_test(SyntaxCompilerError,
                       "[ERROR] Oh no!! You've used the wrong syntax at line 1, column 26: missing ';' at 'h'")

    def test_invalidLoopControlStatement(self):
        self.help_test(ReservedVariableOutOfScope, "[ERROR] The reserved variable 'continue' used is out of scope")

    # This test should fail
    def test_invalidUnaryOperation(self):
        # Unsupported '++'
        self.help_test(RerefError, "")

    def test_mainNotFound(self):
        self.help_test(MainNotFoundError, "[ERROR] Main not found")

    def test_parameterRedefinition1(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable a already defined")

    def test_parameterRedefinition2(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable a already defined")

    def test_parameterRedefinition3(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable a already defined")

    def test_pointerOperationError(self):
        self.help_test(UnknownOperationError, "[ERROR] Undified operation '+' between 'int*' and 'int*'")

    def test_returnOutsideFunction(self):
        self.help_test(ReservedVariableOutOfScope, "[ERROR] The reserved variable 'return' used is out of scope")

    def test_returnTypeMismatch(self):
        self.help_test(ReturnValueError, "[ERROR] Undefined return of 'int': expected 'void'")

    def test_undeclaredFunction(self):
        self.help_test(FunctionUndefinedError, "[ERROR] Function f not defined")

    def test_undeclaredVariable1(self):
        self.help_test(UndeclaredVariableError, "[ERROR] Variable x hasn't been declared yet")

    def test_undeclaredVariable2(self):
        self.help_test(UndeclaredVariableError, "[ERROR] Variable x hasn't been declared yet")

    def test_undeclaredVariable3(self):
        self.help_test(UndeclaredVariableError, "[ERROR] Variable x hasn't been declared yet")

    def test_variableRedefinition1(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable x already defined")

    def test_variableRedefinition2(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable x already defined")

    def test_variableRedefinition3(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable x already defined")

    def test_variableRedefinition4(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable x already defined")

    def test_variableRedefinition5(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable x already defined")

    def test_variableRedefinition6(self):
        self.help_test(VariableRedefinitionError, "[ERROR] Variable x already defined")


if __name__ == '__main__':
    unittest.main()
