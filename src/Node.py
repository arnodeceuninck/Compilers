"""
!
"""


class Node:
    def __init__(self, value="", color="#9f9f9f"):
        self.value = value
        self.color = color

    def __str__(self):
        return '[label="{}", fillcolor="{}"] \n'.format(self.value, self.color)


class StatementSequence(Node):
    def __init__(self):
        Node.__init__(self, "Statement Sequence")


class Constant(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#FFD885")

    def __str__(self):
        return '[label="Constant {}", fillcolor="{}"] \n'.format(self.value, self.color)


class CInt(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "int"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)


class CFloat(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "float"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)


class CChar(Constant):
    def __init__(self, value=""):
        Constant.__init__(self, value)
        self.type = "char"

    def __str__(self):
        return '[label="Constant Type: {}: {}", fillcolor="{}"] \n'.format(self.type, self.value, self.color)


class Operator(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '[label="Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Unary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class UPlus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)


class UMinus(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)


class UNot(Unary):
    def __init__(self, value=""):
        Unary.__init__(self, value)


class Binary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class Compare(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Binary Operator Compare: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class LessT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class MoreT(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class LessOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class MoreOrEq(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class Equal(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class NotEqual(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class LogicAnd(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class LogicOr(Compare):
    def __init__(self, value=""):
        Compare.__init__(self, value)


class Operate(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)


class BMinus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)


class BPlus(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)


class Div(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)


class Mult(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)


class Mod(Operate):
    def __init__(self, value=""):
        Operate.__init__(self, value)


class Assign(Binary):
    def __init__(self, value=""):
        Binary.__init__(self, value)

    def __str__(self):
        return '[label="Assign", fillcolor="{}"] \n'.format(self.color)


class Variable(Node):
    def __init__(self, value=""):
        Node.__init__(self, value, "#af93ff")
        self.type = ""
        self.ptr = False
        self.const = False

    def __str__(self):
        return '[label="Variable: {}", fillcolor="{}"] \n'.format(self.value, self.color)


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "int"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "float"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)
        self.type = "char"

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.type
        var_type += "*" if self.ptr else ""
        return '[label="Variable Type: {}: {}", fillcolor="{}"] \n'.format(var_type, self.value, self.color)
