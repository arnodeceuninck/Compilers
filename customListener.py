from antlr4 import *
from AST import AST
from gen.cParser import cParser

PREVIOUS_CTX = None

# This class defines a complete listener for a parse tree produced by cParser.
class customListener(ParseTreeListener):

    # Enter a parse tree produced by cParser#start_rule.
    def enterStart_rule(self, ctx: cParser.Start_ruleContext):

        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: cParser.Start_ruleContext):
        print("kaas")
        pass

    # Enter a parse tree produced by cParser#operation.
    def enterOperation(self, ctx: cParser.OperationContext):
        pass

    # Exit a parse tree produced by cParser#operation.
    def exitOperation(self, ctx: cParser.OperationContext):
        pass

    # Enter a parse tree produced by cParser#operation_logic_or.
    def enterOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        pass

    # Exit a parse tree produced by cParser#operation_logic_or.
    def exitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        pass

    # Enter a parse tree produced by cParser#operation_logic_and.
    def enterOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        pass

    # Exit a parse tree produced by cParser#operation_logic_and.
    def exitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        pass

    # Enter a parse tree produced by cParser#operation_compare_eq_neq.
    def enterOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        pass

    # Exit a parse tree produced by cParser#operation_compare_eq_neq.
    def exitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        pass

    # Enter a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def enterOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        pass

    # Exit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def exitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        pass

    # Enter a parse tree produced by cParser#operation_plus_minus.
    def enterOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        pass

    # Exit a parse tree produced by cParser#operation_plus_minus.
    def exitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        pass

    # Enter a parse tree produced by cParser#operation_mult_div.
    def enterOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        pass

    # Exit a parse tree produced by cParser#operation_mult_div.
    def exitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        pass

    # Enter a parse tree produced by cParser#operation_unary_plus_minus_not.
    def enterOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        pass

    # Exit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def exitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        pass

    # Enter a parse tree produced by cParser#operation_brackets.
    def enterOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        pass

    # Exit a parse tree produced by cParser#operation_brackets.
    def exitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        pass

    # Enter a parse tree produced by cParser#identifier.
    def enterIdentifier(self, ctx: cParser.IdentifierContext):
        pass

    # Exit a parse tree produced by cParser#identifier.
    def exitIdentifier(self, ctx: cParser.IdentifierContext):
        pass
