from antlr4 import *
from src.AST import *
from gen.cParser import cParser


# This class defines a complete listener for a parse tree produced by cParser.
class customListener(ParseTreeListener):
    # Beste Basil,

    # Sorry dat ik doorheen deze code niet echt veel heb gedocumenteerd.
    # Bij deze zal ik het dus kort even uitleggen:

    # Op weg naar beneden worden bomen aangemaakt met het juiste karakter erop en die worden op een stack gepusht.
    # Dit gebeurt enkel indien er meer dan 1 kind is (want anders verwijst het gewoon naar de volgende operatie,
    # en komt de operatie dus niet echt voor op die plaats.

    # Op weg naar boven wordt er gecheckt of de stack top -2 een teken bevat van de regel. Als dit zo is, dan worden de
    # twee achterste elementen van de stack gepopt en ingesteld als kinderen van de boom met het teken.

    # Hopelijk begrijp je deze brakka uitleg en beetje, en anders ga je alsnog in de code moeten kijken
    trees = []  # This should be used as a stack

    def __init__(self):
        self.previousTree = None
        self.finalTree = None

    """
    Combines all the left over trees in the trees global variable
    It also changes the ids of every child with the position it is normally in
    """

    def combine_trees(self):
        # If there is 1 tree left set no root
        if len(self.trees) == 1:
            return

        # If there are more trees link them with a root
        newRoot = AST(Node("Statement Sequence"))
        for tree in self.trees:
            tree.parent = newRoot
            newRoot.children.append(tree)
        self.trees.clear()
        self.trees.append(newRoot)


    def unary_op_simplify(self):
        tree = self.trees[len(self.trees) - 2]
        sub_tree = self.trees[len(self.trees) - 1]
        sub_tree.parent = tree
        tree.children.append(sub_tree)
        self.trees.pop()

    # Enter a parse tree produced by cParser#start_rule.
    def enterStart_rule(self, ctx: cParser.Start_ruleContext):
        # print("enter Start")
        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: cParser.Start_ruleContext):
        # print("exit Start")
        self.finalTree = self.previousTree
        # Will combine all the generated trees
        self.combine_trees()

    # Enter a parse tree produced by cParser#operation.
    def enterOperation(self, ctx: cParser.OperationContext):
        # print("Enter Operation")
        pass

    # Exit a parse tree produced by cParser#operation.
    def exitOperation(self, ctx: cParser.OperationContext):
        # print("Exit operation")
        pass

    # Enter a parse tree produced by cParser#assignment.
    def enterAssignment(self, ctx: cParser.AssignmentContext):
        # print("Enter Assignment")
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.ASSIGN():
                symbol = "="
                node = Assign(symbol)
            else:
                raise
            self.trees.append(AST(node))

    def exitAssignment(self, ctx: cParser.AssignmentContext):
        # print("Exit Assignment")
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "=":
                self.binary_op_simplify()
            # Set the defined value of the variable to defined
            tree = self.trees[len(self.trees) - 1]
            tree.children[0].node.defined = True

    # Enter a parse tree produced by cParser#lvalue.
    def enterLvalue(self, ctx: cParser.LvalueContext):
        pass

    # Exit a parse tree produced by cParser#lvalue.
    def exitLvalue(self, ctx: cParser.LvalueContext):
        value = ""
        ptr = False
        const = False
        node = None
        for child in ctx.getChildren():
            # If there is only one child then it is an assignment and not a definition or declaration,
            # so no need for explicitly giving the variable a type
            if child.symbol == ctx.variable and ctx.getChildCount() == 1:
                value = child.getText()
                node = Variable()
            elif child.symbol == ctx.variable:
                # print(child.getText())
                value = child.getText()
            elif child.getText() == str(ctx.INT_TYPE()):
                node = VInt()
            elif child.getText() == str(ctx.FLOAT_TYPE()):
                node = VFloat()
            elif child.getText() == str(ctx.CHAR_TYPE()):
                node = VChar()
            elif child.getText() == "*":
                ptr = True
            elif child.getText() == str(ctx.CONST()):
                const = True
        node.value = value
        node.const = const
        node.ptr = ptr
        self.trees.append(AST(node))

    # Enter a parse tree produced by cParser#operation_logic_or.
    def enterOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        # Check whether there are three children: leftside, OP, rightside
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.LOR():
                symbol = "||"
                node = LogicOr(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#operation_logic_or.
    def exitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "||":
                self.binary_op_simplify()

    # Enter a parse tree produced by cParser#operation_logic_and.
    def enterOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        # Check whether there are three children: leftside, OP, rightside
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.LAND():
                symbol = "&&"
                node = LogicAnd(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#operation_logic_and.
    def exitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "&&":
                self.binary_op_simplify()

    # Enter a parse tree produced by cParser#operation_compare_eq_neq.
    def enterOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        # Check whether there are three children: leftside, OP, rightside
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.EQ():
                symbol = "=="
                node = Equal(symbol)
            elif ctx.NEQ():
                symbol = "!="
                node = NotEqual(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Enter a parse tree produced by cParser#print_statement.
    def enterPrint_statement(self, ctx: cParser.Print_statementContext):
        node = Print()
        self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#print_statement.
    def exitPrint_statement(self, ctx: cParser.Print_statementContext):
        if ctx.INT_ID():
            # print(ctx.getText())
            self.trees.append(AST(node=CInt(ctx.INT_ID().getText())))
        elif ctx.FLOAT_ID():
            # print(ctx.getText())
            self.trees.append(AST(node=CFloat(ctx.FLOAT_ID().getText())))
        elif ctx.CHAR_ID():
            # print(ctx.getText())
            self.trees.append(AST(node=CChar(ctx.CHAR_ID().getText())))
        elif ctx.VAR_NAME():
            # print(ctx.getText())
            self.trees.append(AST(node=Variable(ctx.VAR_NAME().getText())))
        self.unary_op_simplify()


    # Exit a parse tree produced by cParser#operation_compare_eq_neq.
    def exitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "==" or symbol == "!=":
                self.binary_op_simplify()

    # Enter a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def enterOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        # Check whether there are three children: leftside, OP, rightside
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.LEQ():
                symbol = "<="
                node = LessOrEq(symbol)
            elif ctx.GEQ():
                symbol = ">="
                node = MoreOrEq(symbol)
            elif ctx.LT():
                symbol = "<"
                node = LessT(symbol)
            elif ctx.GT():
                symbol = ">"
                node = MoreT(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def exitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "<=" or symbol == ">=" or symbol == "<" or symbol == ">":
                self.binary_op_simplify()

    # Enter a parse tree produced by cParser#operation_plus_minus.
    def enterOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        # Check whether there are three children: leftside, OP, rightside
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.PLUS():
                symbol = "+"
                node = BPlus(symbol)
            elif ctx.MIN():
                symbol = "-"
                node = BMinus(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#operation_plus_minus.
    def exitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        # print("Exit +-")
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "+" or symbol == "-":
                self.binary_op_simplify()
        # self.finalTree.children.append(self.previousTree)
        # self.previousTree = None

    # Enter a parse tree produced by cParser#operation_mult_div.
    def enterOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        # print("Enter */")
        if ctx.getChildCount() == 3:
            symbol = ""
            node = None
            if ctx.MULT():
                symbol = "*"
                node = Mult(symbol)
            elif ctx.DIV():
                symbol = "/"
                node = Div(symbol)
            elif ctx.MOD():
                symbol = "%"
                node = Mod(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#operation_mult_div.
    def exitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        # print("Exit */")
        if len(self.trees) > 2 and ctx.getChildCount() == 3:
            tree = self.trees[len(self.trees) - 3]
            symbol = tree.node.value
            if symbol == "*" or symbol == "/" or symbol == "%":
                self.binary_op_simplify()

    def binary_op_simplify(self):
        tree = self.trees[len(self.trees) - 3]
        left_tree = self.trees[len(self.trees) - 2]
        right_tree = self.trees[len(self.trees) - 1]
        left_tree.parent = tree
        right_tree.parent = tree
        tree.children.append(left_tree)
        tree.children.append(right_tree)
        self.trees.pop()
        self.trees.pop()

    # Enter a parse tree produced by cParser#operation_unary_plus_minus_not.
    def enterOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        # One child means immediatly another operation, 2 children means an OP (+|-|!) and then an expression
        if ctx.getChildCount() == 2:
            symbol = ""
            node = None
            if ctx.PLUS():
                symbol = "+"
                node = UPlus(symbol)
            elif ctx.MIN():
                symbol = "-"
                node = UMinus(symbol)
            elif ctx.NOT():
                symbol = "!"
                node = Node(symbol)
            else:
                raise
            self.trees.append(AST(node))

    # Exit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def exitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        if len(self.trees) > 1 and ctx.getChildCount() == 2:
            tree = self.trees[len(self.trees) - 2]
            symbol = tree.node.value
            if symbol == "+" or symbol == "-" or symbol == "!":
                self.unary_op_simplify()

    # Enter a parse tree produced by cParser#operation_brackets.
    def enterOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        # print("enter (")
        if ctx.getChildCount() == 3:
            self.trees.append(AST(Node("[BRACKETS]")))
        pass

    # Exit a parse tree produced by cParser#operation_brackets.
    def exitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        # print("exit )")
        if ctx.INT_ID():
            # print(ctx.getText())
            self.trees.append(AST(node=CInt(ctx.getText())))
        elif ctx.FLOAT_ID():
            # print(ctx.getText())
            self.trees.append(AST(node=CFloat(ctx.getText())))
        elif ctx.CHAR_ID():
            # print(ctx.getText())
            self.trees.append(AST(node=CChar(ctx.getText())))
        elif ctx.VAR_NAME():
            # print(ctx.getText())
            self.trees.append(AST(node=Variable(ctx.getText())))
        else:
            if len(self.trees) > 1:
                self.trees[len(self.trees) -
                           2] = self.trees[len(self.trees) - 1]
                self.trees.pop()
