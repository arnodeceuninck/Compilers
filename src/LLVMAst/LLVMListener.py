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
        self.simplify(2)
        pass

        # Enter a parse tree produced by llvmParser#own_function.

    # Enter a parse tree produced by llvmParser#function_call.
    def enterFunction_call(self, ctx: llvmParser.Function_callContext):
        self.add(LLVMFunction(name=ctx.fname.text, rettype=ctx.rettype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#function_call.
    def exitFunction_call(self, ctx: llvmParser.Function_callContext):
        self.simplify(1)
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
        if ctx.optype.array:
            type = LLVMArrayType(ctx.optype.array.max_count.text, ctx.optype.array.element_type.getText())
        else:
            type = LLVMType(ctx.optype.getText())
        self.add(LLVMAllocate(type, ctx.align_index.text, ctx.global_))
        pass

    # Exit a parse tree produced by llvmParser#alocation.
    def exitAlocation(self, ctx: llvmParser.AlocationContext):
        pass

    # Enter a parse tree produced by llvmParser#binary.
    def enterBinary(self, ctx: llvmParser.BinaryContext):
        self.add(LLVMBinaryOperation(operation=ctx.op.text, optype=ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#binary.
    def exitBinary(self, ctx: llvmParser.BinaryContext):
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
        self.add(LLVMConstInt(ctx.getText()))
        pass

    # Exit a parse tree produced by llvmParser#const_int.
    def exitConst_int(self, ctx: llvmParser.Const_intContext):
        pass

    # Enter a parse tree produced by llvmParser#const_float.
    def enterConst_float(self, ctx: llvmParser.Const_floatContext):
        self.add(LLVMConstFloat(ctx.getText()))
        pass

    # Exit a parse tree produced by llvmParser#const_float.
    def exitConst_float(self, ctx: llvmParser.Const_floatContext):
        pass

    # Enter a parse tree produced by llvmParser#return_.
    def enterReturn_(self, ctx: llvmParser.Return_Context):
        self.add(LLVMReturn(ctx.rettype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#return_.
    def exitReturn_(self, ctx: llvmParser.Return_Context):
        if ctx.var:
            self.simplify(1)
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

    # Enter a parse tree produced by llvmParser#normal_type.
    def enterNormal_type(self, ctx: llvmParser.Normal_typeContext):
        pass

    # Exit a parse tree produced by llvmParser#normal_type.
    def exitNormal_type(self, ctx: llvmParser.Normal_typeContext):
        pass

    # Enter a parse tree produced by llvmParser#array_type.
    def enterArray_type(self, ctx: llvmParser.Array_typeContext):
        pass

    # Exit a parse tree produced by llvmParser#array_type.
    def exitArray_type(self, ctx: llvmParser.Array_typeContext):
        pass

    # Enter a parse tree produced by llvmParser#argument_list.
    def enterArgument_list(self, ctx: llvmParser.Argument_listContext):
        self.add(LLVMArgumentList())
        pass

    # Exit a parse tree produced by llvmParser#argument_list.
    def exitArgument_list(self, ctx: llvmParser.Argument_listContext):
        tree = self.trees[len(self.trees) - 1]
        children = 0
        while not isinstance(tree, LLVMArgumentList):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]
        self.simplify(children)
        pass

    # Enter a parse tree produced by llvmParser#argument.
    def enterArgument(self, ctx: llvmParser.ArgumentContext):
        self.add(LLVMArgument(ctx.getText()))
        pass

    # Exit a parse tree produced by llvmParser#argument.
    def exitArgument(self, ctx: llvmParser.ArgumentContext):
        pass

    # Enter a parse tree produced by llvmParser#use_arg_list.
    def enterUse_arg_list(self, ctx: llvmParser.Use_arg_listContext):
        self.add(LLVMUseArgumentList())
        pass

    # Exit a parse tree produced by llvmParser#use_arg_list.
    def exitUse_arg_list(self, ctx: llvmParser.Use_arg_listContext):
        tree = self.trees[len(self.trees) - 1]
        children = 0
        while not isinstance(tree, LLVMUseArgumentList):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]
        self.simplify(children)
        pass

    # Enter a parse tree produced by llvmParser#normal_argument.
    def enterNormal_argument(self, ctx: llvmParser.Normal_argumentContext):
        self.add(LLVMUseArgument(ctx.type_().getText()))
        pass

    # Exit a parse tree produced by llvmParser#normal_argument.
    def exitNormal_argument(self, ctx: llvmParser.Normal_argumentContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#print_str.
    def enterPrint_str(self, ctx: llvmParser.Print_strContext):
        self.add(LLVMPrintStr(ctx.var.text, ctx.c_count.text))
        pass

    # Exit a parse tree produced by llvmParser#print_str.
    def exitPrint_str(self, ctx: llvmParser.Print_strContext):
        pass

    # Enter a parse tree produced by llvmParser#string_argument.
    def enterString_argument(self, ctx: llvmParser.String_argumentContext):
        self.add(LLVMStringArgument(ctx.c_count.text))
        pass

    # Exit a parse tree produced by llvmParser#string_argument.
    def exitString_argument(self, ctx: llvmParser.String_argumentContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#label.
    def enterLabel(self, ctx: llvmParser.LabelContext):
        self.add(LLVMLabel(ctx.name.text))
        pass

    # Exit a parse tree produced by llvmParser#label.
    def exitLabel(self, ctx: llvmParser.LabelContext):
        pass

    # Enter a parse tree produced by llvmParser#conditional_branch.
    def enterConditional_branch(self, ctx: llvmParser.Conditional_branchContext):
        self.add(LLVMConditionalBranch(optype=ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#conditional_branch.
    def exitConditional_branch(self, ctx: llvmParser.Conditional_branchContext):
        self.simplify(3)
        pass

    # Enter a parse tree produced by llvmParser#normal_branch.
    def enterNormal_branch(self, ctx: llvmParser.Normal_branchContext):
        self.add(LLVMNormalBranch())
        pass

    # Exit a parse tree produced by llvmParser#normal_branch.
    def exitNormal_branch(self, ctx: llvmParser.Normal_branchContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#declaration.
    def enterDeclaration(self, ctx: llvmParser.DeclarationContext):
        self.add(LLVMDeclare(ctx.fname.text, ctx.rettype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#declaration.
    def exitDeclaration(self, ctx: llvmParser.DeclarationContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#load.
    def enterLoad(self, ctx: llvmParser.LoadContext):
        self.add(LLVMLoad(ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#load.
    def exitLoad(self, ctx: llvmParser.LoadContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#extension.
    def enterExtension(self, ctx: llvmParser.ExtensionContext):
        self.add(LLVMExtension(ctx.op.text, ctx.type_from.getText(), ctx.type_to.getText()))
        pass

    # Exit a parse tree produced by llvmParser#extension.
    def exitExtension(self, ctx: llvmParser.ExtensionContext):
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#float_compare.
    def enterFloat_compare(self, ctx: llvmParser.Float_compareContext):
        self.add(LLVMFloatCompareOperation(operation=ctx.op.text, optype=ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#float_compare.
    def exitFloat_compare(self, ctx: llvmParser.Float_compareContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by llvmParser#int_compare.
    def enterInt_compare(self, ctx: llvmParser.Int_compareContext):
        self.add(LLVMIntCompareOperation(operation=ctx.op.text, optype=ctx.optype.getText()))
        pass

    # Exit a parse tree produced by llvmParser#int_compare.
    def exitInt_compare(self, ctx: llvmParser.Int_compareContext):
        self.simplify(2)
        pass

    # Enter a parse tree produced by llvmParser#ptr_index.
    def enterPtr_index(self, ctx: llvmParser.Ptr_indexContext):
        type = LLVMArrayType(ctx.a_type.max_count.text, ctx.a_type.element_type.getText())
        index = ctx.index.text
        self.add(LLVMArrayIndex(type, index))
        pass

    # Exit a parse tree produced by llvmParser#ptr_index.
    def exitPtr_index(self, ctx: llvmParser.Ptr_indexContext):
        self.simplify(1)
        pass