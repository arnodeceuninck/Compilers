# src: https://stackoverflow.com/questions/32224980/python-2-7-antlr4-make-antlr-throw-exceptions-on-invalid-input/32228598

from antlr4 import *
import sys
from gen.cLexer import cLexer
from gen.cParser import cParser
from antlr4.error.ErrorListener import ErrorListener


class CustomErrorListener(ErrorListener):

    def __init__(self):
        super(CustomErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("[ERROR] Oh no!! Something went wrong at line", line, ", column", column, ": ", msg)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print("[ERROR] Oh no!! Ambiguity!")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        print("[ERROR] Oh no!! Attempting Full Context!")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        print("[ERROR] Oh no!! Context Sensitivity!")
