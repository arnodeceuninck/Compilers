# https://medium.com/@raguiar2/building-a-working-calculator-in-python-with-antlr-d879e2ea9058 (accessed on 6/3/2020 14:31)

from src.Node import *
from src.symbolTable import *


def generate_LLVM(ast):
    output = ""
    retval = False
    # If the ast node is a sequence then the nodes below it can be instructions but this node means nothing at the moment
    if isinstance(ast.node, StatementSequence):
        for child in ast.children:
            tempret = generate_LLVM(child)
            output += tempret[0]
            retval = tempret[1]

    # If the type is assignment then we need first calculate the right hand value of the assignment
    if isinstance(ast.node, Assign):
        output += generate_LLVM(ast.children[1])[0]
        # If The left side is a variable then take the variable name not the node type
        if isinstance(ast.children[1].node, Variable):
            output += ast.node.get_LLVM().format("i32*", "@", str(ast.children[1].node.value), "i32", "@",
                                                 str(ast.children[0].node.value))
        else:  # If the node wasnt a variable take the node id
            output += ast.node.get_LLVM().format("i32", "%", str(ast.children[1]), "i32", "@",
                                                 str(ast.children[0].node.value))

    # If we encounter a variable then we do not need to do anything because it is already assigned
    elif isinstance(ast.node, Variable):
        return "", False

    # If the node is a constant then we add the assignment of the constant
    elif isinstance(ast.node, Constant):
        output += BPlus().get_LLVM().format("%", str(ast), "i32", "", str(ast.node.value), "", "0")

    # If we encounter an operator then we need to operate on its children
    elif isinstance(ast.node, Binary):
        # generate LLVM for the left and right side of the operator
        tempret1 = generate_LLVM(ast.children[0])
        output += tempret1[0]
        tempret2 = generate_LLVM(ast.children[1])
        output += tempret2[0]
        retval = tempret1 + tempret2
        # execute operator
        # Both variable
        if isinstance(ast.children[0].node, Variable) and isinstance(ast.children[1].node, Variable):
            tempvar1 = str(ast.node.get_id())
            tempvar2 = str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + "i32, " + "i32* " + "@" + str(ast.children[0].node.value) + "\n"
            output += "%" + tempvar2 + " = load " + "i32, " + "i32* " + "@" + str(ast.children[1].node.value) + "\n"
            output += ast.node.get_LLVM().format("%", str(ast), "i32", "%", tempvar1,
                                                 "%", tempvar2)
        elif isinstance(ast.children[0].node, Variable):  # First variable
            tempvar1 = str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + "i32, " + "i32* " + "@" + str(ast.children[0].node.value) + "\n"
            output += ast.node.get_LLVM().format("%", str(ast), "i32", "%", tempvar1,
                                                 "%", str(ast.children[1]))
        elif isinstance(ast.children[1].node, Variable):  # Second variable
            tempvar1 = str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + "i32, " + "i32* " + "@" + str(ast.children[1].node.value) + "\n"
            output += ast.node.get_LLVM().format("%", str(ast), "i32", "%", str(ast.children[0]),
                                                 "%", tempvar1)
        else:  # No variable
            output += ast.node.get_LLVM().format("%", str(ast), "i32", "%", ast.children[0],
                                                 "%", str(ast.children[1]))

    if isinstance(ast.node, Print):
        tempvar1 = ""
        if isinstance(ast.children[0].node, Variable):
            tempvar1 = str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + "i32, " + "i32* " + "@" + str(ast.children[0].node.value) + "\n"
            output += 'call void (i32) @print(i32 %{})\n'.format(tempvar1)
        else:
            output += 'call void (i32) @print(i32 {})\n'.format(321234141)
        return output, True
    return output, retval


class AST:
    symbol_table = SymbolTable()

    def __init__(self, node=None):
        self.node = node
        self.parent = None
        self.children = list()
        AST.symbol_table = SymbolTable()  # symbol table must reset after each test

    def childIndex(self, ast):
        return self.children.index(ast)

    def simplifyTree(self):
        for idx in range(0, len(self.children)):
            if len(self.children[idx].children) == 1:
                self.children[idx] = self.children[idx].children[0]
                self.children[idx].parent = self
                self.simplifyTree()
            else:
                self.children[idx].simplifyTree()

    def __str__(self):
        returnStr = ""
        if self.parent:
            returnStr += "N"
            returnStr += str(self.parent.childIndex(self))
            returnStr += str(self.parent)
        else:
            returnStr += "T"
        return returnStr

    def to_LLVM(self, filename):
        output = ""
        symbol_table = self.symbol_table.elements
        # generate variable declarations from the symbol table
        for var in symbol_table:
            # define all the variables
            LLVM_var_name = "@" + var
            LLVM_type = ""
            LLVM_align = "align"
            if symbol_table[var].type.const:
                LLVM_type = "constant"
            else:
                LLVM_type = "global"
            if symbol_table[var].type.type == "int":
                LLVM_type += " i32 0"
                LLVM_align += " 4"
            elif symbol_table[var].type.type == "float":
                LLVM_type += " float 0.0"
                LLVM_align += " 4"
            elif symbol_table[var].type.type == "char":
                LLVM_type += " i8 0"
                LLVM_align += " 1"
            output += LLVM_var_name + " = " + LLVM_type + ", " + LLVM_align + "\n"
        output += "\n"
        output += "define i32 @main() #0 {\n"
        retval = generate_LLVM(self)
        output += retval[0]

        output += "ret i32 0\n"
        output += "}\n\n"

        # If we need to print then create the print function
        if retval[1]:
            output += 'declare i32 @printf(i8*, ...)\n'
            output += '@format = private constant [8 x i8] c"d = %d\\0A\\00"\n'
            output += 'define void @print(i32 %a){\n'
            output += '%p = call i32 (i8*, ...)\n'
            output += '@printf(i8* getelementptr inbounds ([8 x i8],\n'
            output += '[8 x i8]* @format,\n'
            output += 'i32 0, i32 0),\n'
            output += 'i32 %a)\n'
            output += 'ret void\n'
            output += '}\n\n'

        # generate attributes of the function
        output += 'attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }\n'
        print(output)

        # Write output to the outputfile
        outputFile = open(filename, "w")
        outputFile.write(output)
        outputFile.close()

    def dotNode(self):
        # The output needs to be the id + The label itself
        output = str(self)
        output += str(self.node)

        for child in self.children:
            output += child.dotNode()

        return output

    def dotConnections(self):
        output = ""
        for child in self.children:
            output += str(self) + " -> " + str(child) + "\n"
            output += child.dotConnections()

        return output

    # Print the tree in dot
    def to_dot(self, filename):
        output = "Digraph G { \n"
        # Add symbol table
        output += str(self.symbol_table)
        output += "subgraph cluster_1 {\n"
        output += "node [style=filled, shape=rectangle, penwidth=2];\n"

        output += self.dotNode()
        output += self.dotConnections()

        output += "label = \"AST\";\n"
        output += "}\n"
        output += "}"

        outputFile = open(filename, "w")
        outputFile.write(output)
        outputFile.close()

    def plus(self, args):
        return args[0] + args[1]

    def min(self, args):
        return args[0] - args[1]

    def mult(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]

    def mod(self, args):
        return args[0] % args[1]

    def minU(self, args):
        return -args[0]

    def plusU(self, args):
        return +args[0]

    def traverse(self, func):
        func(self)
        for child in self.children:
            # func(child) # Why would you do this? you'll already do a func(self) when calling the traverse function of child
            child.traverse(func)

    # Does nothing with Comparison operators or logical operators
    def constant_folding(self):
        if isinstance(self.node, Variable):
            # You can't fold variables
            return False
        if isinstance(self.node, (CInt, CFloat)):
            # Ints and floats are already folded
            return True

        ready_to_continue_folding = True  # Only ready to continue if all children are
        for i in range(len(self.children)):
            # must iterate over i, because for child in self.children doesn't work by reference
            ready_to_continue_folding = self.children[i].constant_folding() and ready_to_continue_folding

        if not ready_to_continue_folding:
            # Can only continue folding if all children have folded properly
            return False

        funct = self.node.funct

        if funct is None:
            return False  # Can't continue folding if the function is unknown for folding

        args = list()
        # We need the right type of node, because compiling wrong type can cause issues
        node = None
        for child in self.children:
            try:
                args.append(float(child.node.value))
                # Set the type of the node to one of the children
                node = child.node
            except ValueError:
                return False  # Can't continue folding if one of the children isn't a float

        # Set the node type to the correct value
        self.node = node
        self.node.value = str(funct(args))
        self.children = list()

        return True

    def getType(self):
        args = list()
        for child in self.children:
            args.append(child.getType())
        return self.node.getType(args)
        # if isinstance(self.node, Variable):
        #     return self.symbol_table[self.node.value]
        # elif isinstance(self.node, CFloat):
        #     return "float"
        # elif isi
