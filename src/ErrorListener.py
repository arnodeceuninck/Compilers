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
        self.variable = variable

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " already declared"


class ConstError(CompilerError):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " is const and can't be assigned after declaration"


class UndeclaredVariableError(CompilerError):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def __str__(self):
        return "[ERROR] Variable " + self.variable + " hasn't been declared yet"


class IncompatibleTypesError(CompilerError):
    def __init__(self, ltype, rtype):
        super().__init__()
        self.ltype = ltype
        self.rtype = rtype

    def __str__(self):
        return "[ERROR] Type " + self.ltype + " is incompatible with " + self.rtype


class RerefError(CompilerError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[ERROR] trying to rereference something that's not a pointer"


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
