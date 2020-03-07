from antlr4 import *
from AST import AST
from gen.cParser import cParser


# This class defines a complete listener for a parse tree produced by cParser.
class customListener(ParseTreeListener):
    trees = []  # This should be used as a stack
    finalTree = None
    previousTree = None

    def __init__(self):
        self.previousTree = None
        self.finalTree = None

    # Enter a parse tree produced by cParser#start_rule.
    def enterStart_rule(self, ctx: cParser.Start_ruleContext):
        print("enter Start")
        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: cParser.Start_ruleContext):
        print("exit Start")
        self.finalTree = self.previousTree
        pass

    # Enter a parse tree produced by cParser#operation.
    def enterOperation(self, ctx: cParser.OperationContext):
        print("Enter Operation")
        pass

    # Exit a parse tree produced by cParser#operation.
    def exitOperation(self, ctx: cParser.OperationContext):
        print("Exit operation")
        pass

    # Enter a parse tree produced by cParser#operation_logic_or.
    def enterOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        # Check whether there are two children
        if ctx.getChildCount() == 3:
            symbol = ""
            if ctx.LOR():
                symbol = "||"
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_logic_or.
    def exitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        if len(self.trees) > 2:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.value
            if symbol == "||":
                self.binary_op_simplify()
        pass

    # Enter a parse tree produced by cParser#operation_logic_and.
    def enterOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        # Check whether there are two children
        if ctx.getChildCount() == 3:
            symbol = ""
            if ctx.LAND():
                symbol = "&&"
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_logic_and.
    def exitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        if len(self.trees) > 2:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.value
            if symbol == "&&":
                self.binary_op_simplify()
        pass

    # Enter a parse tree produced by cParser#operation_compare_eq_neq.
    def enterOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        # Check whether there are two children
        if ctx.getChildCount() == 3:
            symbol = ""
            if ctx.EQ():
                symbol = "=="
            elif ctx.NEQ():
                symbol = "!="
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_compare_eq_neq.
    def exitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        if len(self.trees) > 2:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.value
            if symbol == "==" or symbol == "!=":
                self.binary_op_simplify()
        pass

    # Enter a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def enterOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        # Check whether there are two children
        if ctx.getChildCount() == 3:
            symbol = ""
            if ctx.LEQ():
                symbol = "<="
            elif ctx.GEQ():
                symbol = ">="
            elif ctx.LT():
                symbol = "<"
            elif ctx.GT():
                symbol = ">"
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def exitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        if len(self.trees) > 2:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.value
            if symbol == "<=" or symbol == ">=" or symbol == "<" or symbol == ">":
                self.binary_op_simplify()
        pass

    # Enter a parse tree produced by cParser#operation_plus_minus.
    def enterOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        # Check whether there are two children
        if ctx.getChildCount() == 3:
            symbol = ""
            if ctx.PLUS():
                symbol = "+"
            elif ctx.MIN():
                symbol = "-"
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_plus_minus.
    def exitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        print("Exit +-")
        if len(self.trees) > 2:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.value
            if symbol == "+" or symbol == "-":
                self.binary_op_simplify()
        # self.finalTree.children.append(self.previousTree)
        # self.previousTree = None
        pass

    # Enter a parse tree produced by cParser#operation_mult_div.
    def enterOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        print("Enter */")
        if ctx.getChildCount() == 3:
            symbol = ""
            if ctx.MULT():
                symbol = "*"
            elif ctx.DIV():
                symbol = "/"
            elif ctx.MOD():
                symbol = "%"
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_mult_div.
    def exitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        print("Exit */")
        if len(self.trees) > 2:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.value
            if symbol == "*" or symbol == "/" or symbol == "%":
                self.binary_op_simplify()
        pass

    def binary_op_simplify(self):
        tree = self.trees[len(self.trees)-3]
        left_tree = self.trees[len(self.trees) - 2]
        right_tree = self.trees[len(self.trees) - 1]
        tree.children.append(left_tree)
        tree.children.append(right_tree)
        self.trees.pop()
        self.trees.pop()

    def unary_op_simplify(self):
        tree = self.trees[len(self.trees)-2]
        sub_tree = self.trees[len(self.trees) - 2]
        tree.children.append(sub_tree)
        self.trees.pop()

    # Enter a parse tree produced by cParser#operation_unary_plus_minus_not.
    def enterOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        # One child means immediatly another operation, 2 children means an OP (+|-|!) and then an expression
        if ctx.getChildCount() == 2:
            symbol = ""
            if ctx.PLUS():
                symbol = "+"
            elif ctx.MIN():
                symbol = "-"
            elif ctx.NOT():
                symbol = "!"
            else:
                raise
            self.trees.append(AST(symbol))
        pass

    # Exit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def exitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        if len(self.trees) > 1:
            tree = self.trees[len(self.trees) - 2]
            symbol = tree.value
            if symbol == "+" or symbol == "-" or symbol == "!":
                self.unary_op_simplify()
        pass

    # Enter a parse tree produced by cParser#operation_brackets.
    def enterOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        print("enter (")
        pass

    # Exit a parse tree produced by cParser#operation_brackets.
    def exitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        print("exit )")
        if ctx.ID():
            print(ctx.getText())
            self.trees.append(AST(value=ctx.getText()))
        pass

    # Enter a parse tree produced by cParser#identifier.
    def enterIdentifier(self, ctx: cParser.IdentifierContext):
        print("Enter identifier")
        pass

    # Exit a parse tree produced by cParser#identifier.
    def exitIdentifier(self, ctx: cParser.IdentifierContext):
        print("Exit identifier")
        pass
