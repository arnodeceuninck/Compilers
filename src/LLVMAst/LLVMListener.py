# Generated from /home/arno/Documents/Compilers/input/c.g4 by ANTLR 4.8
from antlr4 import *
from gen_llvm.llvmParser import llvmParser
from src.LLVMAst.LLVMAst import *


# Check whether a context has real children (and not only a connection to the next node)
def has_children(ctx: ParserRuleContext):
    return ctx.getChildCount() > 1


# This class defines a complete listener for a parse tree produced by cParser.
class LLVMListener(ParseTreeListener):
    def __init__(self):
        self.trees = []  # A stack containing all subtrees

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
    def enterStart_rule(self, ctx: llvmParser.Start_ruleContext):
        self.add(LLVMCode())
        pass

    # Exit a parse tree produced by cParser#start_rule.
    def exitStart_rule(self, ctx: llvmParser.Start_ruleContext):
        self.simplify(len(self.trees) - 1)
        pass

    # Enter a parse tree produced by llvmParser#function.
    def enterFunction(self, ctx: llvmParser.FunctionContext):
        self.add(LLVMFunction(name=ctx.name.text, rettype=ctx.rettype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#function.
    def exitFunction(self, ctx: llvmParser.FunctionContext):
        self.simplify(1)  # Only the operation sequence (argument list is not yet supported)
        pass

    # Enter a parse tree produced by llvmParser#scope.
    def enterScope(self, ctx: llvmParser.ScopeContext):
        pass

    # Exit a parse tree produced by llvmParser#scope.
    def exitScope(self, ctx: llvmParser.ScopeContext):
        pass

    # Enter a parse tree produced by llvmParser#operation_sequence.
    def enterOperation_sequence(self, ctx: llvmParser.Operation_sequenceContext):
        self.add(LLVMOperationSequence())
        pass

    # Exit a parse tree produced by llvmParser#operation_sequence.
    def exitOperation_sequence(self, ctx: llvmParser.Operation_sequenceContext):
        tree = self.trees[len(self.trees) - 1]
        children = 0
        while not isinstance(tree, LLVMOperationSequence):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]
        self.simplify(children)
        pass

    # Enter a parse tree produced by llvmParser#operation.
    def enterOperation(self, ctx: llvmParser.OperationContext):
        pass

    # Exit a parse tree produced by llvmParser#operation.
    def exitOperation(self, ctx: llvmParser.OperationContext):
        pass

    # Enter a parse tree produced by llvmParser#store.
    def enterStore(self, ctx: llvmParser.StoreContext):
        self.add(LLVMStore(ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#store.
    def exitStore(self, ctx: llvmParser.StoreContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by llvmParser#assignment.
    def enterAssignment(self, ctx: llvmParser.AssignmentContext):
        self.add(LLVMAssignment())
        pass

    # Exit a parse tree produced by llvmParser#assignment.
    def exitAssignment(self, ctx: llvmParser.AssignmentContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by llvmParser#rvalue.
    def enterRvalue(self, ctx: llvmParser.RvalueContext):
        pass

    # Exit a parse tree produced by llvmParser#rvalue.
    def exitRvalue(self, ctx: llvmParser.RvalueContext):
        pass

    # Enter a parse tree produced by llvmParser#alocation.
    def enterAlocation(self, ctx: llvmParser.AlocationContext):
        self.add(LLVMAllocate(ctx.optype.getText(), ctx.align_index.text))
        pass

    # Exit a parse tree produced by llvmParser#alocation.
    def exitAlocation(self, ctx: llvmParser.AlocationContext):
        pass

    # Enter a parse tree produced by llvmParser#addition.
    def enterAddition(self, ctx: llvmParser.AdditionContext):
        self.add(LLVMAddition(optype=ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#addition.
    def exitAddition(self, ctx: llvmParser.AdditionContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by llvmParser#value.
    def enterValue(self, ctx: llvmParser.ValueContext):
        pass

    # Exit a parse tree produced by llvmParser#value.
    def exitValue(self, ctx: llvmParser.ValueContext):
        pass

    # Enter a parse tree produced by llvmParser#const_int.
    def enterConst_int(self, ctx: llvmParser.Const_intContext):
        self.add(LLVMConst(ctx.getText()))
        pass

    # Exit a parse tree produced by llvmParser#const_int.
    def exitConst_int(self, ctx: llvmParser.Const_intContext):
        pass

    # Enter a parse tree produced by llvmParser#return_.
    def enterReturn_(self, ctx: llvmParser.Return_Context):
        pass

    # Exit a parse tree produced by llvmParser#return_.
    def exitReturn_(self, ctx: llvmParser.Return_Context):
        pass

    # Enter a parse tree produced by llvmParser#variable.
    def enterVariable(self, ctx: llvmParser.VariableContext):
        self.add(LLVMVariable(name=ctx.var.text))
        pass

    # Exit a parse tree produced by llvmParser#variable.
    def exitVariable(self, ctx: llvmParser.VariableContext):
        pass

    # Enter a parse tree produced by llvmParser#type_.
    def enterType_(self, ctx: llvmParser.Type_Context):
        pass

    # Exit a parse tree produced by llvmParser#type_.
    def exitType_(self, ctx: llvmParser.Type_Context):
        pass

    # Enter a parse tree produced by llvmParser#function_call.
    def enterFunction_call(self, ctx: llvmParser.Function_callContext):
        pass

    # Exit a parse tree produced by llvmParser#function_call.
    def exitFunction_call(self, ctx: llvmParser.Function_callContext):
        pass

    # Enter a parse tree produced by llvmParser#print_function.
    def enterPrint_function(self, ctx: llvmParser.Print_functionContext):
        self.add(LLVMPrint())
        pass

    # Exit a parse tree produced by llvmParser#print_function.
    def exitPrint_function(self, ctx: llvmParser.Print_functionContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#print_str.
    def enterPrint_str(self, ctx: llvmParser.Print_strContext):
        self.add(LLVMPrintStr(ctx.var.text))
        pass

    # Exit a parse tree produced by llvmParser#print_str.
    def exitPrint_str(self, ctx: llvmParser.Print_strContext):
        pass

    # Enter a parse tree produced by llvmParser#declaration.
    def enterDeclaration(self, ctx: llvmParser.DeclarationContext):
        pass

    # Exit a parse tree produced by llvmParser#declaration.
    def exitDeclaration(self, ctx: llvmParser.DeclarationContext):
        pass
