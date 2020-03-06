# Generated from /home/basil/PycharmProject/Compilers/c.g4 by ANTLR 4.8
from antlr4 import *
from AST import AST

if __name__ is not None and "." in __name__:
    from .cParser import cParser
else:
    from cParser import cParser


# This class defines a complete generic visitor for a parse tree produced by cParser.

class cVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by cParser#start_rule.
    def visitStart_rule(self, ctx: cParser.Start_ruleContext):
        return ctx.getChild(0).accept(self)

    # Visit a parse tree produced by cParser#operation.
    def visitOperation(self, ctx: cParser.OperationContext):

        return ctx.getChild(0).accept(self)

    # Visit a parse tree produced by cParser#operation_logic_or.
    def visitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        node = AST()
        if ctx.LOR:
            node.value = '||'
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_logic_and.
    def visitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        node = AST()
        if ctx.LAND:
            node.value = '&&'
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_compare_eq_neq.
    def visitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        node = AST()
        if ctx.EQ:
            node.value = '=='
        elif ctx.NEQ:
            node.value = '!='
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def visitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        node = AST()
        if ctx.LEQ:
            node.value = '<='
        elif ctx.GEQ:
            node.value = '>='
        elif ctx.GT:
            node.value = '>'
        elif ctx.LT:
            node.value = '<'
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_plus_minus.
    def visitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        node = AST()
        if ctx.PLUS:
            node.value = '+'
        elif ctx.MIN:
            node.value = '-'
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_mult_div.
    def visitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        node = AST()
        if ctx.MULT:
            node.value = '*'
        elif ctx.DIV:
            node.value = '/'
        elif ctx.MOD:
            node.value = '%'
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def visitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        node = AST()
        if ctx.PLUS:
            node.value = '+'
        elif ctx.MIN:
            node.value = '-'
        elif ctx.NOT:
            node.value = '!'
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#operation_brackets.
    def visitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        return ctx.getChild(1).accept(self)

    # Visit a parse tree produced by cParser#identifier.
    def visitIdentifier(self, ctx: cParser.IdentifierContext):
        return AST(ctx.getText())


del cParser
