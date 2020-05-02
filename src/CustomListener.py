# Generated from /home/arno/Documents/Compilers/input/c.g4 by ANTLR 4.8
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
class CustomListener(ParseTreeListener):
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
        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: cParser.Start_ruleContext):
        # All trees from the parser must be simplified
        if len(self.trees) != 1:
            print("Not all trees collapsed")
            raise CompilerError
        pass

    # Enter a parse tree produced by cParser#include.
    def enterInclude(self, ctx: cParser.IncludeContext):
        # If we detect no trees then we must add a statement sequence
        # We do this in order to avoid that the include comes in front of the first statement sequence
        if not len(self.trees):
            self.add(StatementSequence(self.scope_count))
        self.add(Include())
        pass

    # Exit a parse tree produced by cParser#include.
    def exitInclude(self, ctx: cParser.IncludeContext):
        pass

    # Enter a parse tree produced by cParser#operation_sequence.
    def enterOperation_sequence(self, ctx: cParser.Operation_sequenceContext):
        # We need to check if we are in the global scope, if so then we need to check if include already inserted something
        # If include already did then we need to do nothing because there is already a statement sequence
        if len(self.trees) and self.scope_count == 0:
            return
        self.add(StatementSequence(self.scope_count))
        pass

    # Exit a parse tree produced by cParser#operation_sequence.
    def exitOperation_sequence(self, ctx: cParser.Operation_sequenceContext):
        # Find the number of children
        children = 0
        tree = self.trees[len(self.trees) - 1]
        # When we exit the operation sequence we need to find the right tree to fold to,
        # which should be the same as the scope count of a tree that is the same as the one of
        # the custom listener
        # print("Passed")
        # while not isinstance(has_symbol_table) or tree.scope_count == self.scope_count+1:
        #     children += 1
        #     tree = self.trees[len(self.trees) - 1 - children]
        # # children -= 1 # Remove the scope element itself

        # Get to the right scope
        while isinstance(tree, has_symbol_table):
            # If the scope count is the same
            if tree.scope_count == self.scope_count:
                break
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]

        # Find the first element of this scope
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

    # Enter a parse tree produced by cParser#scope.
    def enterScope(self, ctx: cParser.ScopeContext):
        self.scope_count += 1
        pass

    # Exit a parse tree produced by cParser#scope.
    def exitScope(self, ctx: cParser.ScopeContext):
        self.scope_count -= 1
        pass

    # Enter a parse tree produced by cParser#function.
    def enterFunction(self, ctx: cParser.FunctionContext):
        pass

    # Exit a parse tree produced by cParser#function.
    def exitFunction(self, ctx: cParser.FunctionContext):
        pass

    # Enter a parse tree produced by cParser#function_definition.
    def enterFunction_definition(self, ctx: cParser.Function_definitionContext):
        function = Function(function_type="definition")
        function.scope_count = self.scope_count + 1
        self.add(function)
        pass

    # Exit a parse tree produced by cParser#function_definition.
    def exitFunction_definition(self, ctx: cParser.Function_definitionContext):
        # Special case of simplify, since we have to get the argument list back from the declaration
        operation_sequence = self.trees.pop()

        declaration = self.trees.pop()
        return_type = declaration.return_type
        value = declaration.value
        argument_list = declaration.children[0]

        # Set the right value and return type
        definition = self.trees.pop()
        definition.return_type = return_type
        definition.value = value

        self.add(definition)
        self.add(argument_list)
        self.add(operation_sequence)

        self.simplify(2)  # Simplify the argument list and operation sequence
        pass

    # Enter a parse tree produced by cParser#function_declaration.
    def enterFunction_declaration(self, ctx: cParser.Function_declarationContext):
        function = Function(value=str(ctx.var.text), return_type=str(ctx.type_().getText()), function_type="declaration")
        function.scope_count = self.scope_count + 1
        self.add(function)
        pass

    # Exit a parse tree produced by cParser#function_declaration.
    def exitFunction_declaration(self, ctx: cParser.Function_declarationContext):
        self.simplify(1)  # Simplify the argument list
        pass

    # Enter a parse tree produced by cParser#type_.
    def enterType_(self, ctx: cParser.Type_Context):
        pass

    # Exit a parse tree produced by cParser#type_.
    def exitType_(self, ctx: cParser.Type_Context):
        pass

    # Enter a parse tree produced by cParser#variable_declaration.
    def enterVariable_declaration(self, ctx: cParser.Variable_declarationContext):
        # Determine the type of the declaration
        node = None
        if ctx.type_().int_:
            node = VInt()
        elif ctx.type_().float_:
            node = VFloat()
        elif ctx.type_().char_:
            node = VChar()
        else:
            raise CompilerError

        node.const = bool(ctx.const_)
        node.declaration = True

        self.add(node)
        pass

    # Exit a parse tree produced by cParser#variable_declaration.
    def exitVariable_declaration(self, ctx: cParser.Variable_declarationContext):
        # Get the Variable node back and assign the value information
        variable_use = self.trees.pop()
        variable = self.trees.pop()

        variable.value = variable_use.value
        variable.ptr = variable_use.ptr

        if variable_use.array:
            variable.array = variable_use.array
            variable.array_number = variable_use.array_number

        self.add(variable)

        pass

    # Enter a parse tree produced by cParser#variable_use.
    def enterVariable_use(self, ctx: cParser.Variable_useContext):
        node = Variable(value=ctx.var.text)
        # when the righthand side is dereferenced then we need to add the deref node together with the variable node
        self.add(node)
        pass

    # Exit a parse tree produced by cParser#variable_use.
    def exitVariable_use(self, ctx: cParser.Variable_useContext):
        if ctx.array:
            if not isinstance(ctx.parentCtx, cParser.Operation_bracketsContext):
                array = self.trees.pop()
                variable = array[0]
                variable.array = True
                variable.array_number = int(array[1].value)  # Get the value of the CInt (TODO: other expressions)
                variable.parent = None
                self.add(variable)  # Only add variable, ignore array for now (because only int allowed)



        if ctx.getChild(0).getText() == "*" and isinstance(ctx.parentCtx, (cParser.LvalueContext, cParser.Operation_bracketsContext)):
            ptr_count = 1
            while ctx.getText()[ptr_count] == '*':
                ptr_count += 1

            node = self.trees.pop()
            for i in range(ptr_count):
                self.add(UReref())

            self.add(node)

            for i in range(ptr_count):
                self.simplify(1)

            return
        pass

    # Enter a parse tree produced by cParser#array_index.
    def enterArray_index(self, ctx: cParser.Array_indexContext):
        # index = int(ctx.index.getText())
        variable = self.trees.pop()
        node = ArrayIndex()  # TODO: allow more than only int
        self.add(node)
        self.add(variable)
        pass

    # Exit a parse tree produced by cParser#array_index.
    def exitArray_index(self, ctx: cParser.Array_indexContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by cParser#pointer.
    def enterPointer(self, ctx: cParser.PointerContext):
        pass

    # Exit a parse tree produced by cParser#pointer.
    def exitPointer(self, ctx: cParser.PointerContext):
        variable = self.trees.pop()
        variable.ptr += 1
        self.add(variable)
        pass


    # Enter a parse tree produced by cParser#function_use.
    def enterFunction_use(self, ctx: cParser.Function_useContext):
        # TODO: update the return type of this function, needs to be searched
        function = Function(value=ctx.var.text, function_type="use")
        function.scope_count = self.scope_count + 1
        self.add(function)
        pass

    # Exit a parse tree produced by cParser#function_use.
    def exitFunction_use(self, ctx: cParser.Function_useContext):
        # # If we have arguments that are passed through -> There are always arguments
        # if has_children(ctx):
        self.simplify(1)
        pass

    # Enter a parse tree produced by cParser#use_argument_list.
    def enterUse_argument_list(self, ctx: cParser.Use_argument_listContext):
        self.enterArgument_list(ctx)
        pass

    # Exit a parse tree produced by cParser#use_argument_list.
    def exitUse_argument_list(self, ctx: cParser.Use_argument_listContext):
        self.exitArgument_list(ctx)
        pass

    # Enter a parse tree produced by cParser#argument_list.
    def enterArgument_list(self, ctx: cParser.Argument_listContext):
        self.add(Arguments())
        pass

    # Exit a parse tree produced by cParser#argument_list.
    def exitArgument_list(self, ctx: cParser.Argument_listContext):
        # Find the number of children
        children = 0
        tree = self.trees[len(self.trees) - 1]

        while not isinstance(tree, Arguments):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]

        self.simplify(children)
        pass

    # Enter a parse tree produced by cParser#operation.
    def enterOperation(self, ctx: cParser.OperationContext):
        pass

    # Exit a parse tree produced by cParser#operation.
    def exitOperation(self, ctx: cParser.OperationContext):
        pass

    # Enter a parse tree produced by cParser#if_statement.
    def enterIf_statement(self, ctx: cParser.If_statementContext):
        self.add(If())
        pass

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
        pass

    # Enter a parse tree produced by cParser#else_statement.
    def enterElse_statement(self, ctx: cParser.Else_statementContext):
        pass

    # Exit a parse tree produced by cParser#else_statement.
    def exitElse_statement(self, ctx: cParser.Else_statementContext):
        pass

    # Enter a parse tree produced by cParser#while_statement.
    def enterWhile_statement(self, ctx: cParser.While_statementContext):
        self.add(While())
        pass

    # Exit a parse tree produced by cParser#while_statement.
    def exitWhile_statement(self, ctx: cParser.While_statementContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by cParser#for_statement.
    def enterFor_statement(self, ctx: cParser.For_statementContext):
        self.add(For(self.scope_count + 1))
        pass

    # Exit a parse tree produced by cParser#for_statement.
    def exitFor_statement(self, ctx: cParser.For_statementContext):
        self.simplify(4)
        pass

    # Enter a parse tree produced by cParser#assignment.
    def enterAssignment(self, ctx: cParser.AssignmentContext):
        pass

    # Exit a parse tree produced by cParser#assignment.
    def exitAssignment(self, ctx: cParser.AssignmentContext):
        pass

    # Enter a parse tree produced by cParser#assign.
    def enterAssign(self, ctx: cParser.AssignContext):
        node = Assign()
        self.add(node)
        pass

    # Exit a parse tree produced by cParser#assign.
    def exitAssign(self, ctx: cParser.AssignContext):
        rvalue = self.trees.pop()
        lvalue = self.trees.pop()
        assign = self.trees.pop()

        if isinstance(lvalue, UReref):
            assign.declaration = False
        else:
            assign.declaration = lvalue.declaration

        self.add(assign)
        self.add(lvalue)
        self.add(rvalue)

        self.simplify(2)
        pass

    # Enter a parse tree produced by cParser#lvalue.
    def enterLvalue(self, ctx: cParser.LvalueContext):
        pass

    # Exit a parse tree produced by cParser#lvalue.
    def exitLvalue(self, ctx: cParser.LvalueContext):
        pass

    def has_childeren(self, ctx):
        # If it has only one child, it's only the next operation, without using this operation
        return ctx.getChildCount() > 1

    # Every arg should be a tuploe of the form (bool, NodeType)
    def help_operation(self, ctx, *args):
        if not self.has_childeren(ctx):
            return

        node = None
        for arg in args:
            if not arg[0]:
                continue
            node = arg[1]()

        assert node  # There must be a node

        self.add(node)

    def help_simplify(self, ctx, count):
        if not self.has_childeren(ctx):
            return

        self.simplify(count)

    # Enter a parse tree produced by cParser#operation_logic_or.
    def enterOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        self.help_operation(ctx, (ctx.lor, LogicOr))
        pass

    # Exit a parse tree produced by cParser#operation_logic_or.
    def exitOperation_logic_or(self, ctx: cParser.Operation_logic_orContext):
        self.help_simplify(ctx, 2)
        pass

    # Enter a parse tree produced by cParser#operation_logic_and.
    def enterOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        self.help_operation(ctx, (ctx.land, LogicAnd))
        pass

    # Exit a parse tree produced by cParser#operation_logic_and.
    def exitOperation_logic_and(self, ctx: cParser.Operation_logic_andContext):
        self.help_simplify(ctx, 2)
        pass

    # Enter a parse tree produced by cParser#operation_compare_eq_neq.
    def enterOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        self.help_operation(ctx, (ctx.eq, Equal), (ctx.neq, NotEqual))
        pass

    # Exit a parse tree produced by cParser#operation_compare_eq_neq.
    def exitOperation_compare_eq_neq(self, ctx: cParser.Operation_compare_eq_neqContext):
        self.help_simplify(ctx, 2)
        pass

    # Enter a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def enterOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        self.help_operation(ctx, (ctx.leq, LessOrEq), (ctx.geq, MoreOrEq), (ctx.lt, LessT), (ctx.gt, MoreT))
        pass

    # Exit a parse tree produced by cParser#operation_compare_leq_geq_l_g.
    def exitOperation_compare_leq_geq_l_g(self, ctx: cParser.Operation_compare_leq_geq_l_gContext):
        self.help_simplify(ctx, 2)
        pass

    # Enter a parse tree produced by cParser#operation_plus_minus.
    def enterOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        self.help_operation(ctx, (ctx.plus, BPlus), (ctx.minus, BMinus))
        pass

    # Exit a parse tree produced by cParser#operation_plus_minus.
    def exitOperation_plus_minus(self, ctx: cParser.Operation_plus_minusContext):
        self.help_simplify(ctx, 2)
        pass

    # Enter a parse tree produced by cParser#operation_mult_div.
    def enterOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        self.help_operation(ctx, (ctx.mult, Mult), (ctx.div, Div), (ctx.mod, Mod))
        pass

    # Exit a parse tree produced by cParser#operation_mult_div.
    def exitOperation_mult_div(self, ctx: cParser.Operation_mult_divContext):
        self.help_simplify(ctx, 2)
        pass

    # Enter a parse tree produced by cParser#operation_unary_plus_minus_not.
    def enterOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        self.help_operation(ctx, (ctx.plus, UPlus), (ctx.minus, UMinus), (ctx.not_, UNot),
                            (ctx.dref, UDeref)) # (ctx.rref, UReref),
        pass

    # Exit a parse tree produced by cParser#operation_unary_plus_minus_not.
    def exitOperation_unary_plus_minus_not(self, ctx: cParser.Operation_unary_plus_minus_notContext):
        self.help_simplify(ctx, 1)
        pass

    # Enter a parse tree produced by cParser#operation_brackets.
    def enterOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        # Can't use help operation function, because children are not required
        if ctx.break_:
            self.add(Break())
        elif ctx.continue_:
            self.add(Continue())
        pass

    # Exit a parse tree produced by cParser#operation_brackets.
    def exitOperation_brackets(self, ctx: cParser.Operation_bracketsContext):
        pass

    # Enter a parse tree produced by cParser#constant.
    def enterConstant(self, ctx: cParser.ConstantContext):
        if ctx.int_:
            value = ctx.getText()
            self.add(CInt(value))
        elif ctx.char_:
            value = ctx.getText()[1:-1]  # Cut 'a' to a
            self.add(CChar(value))
        elif ctx.float_:
            value = ctx.getText()
            self.add(CFloat(value))
        elif ctx.str_:
            value = ctx.getText()[1:-1]  # Cut "a" to a
            self.add(CString(value))
        pass

        # Exit a parse tree produced by cParser#constant.

    def exitConstant(self, ctx: cParser.ConstantContext):
        pass

    # Enter a parse tree produced by cParser#return_op.
    def enterReturn_op(self, ctx: cParser.Return_opContext):
        self.add(Return("return"))
        pass

    # Exit a parse tree produced by cParser#return_op.
    def exitReturn_op(self, ctx: cParser.Return_opContext):
        if not self.has_childeren(ctx):
            return
        self.simplify(1)
        pass
