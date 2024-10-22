# src: https://stackoverflow.com/questions/32224980/python-2-7-antlr4-make-antlr-throw-exceptions-on-invalid-input/32228598

from antlr4 import *
import sys
from gen.cLexer import cLexer
from gen.cParser import cParser
from antlr4.error.ErrorListener import ErrorListener


class CompilerError(BaseException):
    def __init__(self):
        pass


class VariableRedeclarationError(CompilerError):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable[:-2]

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " already declared"


class VariableRedefinitionError(CompilerError):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable[:-2]

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " already defined"


class ConstError(CompilerError):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable[:-2]

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " is const and can't be assigned after declaration"


class ArrayIndexError(CompilerError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[ERROR] Array index must be int"


class NoArrayError(CompilerError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[ERROR] Trying to take the index of something that's not an array"


class UndeclaredVariableError(CompilerError):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable[:-2]

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " hasn't been declared yet"


class IncompatibleTypesError(CompilerError):
    def __init__(self, ltype, rtype):
        super().__init__()
        self.ltype = ltype
        self.rtype = rtype

    def __str__(self):
        return "[ERROR] Type " + self.ltype + " is incompatible with " + self.rtype


class IncompatibleFunctionType(CompilerError):
    def __init__(self, ltype, rtype, function_name):
        super().__init__()
        self.ltype = ltype
        self.rtype = rtype
        self.function_name = function_name

    def __str__(self):
        return "[ERROR] Function " + self.function_name + " with type '" + self.ltype + "' is incompatible with '" + \
               self.rtype + "'"


class UnknownOperationError(CompilerError):
    def __init__(self, operation, ltype, rtype=None):
        super().__init__()
        self.operation = operation
        self.ltype = ltype
        self.rtype = rtype

    def __str__(self):
        if self.rtype:
            return "[ERROR] Undified operation \'{op}\' between \'{ltype}\' and \'{rtype}\'" \
                .format(op=self.operation, ltype=self.ltype, rtype=self.rtype)
        else:
            return "[ERROR] Undified operation \'{op}\' on \'{ltype}\'" \
                .format(op=self.operation, ltype=self.ltype)


class RerefError(CompilerError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[ERROR] trying to rereference something that's not a pointer"


class DerefError(CompilerError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[ERROR] trying to take the address of something that's not a variable"


class SyntaxCompilerError(CompilerError):
    def __init__(self, row, column, offendingSymbol, msg):
        super().__init__()
        self.row = row
        self.column = column
        self.offendingSymbol = offendingSymbol
        self.msg = msg

    def __str__(self):
        return "[ERROR] Oh no!! You've used the wrong syntax at line " + str(self.row) + ", column " + str(
            self.column) + ": " + self.msg


class ReservedVariableOutOfScope(CompilerError):
    def __init__(self, reserved_value):
        super().__init__()
        self.reserved_value = reserved_value

    def __str__(self):
        return "[ERROR] The reserved variable '{reserved_value}' used is out of scope".format(
            reserved_value=self.reserved_value)


class ExpressionOutOfScope(CompilerError):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def __str__(self):
        return "[ERROR] The expression '{expression}' used is out of scope".format(
            expression=self.expression)


class FunctionRedeclarationError(CompilerError):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return "[ERROR] Function " + self.function + " already declared"


class FunctionUndefinedError(CompilerError):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return "[ERROR] Function " + self.function + " not defined"


class FunctionWrongDefinedError(CompilerError):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return "[ERROR] Function " + self.function + " not defined correctly"


class ReturnValueError(CompilerError):
    def __init__(self, ret_val, expected):
        super().__init__()
        self.ret_val = ret_val
        self.expected = expected

    def __str__(self):
        return "[ERROR] Undefined return of \'{ltype}\': expected \'{rtype}\'" \
            .format(ltype=self.ret_val, rtype=self.expected)


class FunctionDefinitionOutOfScope(CompilerError):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return "[ERROR] Function " + self.function + " defined out of scope"


class CallAmountMismatchError(CompilerError):
    def __init__(self, function, expected_operators, get_operators):
        super().__init__()
        self.function = function
        self.expected_operators = expected_operators
        self.get_operators = get_operators

    def __str__(self):
        return "[ERROR] Function " + self.function + " expects " + str(self.expected_operators) + \
               " operators but gets " + str(self.get_operators) + " instead"


class FunctionRedefinitionError(CompilerError):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return "[ERROR] Function " + self.function + " is redefined"


class MainNotFoundError(CompilerError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[ERROR] Main not found"


class CustomErrorListener(ErrorListener):

    def __init__(self):
        super(CustomErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # print("[ERROR] Oh no!! Something went wrong at line", line, ", column", column, ": ", msg)
        raise SyntaxCompilerError(line, column, offendingSymbol, msg)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print("[ERROR] Oh no!! Ambiguity!")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        print("[ERROR] Oh no!! Attempting Full Context!")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        print("[ERROR] Oh no!! Context Sensitivity!")
