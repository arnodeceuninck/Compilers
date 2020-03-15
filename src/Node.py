"""
!
"""


class Node:
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return '[label="{}", fillcolor="#9f9f9f"] \n'.format(self.value)


class Constant(Node):
    def __init__(self, value=""):
        Node.__init__(self, value)

    def __str__(self):
        return '[label="Constant {}", fillcolor="#FFD885"] \n'.format(self.value)


class CInt(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "int"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="#FFD885"] \n'.format(self.type, self.value)


class CFloat(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "float"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="#FFD885"] \n'.format(self.type, self.value)


class CChar(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "char"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="#FFD885"] \n'.format(self.type, self.value)


class Operator(Node):
    def __init__(self, value=""):
        Node.__init__(self, value)

    def __str__(self):
        return '[label="Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class UPlus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class UMinus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Binary(Node):
    def __init__(self, value=""):
        Node.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Compare(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class LessT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class MoreT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class LessOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class MoreOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Equal(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class NotEqual(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class LogicAnd(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class LogicOr(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Operate(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class BMinus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class BPlus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Div(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Mult(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Mod(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="#87f5ff"] \n'.format(self.value)


class Assign(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Assign", fillcolor="#87f5ff"] \n'.format(self.value)


class Variable(Node):
    def __init__(self, value=""):
        Node.__init__(self, value)
        self.type = ""
        self.ptr = False
        self.const = False

    def __str__(self):
        return '[label="Variable: {}", fillcolor="#af93ff"] \n'.format(self.value)


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "int"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="#af93ff"] \n'.format(var_type, self.value)


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "float"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="#af93ff"] \n'.format(var_type, self.value)


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "char"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="#af93ff"] \n'.format(var_type, self.value)
