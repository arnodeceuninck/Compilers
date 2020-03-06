# Generated from /home/basil/PycharmProject/Compilers/c.g4 by ANTLR 4.8
from antlr4 import *
from AST import AST

if __name__ is not None and "." in __name__:
    from .cParser import cParser
else:
    from gen.cParser import cParser


# This class defines a complete generic visitor for a parse tree produced by cParser.
class cVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by cParser#start_rule.
    def visitStart_rule(self, ctx: cParser.Start_ruleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_block.
    def visitOperation_block(self, ctx: cParser.Operation_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation.
    def visitOperation(self, ctx: cParser.OperationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_logic_or.
    def visitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_logic_and.
    def visitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_compare_eq_neq.
    def visitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def visitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_plus_minus.
    def visitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        node = AST()
        node.value = "+"
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_mult_div.
    def visitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def visitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by cParser#operation_brackets.
    def visitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        return self.visitChildren(ctx)


del cParser
