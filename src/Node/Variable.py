from src.Node.AST import AST, StatementSequence, Assign


class Variable(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#af93ff")
        self.ptr = False  # e.g. int* a (in declaration), &a (deref in rvalue)
        self.const = False
        self.defined = False
        self.llvm_defined = False  # If the variable is already defined in llvm code

        self.reref = False  # e.g. *a

        self.array = False
        self.array_number = 0

        self.declaration = False

    def __str__(self):
        var_type = "const " if self.const else ""
        var_type += self.get_type()
        label = "Variable Type: {type}: {value}".format(type=var_type,
                                                        value=self.value)
        if self.array:
            label += "[{nr}]".format(nr=self.array_number)
        return '\t{name}[label=\"{label}\", fillcolor="{color}"] \n'.format(name=self.id(), label=label,
                                                                            color=self.color)

    def constant_folding(self):
        return False

    def get_type(self):
        raise Exception("Abstract function")
        # return self.type + ("*" if self.ptr else "")

    def getLLVMType(self, ignore_array=False):
        return ""

    def getFormatType(self):
        return ""

    def convertString(self, type):
        return ""

    def get_llvm_template(self):
        return self.llvm_load_template()

    # Variable should be llvm_formated, e.g. %1
    def llvm_load(self, variable: str):
        code = self.get_llvm_template()
        code = code.format(result=variable, type=self.get_llvm_type(), var=self.variable(store=True))
        AST.llvm_output += code

    def index_load(self, result, index):
        code = "{temp} = getelementptr inbounds {array_type}, {array_type}* {variable}, i64 0, i64 {index}\n"
        code += "{result} = load {type}, {type}* {temp}, align 4\n"
        code = code.format(result=result, temp=self.get_temp(), array_type=self.get_llvm_type(),
                           variable=self.variable(store=True), index=index)
        AST.llvm_output += code

    def get_align(self):
        return 0

    # The llvm code for a variable will only be generated if the parent is a statement sequence,
    # because then we will have to allocate the variable
    def llvm_code(self):
        if isinstance(self.parent, StatementSequence) and not self.parent.symbol_table.get_symbol_table(self.value)[
            self.value].llvm_defined:
            # Allocate the variable
            create_var = "\t{variable} = alloca {llvm_type}, align {align}\n".format(
                variable=self.variable(store=True),
                llvm_type=self.get_llvm_type(),
                align=self.get_align())
            AST.llvm_output += create_var
            self.parent.symbol_table.get_symbol_table(self.value)[self.value].llvm_defined = True
        return ""

    def comments(self, comment_out: bool = False):
        comment = self.value
        return self.comment_out(comment, comment_out)


class VInt(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_llvm_type(self, ignore_array=False) -> str:
        if not ignore_array and self.array:
            return "[{size} x {type}]".format(size=self.array_number, type=self.get_llvm_type(ignore_array=True))
        return "i32" + ("*" if self.ptr else "")

    def get_llvm_print_type(self) -> str:
        return "i32"

    def get_type(self):
        return "int" + ("*" if self.ptr else "")

    def get_format_type(self):
        return "d"

    def get_align(self, ignore_array=False):
        if self.array and not ignore_array:
            return 4 if self.array_number < 4 else 16
        return 4 + 4 * self.ptr

    def convert_template(self, type):
        if type == "int":
            return ""
        elif type == "char":
            return "\t{}{} = trunc i32 {}{} to i8\n"
        elif type == "float":
            return "\t{}{} = sitofp i32 {}{} to float\n"
        elif type == "double":
            return "\t{}{} = sitofp i32 {}{} to double\n"
        elif type == "bool":
            return "\t{}{} = trunc i32 {}{} to i1\n"


class VChar(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_llvm_type(self, ignore_array=False) -> str:
        if not ignore_array and self.array:
            return "[{size} x {type}]".format(size=self.array_number, type=self.get_llvm_type(ignore_array=True))
        return "i8" + ("*" if self.ptr else "")

    def get_type(self):
        return "char" + ("*" if self.ptr else "")

    def get_llvm_print_type(self) -> str:
        return "i8"

    def get_format_type(self):
        return "c"

    def get_align(self):
        return 1 + 7 * self.ptr

    def convert_template(self, type):
        if type == "int":
            return "\t{result} = zext i8 {value} to i32\n"
        elif type == "char":
            return None
        elif type == "float":
            return "\t{result} = uitofp i8 {value} to float\n"
        elif type == "double":
            return "\t{result} = uitofp i8 {value} to double\n"
        elif type == "bool":
            return "\t{result} = trunc i8 {value} to i1\n"


class VFloat(Variable):
    def __init__(self, value=""):
        Variable.__init__(self, value)

    def get_type(self):
        return "float" + ("*" if self.ptr else "")

    def get_llvm_type(self, ignore_array=False) -> str:
        if not ignore_array and self.array:
            return "[{size} x {type}]".format(size=self.array_number, type=self.get_llvm_type(ignore_array=True))
        return "float" + ("*" if self.ptr else "")

    def get_llvm_print_type(self) -> str:
        return "double"

    def get_format_type(self):
        return "f"

    def get_align(self):
        return 4 + 4 * self.ptr

    @staticmethod
    def convert_template(type):
        if type == "int":
            return "\t{result} = fptosi float {value} to i32\n"
        elif type == "char":
            return "\t{result} = fptoui float {value} to i8\n"
        elif type == "float":
            return ""
        elif type == "double":
            return "\t{result} = fpext float {value} to double\n"
        elif type == "bool":
            return "\t{result} = fptoui float {value} to i1\n"
