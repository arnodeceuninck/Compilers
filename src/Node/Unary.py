from src.Node.AST import Operator, AST, BoolClasses
from src.Node.constant import CBool

printString = '\tcall i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str{format_type}, i32 0, i32 0), {print_type} {value})\n'


class Unary(Operator):
    def __init__(self, value=""):
        Operator.__init__(self, value)
        self.funct = None

    def __str__(self):
        return '\t{name}[label="Unary Operator: {value}", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                          value=self.value,
                                                                                          color=self.color)

    def get_type(self):
        return self[0].get_type()  # Only one type as argument

    def comments(self, comment_out: bool = True) -> str:
        comment = self.value + " " + self[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        type = self.get_llvm_type()

        code = self.get_llvm_template()
        code = code.format(result=self.variable(), type=type, value=self[0].variable())

        AST.llvm_output += code


class UPlus(Unary):
    def __init__(self, value="+"):
        Unary.__init__(self, value)
        self.funct = lambda args: +args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fadd {type} {value}, 0.0\n"
        else:
            return "\t{result} = add {type} {value}, 0\n"


class UMinus(Unary):
    def __init__(self, value="-"):
        Unary.__init__(self, value)
        self.funct = lambda args: -args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            return "\t{result} = fsub {type} 0.0, {value}\n"
        else:
            return "\t{result} = sub {type} 0, {value}\n"


class UDMinus(Unary):
    def __init__(self, value="--"):
        Unary.__init__(self, value)
        self.funct = lambda args: args[0] - 1


class UDPlus(Unary):
    def __init__(self, value="++"):
        Unary.__init__(self, value)
        self.funct = lambda args: args[0] - 1


class UNot(Unary):
    def __init__(self, value="!"):
        Unary.__init__(self, value)
        self.funct = lambda args: not args[0]

    def get_llvm_template(self) -> str:
        if self.get_type() == "float":
            template = "\t{{result}} = fcmp oeq {{type}} {neutral}, {{value}}\n"
        else:
            template = "\t{{result}} = icmp eq {{type}} {neutral}, {{value}}\n"
        template = template.format(neutral=str(self.get_neutral()))
        return template

    def llvm_code(self):
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        type = self.get_llvm_type()

        # We need to have the variable in order to have the correct translation when the parrent is the boolclasses
        # because we do not want to extend the i1 we have to keep it that way
        if isinstance(self.parent, BoolClasses):
            temp = self.variable(self.id())
        else:
            temp = self.get_temp()

        code = self.get_llvm_template()
        code = code.format(result=temp, type=type, value=self[0].variable())
        AST.llvm_output += code

        # if the parent is an if statement then do not convert the variable
        if isinstance(self.parent, BoolClasses):
            return
        bool_to_type = CBool.convert_template(self.get_type())
        bool_to_type = bool_to_type.format(result=self.variable(), value=temp)

        AST.llvm_output += bool_to_type


class ArrayIndex(Unary):
    def __init__(self, index=None):
        self.index = index
        Unary.__init__(self, "[{i}]".format(i=index))

    def get_type(self):
        try:
            return self[0].get_type()
        except:
            return None

    def get_llvm_type(self):
        try:
            return self[0].get_llvm_type(ignore_array=True)
        except:
            return None

    def get_llvm_template(self):
        code = "{temp_index} = sext {index_type} {index} to i64\n"
        code += "{temp} = getelementptr inbounds {array_type}, {array_type}* {variable}, i64 0, i64 {temp_index}\n"
        code += "{result} = load {type}, {type}* {temp}, align {align}\n"  # NOTE: not the array align
        return code

    def get_align(self):
        return self[0].get_align(ignore_array=True)

    def comments(self, comment_out=True):
        comment = self[0].value + self.value
        return self.comment_out(comment, comment_out)

    def llvm_code(self):
        # print("Index yeet")
        AST.llvm_output += self.comments()

        self[1].llvm_code()
        self[0].llvm_code()

        code = self.get_llvm_template()
        code = code.format(temp=self.get_temp(), array_type=self[0].get_llvm_type(), variable=self[0].variable(store=True),
                           index=self[1].variable(),
                           result=self.variable(), type=self[0].get_llvm_type(ignore_array=True),
                           align=self.get_align(), temp_index=self.get_temp(), index_type=self[1].get_llvm_type())

        AST.llvm_output += code


class Print(Unary):
    def __init__(self, value="printf"):
        Unary.__init__(self, value)

    def get_type(self):
        return "function"

    def llvm_code(self):
        AST.print = True

        # Generate LLVM for the node that needs to be printed
        self[0].llvm_code()

        AST.llvm_output += self.comments()

        format_type = self[0].get_format_type()
        print_type = self[0].get_llvm_print_type()

        variable = self[0].variable()
        # Because you can't print floats
        if print_type == "double":
            convert_code = self[0].convert_template("double")
            convert_code = convert_code.format(result=self.variable(), value=self[0].variable())
            variable = self.variable()
            AST.llvm_output += convert_code

        print_code = printString.format(format_type=format_type, print_type=print_type, value=variable)
        AST.llvm_output += print_code

    def comments(self, comment_out=True):
        comment = "Print " + self[0].comments(comment_out=False)
        return self.comment_out(comment, comment_out)
