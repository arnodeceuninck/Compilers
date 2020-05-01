from antlr4 import *
from gen.cParser import cParser
from src.ErrorListener import CompilerError
from src.Node.AST import AST, StatementSequence, If, For, Assign, VFloat, VInt, VChar, CBool, CFloat, CInt, CChar, \
    Comments, Variable, LogicAnd, LogicOr, LessOrEq, LessT, Equal, NotEqual, UDeref, UDMinus, UDPlus, Unary, UNot, \
    UMinus, UPlus, UReref, Binary, BMinus, BPlus, Print, MoreOrEq, MoreT, Mult, Div, Mod, While, Break, Continue, \
    has_symbol_table, Return, Function, Arguments, Include, CString, CArray, ArrayIndex


# Check whether a context has real children (and not only a connection to the next node)
def has_children(ctx: ParserRuleContext):
    return ctx.getChildCount() > 1


# This class defines a complete listener for a parse tree produced by cParser.
class customListener(ParseTreeListener):
    def __init__(self):
        self.trees = []  # A stack containing all subtrees
        self.scope_count = 0  # The current scope we are finding ourselves in

    # Add an AST with given node to the stack
    def add(self, ast):
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
        self.enterOperation_sequence(ctx)
        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: cParser.Start_ruleContext):
        self.exitOperation_sequence(ctx)
        if len(self.trees) != 1:
            raise CompilerError
        pass

    # Enter a parse tree produced by cParser#operation_sequence.
    def enterOperation_sequence(self, ctx: cParser.Operation_sequenceContext):
        # self.scope_count += 1
        # We need to check if we are in the global scope, if so then we need to check if include already inserted something
        # If include already did then we need to do nothing because there is already a statement sequence
        # if len(self.trees) and self.scope_count == 1:
        #     return
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
        pass
        # self.scope_count -= 1

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
    def enterAssign(self, ctx: cParser.AssignmentContext):
        # print("Enter Assignment")
        # for child in ctx.children:
        #     if child.symbol == ctx.ASSIGN
        if has_children(ctx):
            if ctx.ASSIGN():
                node = Assign()
                # If the lhs is not a declaration then mark is at false
                # This should be fixed with my change in the grammar
                # if ctx.children[0].getChildCount() == 1 or ctx.children[0].getChild(0).getText() == "*" or \
                #         (ctx.children[0].getChildCount() == 4 and  # Assignment
                #          ctx.children[0].getChild(1).getText() == "[" and ctx.children[0].getChild(3).getText() == "]"):
                if not isinstance(ctx.children[0], cParser.DeclareContext):
                    node.declaration = False
                else:
                    node.declaration = True
                self.add(node)

    def exitAssign(self, ctx: cParser.AssignmentContext):
        # print("Exit Assignment")
        if has_children(ctx):
            self.simplify(2)
            pass

    def help_exit_lvalue_declare(self, ctx, declaration=False):
        value = ""
        ptr = False
        const = False
        node = None
        array_index = 0
        for child in ctx.getChildren():
            # Try to find the type of the variable
            if child.getText() == str(ctx.INT_TYPE()):
                node = VInt()
            elif child.getText() == str(ctx.FLOAT_TYPE()):
                node = VFloat()
            elif child.getText() == str(ctx.CHAR_TYPE()):
                node = VChar()
            elif child.symbol == ctx.array_index:
                array_index = int(child.getText())
            elif child.symbol == ctx.variable:
                # Get the name of variable
                value = child.getText()
                # if ctx.getChildCount() == 1 or ctx.getChild(0).getText() == "*" or \
                #         (ctx.getChildCount() == 4 and  # Assignment
                #          ctx.getChild(1).getText() == "[" and ctx.getChild(3).getText() == "]"):  # Assignment
                if not declaration:
                    # Case: assignment (no declaration)
                    node = Variable(value)

            # Check whether it's a pointer
            elif child.getText() == "*":
                ptr = True

            # Check whether it's a const variable
            elif child.getText() == str(ctx.CONST()):
                const = True

        node.value = value
        node.const = const
        node.ptr = ptr
        node.declaration = declaration
        if array_index:
            node.array = True
            node.array_number = array_index
        # when the righthand side is dereferenced then we need to add the deref node together with the variable node
        if ctx.getChild(0).getText() == "*":
            self.add(UReref())
            self.add(node)
            # Combine these two nodes
            self.simplify(1)
            return
        self.add(node)

    # Enter a parse tree produced by cParser#lvalue.
    def enterLvalue(self, ctx: cParser.LvalueContext):
        pass

    # Exit a parse tree produced by cParser#lvalue.
    def exitLvalue(self, ctx: cParser.LvalueContext):
        declaration = False
        for child in ctx.children:
            if child.symbol == ctx.declaration:
                declaration = True
        self.help_exit_lvalue_declare(ctx, declaration=declaration)

    # Exit a parse tree produced by cParser#declare.
    def exitDeclare(self, ctx: cParser.DeclareContext):
        self.help_exit_lvalue_declare(ctx, declaration=True)

    # Enter a parse tree produced by cParser#declare.
    def enterDeclare(self, ctx: cParser.DeclareContext):
        pass

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

    # # Enter a parse tree produced by cParser#print_statement.
    # def enterPrint_statement(self, ctx: cParser.Print_statementContext):
    #     self.add(Print())
    #
    # # Exit a parse tree produced by cParser#print_statement.
    # def exitPrint_statement(self, ctx: cParser.Print_statementContext):
    #     if ctx.INT_ID():
    #         self.add(CInt(ctx.INT_ID().getText()))
    #     elif ctx.FLOAT_ID():
    #         self.add(CFloat(ctx.FLOAT_ID().getText()))
    #     elif ctx.CHAR_ID():
    #         character = ctx.CHAR_ID().getText()  # e.g. 'a'
    #         character = character[1:-1]  # e.g. a
    #         self.add(CChar(character))
    #     elif ctx.VAR_NAME():
    #         self.add(Variable(ctx.VAR_NAME().getText()))
    #     self.simplify(1)

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
            self.add(Break("break"))
        elif ctx.CONTINUE():
            self.add(Continue("continue"))
        elif ctx.VAR_NAME():
            self.add(Variable(ctx.getText()))
        elif ctx.STR_ID():
            self.add(CString(ctx.getText()[1:-1]))
        # Handling operation of orders with brackets is already assured by the grammar
        pass

    # Enter a parse tree produced by cParser#return_op.
    def enterReturn_op(self, ctx: cParser.Return_opContext):
        self.add(Return("return"))
        # if has_children(ctx):
        #     if ctx.INT_ID():
        #         self.add(CInt(ctx.getText()[6:]))
        #     elif ctx.FLOAT_ID():
        #         self.add(CFloat(ctx.getText()[6:]))
        #     elif ctx.CHAR_ID():
        #         character = ctx.CHAR_ID().getText()  # e.g. 'a'
        #         character = character[1:-1]  # e.g. a
        #         self.add(CChar(character))
        #     elif ctx.VAR_NAME():
        #         self.add(Variable(ctx.getText()[6:]))

    # Exit a parse tree produced by cParser#return_op.
    def exitReturn_op(self, ctx: cParser.Return_opContext):
        # TODO: Fix that this also works with variables and such in place...
        if has_children(ctx):
            # # TODO: This needs to be much more elegant
            # # We need to switch the return and last value because they are in the wrong order in the list
            # # Take the last element
            # last_element = self.trees[len(self.trees) - 1]
            # # Take the pre last element
            # pre_last_element = self.trees[len(self.trees) - 2]
            # # Swap the two entities
            # self.trees[len(self.trees) - 1] = pre_last_element
            # self.trees[len(self.trees) - 2] = last_element

            # make it a child of the current return value
            self.simplify(1)
        pass

    # Enter a parse tree produced by cParser#function.
    def enterFunction(self, ctx: cParser.FunctionContext):
        pass

    # Exit a parse tree produced by cParser#function.
    def exitFunction(self, ctx: cParser.FunctionContext):
        pass

    # Enter a parse tree produced by cParser#function_definition.
    def enterFunction_definition(self, ctx: cParser.Function_definitionContext):
        self.add(Function(value=str(ctx.children[1]), return_type=str(ctx.children[0]), function_type="definition"))
        pass

    # Exit a parse tree produced by cParser#function_definition.
    def exitFunction_definition(self, ctx: cParser.Function_definitionContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by cParser#function_declaration.
    def enterFunction_declaration(self, ctx: cParser.Function_declarationContext):
        self.add(Function(value=str(ctx.children[1]), return_type=str(ctx.children[0]), function_type="declaration"))
        pass

    # Exit a parse tree produced by cParser#function_declaration.
    def exitFunction_declaration(self, ctx: cParser.Function_declarationContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by cParser#function_use.
    def enterFunction_use(self, ctx: cParser.Function_useContext):
        # TODO: update the return type of this function, needs to be searched
        self.add(Function(value=str(ctx.children[0]), function_type="use"))
        pass

    # Exit a parse tree produced by cParser#function_use.
    def exitFunction_use(self, ctx: cParser.Function_useContext):
        # If we have arguments that are passed through
        if has_children(ctx):
            self.simplify(1)
        pass

    # Enter a parse tree produced by cParser#argument_list.
    def enterArgument_list(self, ctx: cParser.Argument_listContext = None):
        self.add(Arguments())
        pass

    # Exit a parse tree produced by cParser#argument_list.
    def exitArgument_list(self, ctx: cParser.Argument_listContext = None):
        # Find the number of children
        children = 0
        tree = self.trees[len(self.trees) - 1]
        while not isinstance(tree, Arguments):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]

        self.simplify(children)
        pass

    # Enter a parse tree produced by cParser#argument.
    def enterArgument(self, ctx: cParser.ArgumentContext):
        value = ""
        ptr = False
        const = False
        node = None
        for child in ctx.getChildren():
            # Try to find the type of the variable
            if child.getText() == str(ctx.INT_TYPE()):
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

            elif ctx.VAR_NAME():
                # Get the name of variable
                value = child.getText()
                if ctx.getChildCount() == 1:
                    # Case: assignment (no declaration)
                    node = Variable()

        node.value = value
        node.const = const
        node.ptr = ptr
        node.declaration = True
        self.add(node)

    # Exit a parse tree produced by cParser#argument.
    def exitArgument(self, ctx: cParser.ArgumentContext):
        pass

    # Enter a parse tree produced by cParser#use_argument_list.
    def enterUse_argument_list(self, ctx: cParser.Use_argument_listContext):
        self.enterArgument_list()
        pass

    # Exit a parse tree produced by cParser#use_argument_list.
    def exitUse_argument_list(self, ctx: cParser.Use_argument_listContext):
        self.exitArgument_list()
        pass

    # Enter a parse tree produced by cParser#include.
    def enterInclude(self, ctx: cParser.IncludeContext):
        # If we detect no trees then we must add a statement sequence
        # We do this in order to avoid that the include comes in front of the first statement sequence
        # if not len(self.trees):
        #     self.add(StatementSequence(self.scope_count + 1))
        self.add(Include())
        pass

    # Exit a parse tree produced by cParser#include.
    def exitInclude(self, ctx: cParser.IncludeContext):
        pass

    # Enter a parse tree produced by cParser#const_array.
    def enterConst_array(self, ctx: cParser.Const_arrayContext):
        self.add(CArray())

    # Exit a parse tree produced by cParser#const_array.
    def exitConst_array(self, ctx: cParser.Const_arrayContext):
        # Find the number of children
        children = 0
        tree = self.trees[len(self.trees) - 1]
        while not isinstance(tree, CArray):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]

        self.simplify(children)

    # Enter a parse tree produced by cParser#const_array_element.
    def enterConst_array_element(self, ctx: cParser.Const_array_elementContext):
        pass

    # Exit a parse tree produced by cParser#const_array_element.
    def exitConst_array_element(self, ctx: cParser.Const_array_elementContext):
        if ctx.INT_ID():
            self.add(CInt(ctx.getText()))
        elif ctx.FLOAT_ID():
            self.add(CFloat(ctx.getText()))
        elif ctx.CHAR_ID():
            character = ctx.CHAR_ID().getText()  # e.g. 'a'
            character = character[1:-1]  # e.g. a
            self.add(CChar(character))
        elif ctx.VAR_NAME():
            self.add(Variable(ctx.getText()))
        pass

    # Enter a parse tree produced by cParser#array_var_name.
    def enterArray_var_name(self, ctx: cParser.Array_var_nameContext):
        index = None
        variable = None
        for child in ctx.getChildren():
            # if child.symbol == ctx.nr:
            #     index = int(child.getText())
            try:
                if child.symbol == ctx.var:
                    variable = Variable(child.getText())
            except AttributeError:
                pass # Because an Operation_logic_orContext object has no attribute 'symbol'
        self.add(ArrayIndex(index))
        self.add(variable)
        pass

    # Exit a parse tree produced by cParser#array_var_name.
    def exitArray_var_name(self, ctx: cParser.Array_var_nameContext):
        self.simplify(2)
        pass