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
        self.type_ctr = 0 # Increases when expecting a type, must be uses when a type is twice, e.g. in store, we only want to add one type to the tree
        self.disable_arg_list = False # Must be disabled on function call (for argument list with printf)
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
        self.add(LLVMFunction(name=ctx.name.text))
        self.type_ctr += 1 # Expecting return type
        pass

    # Exit a parse tree produced by llvmParser#function.
    def exitFunction(self, ctx: llvmParser.FunctionContext):
        opseq = self.trees.pop()
        args = self.trees.pop()
        type = self.trees.pop()
        function = self.trees.pop()
        function.rettype = type
        self.add(function)
        self.add(args)
        self.add(opseq)
        self.simplify(2)
        pass

        # Enter a parse tree produced by llvmParser#own_function.

    # Enter a parse tree produced by llvmParser#function_call.
    def enterFunction_call(self, ctx: llvmParser.Function_callContext):
        self.disable_arg_list = True
        self.add(LLVMFunctionUse(name=ctx.fname.text))
        self.type_ctr += 1 # Expecting return type
        pass

    # Exit a parse tree produced by llvmParser#function_call.
    def exitFunction_call(self, ctx: llvmParser.Function_callContext):
        args = self.trees.pop()
        type = self.trees.pop()
        funccall = self.trees.pop()
        funccall.rettype = type
        self.add(funccall)
        self.add(args)
        self.simplify(1)
        self.disable_arg_list = False
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
        self.add(LLVMStore())
        self.type_ctr += 1 # Expecting store type
        pass

    # Exit a parse tree produced by llvmParser#store.
    def exitStore(self, ctx: llvmParser.StoreContext):
        v1 = self.trees.pop()
        v2 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.type = type
        self.add(op)
        self.add(v2)
        self.add(v1)
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
        self.add(LLVMAllocate(ctx.align_index.text, ctx.global_))
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#alocation.
    def exitAlocation(self, ctx: llvmParser.AlocationContext):
        type = self.trees.pop()
        allocation = self.trees.pop()
        allocation.type = type
        self.add(allocation)
        pass

    # Enter a parse tree produced by llvmParser#binary.
    def enterBinary(self, ctx: llvmParser.BinaryContext):
        self.add(LLVMBinaryOperation(operation=ctx.op.text))
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#binary.
    def exitBinary(self, ctx: llvmParser.BinaryContext):
        v1 = self.trees.pop()
        v2 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.optype = type
        self.add(op)
        self.add(v2)
        self.add(v1)
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
        self.add(LLVMReturn())
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#return_.
    def exitReturn_(self, ctx: llvmParser.Return_Context):
        v1 = None
        if ctx.var:
            v1 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.type = type
        self.add(op)
        if ctx.var:
            self.add(v1)
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
        if self.type_ctr:
            self.add(LLVMType(ctx.getText()))
            self.type_ctr -= 1
        pass

    # Exit a parse tree produced by llvmParser#normal_type.
    def exitNormal_type(self, ctx: llvmParser.Normal_typeContext):
        pass

    # Enter a parse tree produced by llvmParser#array_type.
    def enterArray_type(self, ctx: llvmParser.Array_typeContext):
        if self.type_ctr:
            self.add(LLVMArrayType(ctx.max_count.text))
            self.type_ctr += 1
        pass

    # Exit a parse tree produced by llvmParser#array_type.
    def exitArray_type(self, ctx: llvmParser.Array_typeContext):
        if self.type_ctr:
            type = self.trees.pop()
            array = self.trees.pop()
            array.type = type
            self.add(array)
            self.type_ctr -= 1
        pass

    # Enter a parse tree produced by llvmParser#argument_list.
    def enterArgument_list(self, ctx: llvmParser.Argument_listContext):
        if self.disable_arg_list:
            return
        self.add(LLVMArgumentList())
        pass

    # Exit a parse tree produced by llvmParser#argument_list.
    def exitArgument_list(self, ctx: llvmParser.Argument_listContext):
        if self.disable_arg_list:
            return
        tree = self.trees[len(self.trees) - 1]
        children = 0
        while not isinstance(tree, LLVMArgumentList):
            children += 1
            tree = self.trees[len(self.trees) - 1 - children]
        self.simplify(children)
        pass

    # Enter a parse tree produced by llvmParser#argument.
    def enterArgument(self, ctx: llvmParser.ArgumentContext):
        if self.disable_arg_list:
            return
        self.add(LLVMArgument())
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#argument.
    def exitArgument(self, ctx: llvmParser.ArgumentContext):
        if self.disable_arg_list:
            return
        type = self.trees.pop()
        op = self.trees.pop()
        op.type = type
        self.add(op)
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

    # Enter a parse tree produced by llvmParser#typed_variable.
    def enterTyped_variable(self, ctx: llvmParser.Typed_variableContext):
        # self.add(LLVMUseArgument())
        self.type_ctr += 1  # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#typed_variable.
    def exitTyped_variable(self, ctx: llvmParser.Typed_variableContext):
        v1 = self.trees.pop()
        type = self.trees.pop()
        v1.type = type
        self.add(v1)
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
        self.add(LLVMStringType(ctx.c_count.text))
        pass

    # Exit a parse tree produced by llvmParser#string_argument.
    def exitString_argument(self, ctx: llvmParser.String_argumentContext):
        v1 = self.trees.pop()
        type = self.trees.pop()
        v1.type = type
        self.add(v1)
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
        self.add(LLVMConditionalBranch())
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#conditional_branch.
    def exitConditional_branch(self, ctx: llvmParser.Conditional_branchContext):
        v1 = self.trees.pop()
        v2 = self.trees.pop()
        v3 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.optype = type
        self.add(op)
        self.add(v3)
        self.add(v2)
        self.add(v1)
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
        self.add(LLVMDeclare(ctx.fname.text))
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#declaration.
    def exitDeclaration(self, ctx: llvmParser.DeclarationContext):
        v1 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.type = type
        self.add(op)
        self.add(v1)
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#load.
    def enterLoad(self, ctx: llvmParser.LoadContext):
        self.add(LLVMLoad())
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#load.
    def exitLoad(self, ctx: llvmParser.LoadContext):
        v1 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.type = type
        self.add(op)
        self.add(v1)
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#extension.
    def enterExtension(self, ctx: llvmParser.ExtensionContext):
        self.add(LLVMExtension(ctx.op.text))
        self.type_ctr += 2 # Expecting type from and to
        pass

    # Exit a parse tree produced by llvmParser#extension.
    def exitExtension(self, ctx: llvmParser.ExtensionContext):
        type_to = self.trees.pop()
        v2 = self.trees.pop()
        type_from = self.trees.pop()
        op = self.trees.pop()
        op.type_from = type_from
        op.type_to = type_to
        self.add(op)
        self.add(v2)
        self.simplify(1)
        pass

    # Enter a parse tree produced by llvmParser#compare.
    def enterCompare(self, ctx: llvmParser.CompareContext):
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#compare.
    def exitCompare(self, ctx: llvmParser.CompareContext):
        v1 = self.trees.pop()
        v2 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.optype = type
        self.add(op)
        self.add(v2)
        self.add(v1)
        self.simplify(2)
        pass

    # Enter a parse tree produced by llvmParser#float_compare.
    def enterFloat_compare(self, ctx: llvmParser.Float_compareContext):
        self.add(LLVMFloatCompareOperation(operation=ctx.op.text))
        pass

    # Exit a parse tree produced by llvmParser#float_compare.
    def exitFloat_compare(self, ctx: llvmParser.Float_compareContext):
        pass

    # Enter a parse tree produced by llvmParser#int_compare.
    def enterInt_compare(self, ctx: llvmParser.Int_compareContext):
        self.add(LLVMIntCompareOperation(operation=ctx.op.text))
        pass

    # Exit a parse tree produced by llvmParser#int_compare.
    def exitInt_compare(self, ctx: llvmParser.Int_compareContext):
        pass

    # Enter a parse tree produced by llvmParser#ptr_index.
    def enterPtr_index(self, ctx: llvmParser.Ptr_indexContext):
        # index = ctx.index.text # Child will contain index
        self.add(LLVMArrayIndex())
        self.type_ctr += 1 # Expecting type
        pass

    # Exit a parse tree produced by llvmParser#ptr_index.
    def exitPtr_index(self, ctx: llvmParser.Ptr_indexContext):
        v1 = self.trees.pop()
        v2 = self.trees.pop()
        type = self.trees.pop()
        op = self.trees.pop()
        op.type = type
        self.add(op)
        self.add(v2)
        self.add(v1)
        self.simplify(2)  # Index and variable
        pass
