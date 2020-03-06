# Generated from /home/arno/Compilers/c.g4 by ANTLR 4.8
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
        # test = self.visitChildren(ctx)

        c = ctx.getChild(0)
        return c.accept(self)

    # Visit a parse tree produced by cParser#operation_plus_minus.
    def visitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        node = AST()
        print("YEEET")
        if ctx.PLUS:
            node.value = "+"
            print("DETECTED +")
        node.left = self.visit(ctx.left)
        node.right = self.visit(ctx.right)
        return node

    # Visit a parse tree produced by cParser#identifier.
    def visitIdentifier(self, ctx: cParser.IdentifierContext):
        return ctx.getText()


del cParser
