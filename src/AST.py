# https://medium.com/@raguiar2/building-a-working-calculator-in-python-with-antlr-d879e2ea9058 (accessed on 6/3/2020 14:31)

from src.Node import *
from src.symbolTable import *


def generate_LLVM(ast):
    output = ""
    retval = False
    formatTypes = list()
    # If the ast node is a sequence then the nodes below it can be instructions but this node means nothing at the moment
    if isinstance(ast.node, StatementSequence):
        for child in ast.children:
            tempret = generate_LLVM(child)
            output += tempret[0]
            retval = tempret[1]
            for formatType in tempret[2]:
                if formatType not in formatTypes:
                    formatTypes.append(formatType)

    # If the type is assignment then we need first calculate the right hand value of the assignment
    if isinstance(ast.node, Assign):
        output += generate_LLVM(ast.children[1])[0]
        type = ""
        if isinstance(ast.children[0].node, VChar):
            type = "i8"
        elif isinstance(ast.children[0].node, VInt):
            type = "i32"
        elif isinstance(ast.children[0].node, VFloat):
            type = "float"
        # If The right side is a variable then take the variable name not the node type
        if isinstance(ast.children[1].node, Variable):
            output += ast.node.get_LLVM().format(type + "*", "@", str(ast.children[1].node.value), type, "@",
                                                 str(ast.children[0].node.value))
        else:  # If the node wasnt a variable take the node id
            output += ast.node.get_LLVM().format(type, "%", str(ast.children[1]), type, "@",
                                                 str(ast.children[0].node.value))

    # If we encounter a variable then we do not need to do anything because it is already assigned
    elif isinstance(ast.node, Variable):
        return "", retval, formatTypes

    # If the node is a constant then we add the assignment of the constant
    elif isinstance(ast.node, Constant):
        type = ""
        val = ""
        neutralval = ""
        if isinstance(ast.node, CChar):
            type = "i8"
            val = str(ord(ast.node.value[1]))
            neutralval = "0"
        elif isinstance(ast.node, CInt):
            type = "i32"
            val = str(ast.node.value)
            neutralval = "0"
        elif isinstance(ast.node, CFloat):
            type = "float"
            val = str(ast.node.value)
            neutralval = "0.0"
        output += BPlus().get_LLVM(type == "float").format("%", str(ast), type, "", val, "", neutralval)

    # If we encounter an operator operate then we need to operate on its children
    elif isinstance(ast.node, Operate):
        # generate LLVM for the left and right side of the operator
        tempret1 = generate_LLVM(ast.children[0])
        output += tempret1[0]
        tempret2 = generate_LLVM(ast.children[1])
        output += tempret2[0]
        retval = tempret1[1] + tempret2[1]
        is_float = False
        for formatType in tempret1[2]:
            if formatType not in formatTypes:
                formatTypes.append(formatType)
        for formatType in tempret2[2]:
            if formatType not in formatTypes:
                formatTypes.append(formatType)
        # execute operator
        type = ast.getType()
        if type == "float":
            type = "float"
            is_float = True
        elif type == "int":
            type = "i32"
        elif type == "char":
            type = "i8"
        # Both variable
        if isinstance(ast.children[0].node, Variable) and isinstance(ast.children[1].node, Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            tempvar2 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"
            output += "%" + tempvar2 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[1].node.value) + "\n"
            output += ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1,
                                                         "%", tempvar2)
        elif isinstance(ast.children[0].node, Variable):  # First variable
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"
            output += ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1,
                                                         "%", str(ast.children[1]))
        elif isinstance(ast.children[1].node, Variable):  # Second variable
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[1].node.value) + "\n"
            output += ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", str(ast.children[0]),
                                                         "%", tempvar1)
        else:  # No variable
            output += ast.node.get_LLVM(is_float).format("%", str(ast), type, "%", ast.children[0],
                                                         "%", str(ast.children[1]))
    # If we encounter an operator operate then we need to operate on its children
    elif isinstance(ast.node, Compare):
        # generate LLVM for the left and right side of the operator
        tempret1 = generate_LLVM(ast.children[0])
        output += tempret1[0]
        tempret2 = generate_LLVM(ast.children[1])
        output += tempret2[0]
        retval = tempret1[1] + tempret2[1]
        is_float = False
        for formatType in tempret1[2]:
            if formatType not in formatTypes:
                formatTypes.append(formatType)
        for formatType in tempret2[2]:
            if formatType not in formatTypes:
                formatTypes.append(formatType)
        # execute operator
        type = ast.getType()
        if type == "float":
            type = "float"
            is_float = True
        elif type == "int":
            type = "i32"
        elif type == "char":
            type = "i8"
        # Both variable
        if isinstance(ast.children[0].node, Variable) and isinstance(ast.children[1].node, Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"
            if type == "float":
                tempvar1_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar1_ + " = fptosi float %" + tempvar1 + " to i32\n"
                tempvar1 = tempvar1_

            tempvar2 = "t" + str(ast.node.get_id())
            output += "%" + tempvar2 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[1].node.value) + "\n"
            if type == "float":
                tempvar2_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar2_ + " = fptosi float %" + tempvar2 + " to i32\n"
                tempvar2 = tempvar2_

            tempSave = "t" + str(ast.node.get_id())
            if type == "float":
                output += ast.node.get_LLVM().format("%", tempSave, "i32", "%", tempvar1,
                                                     "%", tempvar2)
                output += "%" + str(ast) + " = uitofp i1 %" + tempSave + " to float\n"
            else:
                output += ast.node.get_LLVM().format("%", tempSave, type, "%", tempvar1,
                                                     "%", tempvar2)
                output += "%" + str(ast) + " = zext i1 %" + tempSave + " to " + type + "\n"

        elif isinstance(ast.children[0].node, Variable):  # First variable
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"
            if type == "float":
                tempvar1_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar1_ + " = fptosi float %" + tempvar1 + " to i32\n"
                tempvar1 = tempvar1_

            tempvar2 = "t" + str(ast.node.get_id())
            neutralVal = ""
            if type == "float":
                neutralVal = "0.0"
            else:
                neutralVal = "0"
            output += BPlus().get_LLVM(is_float).format("%", tempvar2, type, "%", str(ast.children[1]), "", neutralVal)
            if type == "float":
                tempvar2_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar2_ + " = fptosi float %" + tempvar2 + " to i32\n"
                tempvar2 = tempvar2_

            tempSave = "t" + str(ast.node.get_id())
            if type == "float":
                output += ast.node.get_LLVM().format("%", tempSave, "i32", "%", tempvar1,
                                                     "%", tempvar2)
                output += "%" + str(ast) + " = uitofp i1 %" + tempSave + " to float\n"
            else:
                output += ast.node.get_LLVM().format("%", tempSave, type, "%", tempvar1,
                                                     "%", tempvar2)
                output += "%" + str(ast) + " = zext i1 %" + tempSave + " to " + type + "\n"

        elif isinstance(ast.children[1].node, Variable):  # Second variable
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[1].node.value) + "\n"
            if type == "float":
                tempvar1_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar1_ + " = fptosi float %" + tempvar1 + " to i32\n"
                tempvar1 = tempvar1_

            tempvar2 = "t" + str(ast.node.get_id())
            neutralVal = "0"
            if type == "float":
                neutralVal = "0.0"

            output += BPlus().get_LLVM(is_float).format("%", tempvar2, type, "%", str(ast.children[0]), "", neutralVal)
            if type == "float":
                tempvar2_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar2_ + " = fptosi float %" + tempvar2 + " to i32\n"
                tempvar2 = tempvar2_

            tempSave = "t" + str(ast.node.get_id())
            if type == "float":
                output += ast.node.get_LLVM().format("%", tempSave, "i32", "%", tempvar2,
                                                     "%", tempvar1)
                output += "%" + str(ast) + " = uitofp i1 %" + tempSave + " to float\n"
            else:
                output += ast.node.get_LLVM().format("%", tempSave, type, "%", tempvar2,
                                                     "%", tempvar1)
                output += "%" + str(ast) + " = zext i1 %" + tempSave + " to " + type + "\n"
        else:  # No variable
            tempvar1 = "t" + str(ast.node.get_id())
            neutralVal = "0"
            if type == "float":
                neutralVal = "0.0"

            output += BPlus().get_LLVM(is_float).format("%", tempvar1, type, "%", str(ast.children[0]), "", neutralVal)
            if type == "float":
                tempvar1_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar1_ + " = fptosi float %" + tempvar1 + " to i32\n"
                tempvar1 = tempvar1_

            tempvar2 = "t" + str(ast.node.get_id())
            output += BPlus().get_LLVM(is_float).format("%", tempvar2, type, "%", str(ast.children[1]), "", neutralVal)
            if type == "float":
                tempvar2_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar2_ + " = fptosi float %" + tempvar2 + " to i32\n"
                tempvar2 = tempvar2_

            tempSave = "t" + str(ast.node.get_id())
            if type == "float":
                output += ast.node.get_LLVM().format("%", tempSave, "i32", "%", tempvar1,
                                                     "%", tempvar2)
                output += "%" + str(ast) + " = uitofp i1 %" + tempSave + " to float\n"
            else:
                output += ast.node.get_LLVM().format("%", tempSave, type, "%", tempvar1,
                                                     "%", tempvar2)
                output += "%" + str(ast) + " = zext i1 %" + tempSave + " to " + type + "\n"

    elif isinstance(ast.node, UPlus):
        is_float = False
        type = "i32"
        if "float" == ast.getType():
            is_float = True
            type = "float"
        elif ast.getType() == "char":
            type = "i8"
        tempvar1 = str(ast.children[0])
        if isinstance(ast.children[0], Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"

        output += UPlus().get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1)

    elif isinstance(ast.node, UMinus):
        is_float = False
        type = "i32"
        if "float" == ast.getType():
            is_float = True
            type = "float"
        elif ast.getType() == "char":
            type = "i8"

        tempvar1 = str(ast.children[0])
        if isinstance(ast.children[0], Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"

        output += UMinus().get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1)

    elif isinstance(ast.node, UNot):
        is_float = False
        type = "i32"
        tempvar = "t" + str(ast.node.get_id())
        if "float" == ast.getType():
            is_float = True
            type = "float"
        elif ast.getType() == "char":
            type = "i8"

        tempvar = str(ast.node.get_id())
        if isinstance(ast.node, Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type + ", " + type + "* " + "@" + str(
                ast.children[0].node.value) + "\n"
            if type == "float":
                tempvar1_ = "t" + str(ast.node.get_id())
                output += "%" + tempvar1_ + " = fptosi float %" + tempvar1 + " to i32\n"
                tempvar1 = tempvar1_

            tempvar2 = "t" + str(ast.node.get_id())
            if type == "float":
                output += UNot().get_LLVM(is_float).format("%", tempvar2, "i32", "%", tempvar1)
                output += "%" + str(ast) + " = uitofp i1 %" + tempvar2 + " to float\n"
            else:
                output += UNot().get_LLVM(is_float).format("%", str(ast), type, "%", tempvar1)

    if isinstance(ast.node, Print):
        tempvar1 = ""
        formatType = ""
        type = ""
        # Check the variable type of the node
        if isinstance(ast.children[0].node, VInt) or isinstance(ast.children[0].node, CInt):
            formatType = "d"
            type = "i32"
            type_ = "i32"
        elif isinstance(ast.children[0].node, VFloat) or isinstance(ast.children[0].node, CFloat):
            formatType = "f"
            type = "double"
            type_ = "float"
        elif isinstance(ast.children[0].node, VChar) or isinstance(ast.children[0].node, CChar):
            formatType = "c"
            type = "i8"
            type_ = "i8"

        if formatType not in formatTypes:
            formatTypes.append(formatType)

        if isinstance(ast.children[0].node, CChar):
            output += 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str{}, i32 0, i32 0), {} {})\n'.format(
                formatType, type, ord(ast.children[0].node.value[1]))
        elif isinstance(ast.children[0].node, Variable):
            tempvar1 = "t" + str(ast.node.get_id())
            output += "%" + tempvar1 + " = load " + type_ + ", " + type_ + "* " + "@" + str(
                ast.children[0].node.value) + "\n"
            if type == "double":
                tempvar2 = "t" + str(ast.node.get_id())
                output += "%" + tempvar2 + " = fpext float %" + tempvar1 + " to double\n"
                tempvar1 = tempvar2
            output += 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str{}, i32 0, i32 0), {} %{})\n'.format(
                formatType, type, tempvar1)
        else:
            output += 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str{}, i32 0, i32 0), {} {})\n'.format(
                formatType, type, ast.children[0].node.value)
        return output, True, formatTypes
    return output, retval, formatTypes


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
        output += "define i32 @main() {\n"
        retval = generate_LLVM(self)
        output += retval[0]

        output += "ret i32 0\n"
        output += "}\n\n"

        # If we need to print then create the print function
        if retval[1]:
            if "c" in retval[2]:
                output += '@.strc = private unnamed_addr constant [4 x i8] c"%c\\0A\\00", align 1\n'
            if "d" in retval[2]:
                output += '@.strd = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1\n'
            if "f" in retval[2]:
                output += '@.strf = private unnamed_addr constant [4 x i8] c"%f\\0A\\00", align 1\n'
            output += 'declare i32 @printf(i8*, ...)\n'

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
