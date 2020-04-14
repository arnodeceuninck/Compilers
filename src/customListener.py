from antlr4 import *
from gen.cParser import cParser
from src.ErrorListener import CompilerError
from src.Node.AST import AST, StatementSequence, If, For, Assign, VFloat, VInt, VChar, CBool, CFloat, CInt, CChar, \
    Comments, Variable, LogicAnd, LogicOr, LessOrEq, LessT, Equal, NotEqual, UDeref, UDMinus, UDPlus, Unary, UNot, \
    UMinus, UPlus, UReref, Binary, BMinus, BPlus, Print, MoreOrEq, MoreT, Mult, Div, Mod, While, Break, Continue, \
    has_symbol_table, Return


# Check whether a context has real children (and not only a connection to the next node)
def has_children(ctx: ParserRuleContext):
    return ctx.getChildCount() > 1


# This class defines a complete listener for a parse tree produced by cParser.
class customListener(ParseTreeListener):
    def __init__(self):
        self.trees = []  # A stack containing all subtrees
        self.scope_count = 0  # The current scope we are finding ourselves in

    # Add an AST with given node to the stack
    def add(self, ast: AST):
        self.trees.append(ast)

    # Take <size> trees from the stack and place them as children from the last stack top
    # size = 1 for unary operations, size = 2 for binary operations
    def simplify(self, size: int):
        # Collect all children from the top of the stack
        children = list()
        for i in range(size):
            term = self.trees.pop()
            children.insert(0, term)

        # The current top should be the operator
        operator = self.trees[len(self.trees) - 1]

        # Assign the children to the operator
        operator.children = children
        for i in range(len(children)):
            children[i].parent = operator

    # Enter a parse tree produced by cParser#start_rule.
    def enterStart_rule(self, ctx: cParser.Start_ruleContext):
        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: cParser.Start_ruleContext):
        if len(self.trees) != 1:
            raise CompilerError
        pass

    # Enter a parse tree produced by cParser#operation_sequence.
    def enterOperation_sequence(self, ctx: cParser.Operation_sequenceContext):
        self.scope_count += 1
        self.add(StatementSequence(self.scope_count))

    # Exit a parse tree produced by cParser#operation_sequence.
    def exitOperation_sequence(self, ctx: cParser.Operation_sequenceContext):
        # Find the number of children
        children = 0
        tree = self.trees[len(self.trees) - 1]
        # When we exit the operation sequence we need to find the right tree to fold to,
        # which should be the same as the scope count of a tree that is the same as the one of
        # the custom listener
        while isinstance(tree, has_symbol_table):
            # If the scope count is the same
            if tree.scope_count == self.scope_count:
                break
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]

        while not isinstance(tree, has_symbol_table):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]
            # Check if the matched scope of the item is met
            while isinstance(tree, has_symbol_table):
                if tree.scope_count == self.scope_count:
                    break
                children += 1
                tree = self.trees[len(self.trees) - 1 - children]

        self.simplify(children)
        self.scope_count -= 1

    # Enter a parse tree produced by cParser#unnamed_scope.
    def enterUnnamed_scope(self, ctx: cParser.Unnamed_scopeContext):
        pass

    # Exit a parse tree produced by cParser#unnamed_scope.
    def exitUnnamed_scope(self, ctx: cParser.Unnamed_scopeContext):
        pass

    # Enter a parse tree produced by cParser#if_statement.
    def enterIf_statement(self, ctx: cParser.If_statementContext):
        if has_children(ctx):
            self.add(If())

    # Exit a parse tree produced by cParser#if_statement.
    def exitIf_statement(self, ctx: cParser.If_statementContext):
        # Find the number of children, it always will be 2 or 3, because
        # if we have an if it will be 2, because of the condition and the statement sequence,
        # If it is an else, there will be 3 children condition, statement sequence and else statement sequence
        children = 2
        tree = self.trees[len(self.trees) - 3]

        if not isinstance(tree, If):
            children = 3

        self.simplify(children)

    # Enter a parse tree produced by cParser#else_statement.
    def enterElse_statement(self, ctx: cParser.Else_statementContext):
        pass

    # Exit a parse tree produced by cParser#else_statement.
    def exitElse_statement(self, ctx: cParser.Else_statementContext):
        pass

    # Enter a parse tree produced by cParser#while_statement.
    def enterWhile_statement(self, ctx: cParser.While_statementContext):
        self.add(While())

    # Exit a parse tree produced by cParser#while_statement.
    def exitWhile_statement(self, ctx: cParser.While_statementContext):
        self.simplify(2)

    # Enter a parse tree produced by cParser#for_statement.
    def enterFor_statement(self, ctx: cParser.For_statementContext):
        self.scope_count += 1
        self.add(For(self.scope_count))
        pass

    # Exit a parse tree produced by cParser#for_statement.
    def exitFor_statement(self, ctx: cParser.For_statementContext):
        self.simplify(4)
        self.scope_count -= 1
        pass

    # Enter a parse tree produced by cParser#operation.
    def enterOperation(self, ctx: cParser.OperationContext):
        pass

    # Exit a parse tree produced by cParser#operation.
    def exitOperation(self, ctx: cParser.OperationContext):
        pass

    # Enter a parse tree produced by cParser#assignment.
    def enterAssignment(self, ctx: cParser.AssignmentContext):
        # print("Enter Assignment")
        if has_children(ctx):
            if ctx.ASSIGN():
                node = Assign()
                if ctx.children[0].getChildCount() == 1:
                    node.declaration = False
                self.add(node)

    def exitAssignment(self, ctx: cParser.AssignmentContext):
        # print("Exit Assignment")
        if has_children(ctx):
            self.simplify(2)

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
            if child.symbol == ctx.variable:
                # Get the name of variable
                value = child.getText()
                if ctx.getChildCount() == 1:
                    # Case: assignment (no declaration)
                    node = Variable()

            # Try to find the type of the variable
            elif child.getText() == str(ctx.INT_TYPE()):
                node = VInt()
            elif child.getText() == str(ctx.FLOAT_TYPE()):
                node = VFloat()
            elif child.getText() == str(ctx.CHAR_TYPE()):
                node = VChar()

            # Check whether it's a pointer
            elif child.getText() == "*":
                ptr = True

            # Check whether it's a const variable
            elif child.getText() == str(ctx.CONST()):
                const = True

        node.value = value
        node.const = const
        node.ptr = ptr
        self.add(node)

    # Enter a parse tree produced by cParser#operation_logic_or.
    def enterOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        # Check whether there are three children: leftside, OP, rightside
        if has_children(ctx):
            if ctx.LOR():
                self.add(LogicOr())

    # Exit a parse tree produced by cParser#operation_logic_or.
    def exitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        if has_children(ctx):
            self.simplify(2)

    # Enter a parse tree produced by cParser#operation_logic_and.
    def enterOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        # Check whether there are three children: leftside, OP, rightside
        if has_children(ctx):
            if ctx.LAND():
                self.add(LogicAnd())

    # Exit a parse tree produced by cParser#operation_logic_and.
    def exitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        if has_children(ctx):
            self.simplify(2)

    # Enter a parse tree produced by cParser#operation_compare_eq_neq.
    def enterOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        # Check whether there are three children: leftside, OP, rightside
        if has_children(ctx):
            if ctx.EQ():
                self.add(Equal())
            elif ctx.NEQ():
                self.add(NotEqual())

    # Enter a parse tree produced by cParser#print_statement.
    def enterPrint_statement(self, ctx: cParser.Print_statementContext):
        self.add(Print())

    # Exit a parse tree produced by cParser#print_statement.
    def exitPrint_statement(self, ctx: cParser.Print_statementContext):
        if ctx.INT_ID():
            self.add(CInt(ctx.INT_ID().getText()))
        elif ctx.FLOAT_ID():
            self.add(CFloat(ctx.FLOAT_ID().getText()))
        elif ctx.CHAR_ID():
            character = ctx.CHAR_ID().getText()  # e.g. 'a'
            character = character[1:-1]  # e.g. a
            self.add(CChar(character))
        elif ctx.VAR_NAME():
            self.add(Variable(ctx.VAR_NAME().getText()))
        self.simplify(1)

    # Exit a parse tree produced by cParser#operation_compare_eq_neq.
    def exitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        if has_children(ctx):
            self.simplify(2)

    # Enter a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def enterOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        # Check whether there are three children: leftside, OP, rightside
        if has_children(ctx):
            if ctx.LEQ():
                self.add(LessOrEq())
            elif ctx.GEQ():
                self.add(MoreOrEq())
            elif ctx.LT():
                self.add(LessT())
            elif ctx.GT():
                self.add(MoreT())

    # Exit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def exitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        if has_children(ctx):
            self.simplify(2)

    # Enter a parse tree produced by cParser#operation_plus_minus.
    def enterOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        # Check whether there are three children: leftside, OP, rightside
        if has_children(ctx):
            if ctx.PLUS():
                self.add(BPlus())
            elif ctx.MIN():
                self.add(BMinus())

    # Exit a parse tree produced by cParser#operation_plus_minus.
    def exitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        if has_children(ctx):
            self.simplify(2)

    # Enter a parse tree produced by cParser#operation_mult_div.
    def enterOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        # print("Enter */")
        if has_children(ctx):
            if ctx.MULT():
                self.add(Mult())
            elif ctx.DIV():
                self.add(Div())
            elif ctx.MOD():
                self.add(Mod())

    # Exit a parse tree produced by cParser#operation_mult_div.
    def exitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        if has_children(ctx):
            self.simplify(2)

    # Enter a parse tree produced by cParser#operation_unary_plus_minus_not.
    def enterOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        if has_children(ctx):
            if ctx.DOUBLE_PLUS():
                self.add(UDPlus())
            if ctx.DOUBLE_MIN():
                self.add(UDMinus())
            elif ctx.PLUS():
                self.add(UPlus())
            elif ctx.MIN():
                self.add(UMinus())
            elif ctx.NOT():
                self.add(UNot())
            elif ctx.MULT():
                self.add(UReref())
            elif ctx.REF():
                self.add(UDeref())

    # Exit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def exitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        if ctx.getChildCount() == 2:
            self.simplify(1)

    # Enter a parse tree produced by cParser#operation_brackets.
    def enterOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        pass

    # Exit a parse tree produced by cParser#operation_brackets.
    def exitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        if ctx.INT_ID():
            self.add(CInt(ctx.getText()))
        elif ctx.FLOAT_ID():
            self.add(CFloat(ctx.getText()))
        elif ctx.CHAR_ID():
            character = ctx.CHAR_ID().getText()  # e.g. 'a'
            character = character[1:-1]  # e.g. a
            self.add(CChar(character))
        elif ctx.BREAK():
            self.add(Break())
        elif ctx.CONTINUE():
            self.add(Continue())
        elif ctx.VAR_NAME():
            self.add(Variable(ctx.getText()))
        # Handling operation of orders with brackets is already assured by the grammar
        pass

    # Enter a parse tree produced by cParser#return_op.
    def enterReturn_op(self, ctx: cParser.Return_opContext):
        self.add(Return())
        if has_children(ctx):
            if ctx.INT_ID():
                self.add(CInt(ctx.getText()[6:]))
            elif ctx.FLOAT_ID():
                self.add(CFloat(ctx.getText()[6:]))
            elif ctx.CHAR_ID():
                character = ctx.CHAR_ID().getText()  # e.g. 'a'
                character = character[1:-1]  # e.g. a
                self.add(CChar(character))
            elif ctx.VAR_NAME():
                self.add(Variable(ctx.getText()[6:]))
            # make it a child of the current return value
            self.simplify(1)

    # Exit a parse tree produced by cParser#return_op.
    def exitReturn_op(self, ctx: cParser.Return_opContext):
        pass
