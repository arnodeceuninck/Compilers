# TODO: limit all functions to an absolute maximum size of 20 lines (for readability)
class llvm:
    output = ""


# NOTE the parts referenced here are the parts described in the function get_llvm_print of the class Function
# This string belongs to the first part
stringVar = '@.str.{string_id} = private unnamed_addr constant [{string_len} x i8] c"{string_val}", align 1\n'
# This string belongs to the second part
stringArg = 'i8* getelementptr inbounds ([{string_len} x i8], [{string_len} x i8]* @.str.{string_id}, i32 0, i32 0)'
stringCall = '\tcall i32 (i8*, ...) @printf({string_arg})\n'

scanCall = "\tcall i32 (i8*, ...) @__isoc99_scanf({scan_arg})\n"


def llvm_code(ast):
    if isinstance(ast.parent, StatementSequence):
        llvm.output += "\n"
    llvm.output += ast.comments()

    if isinstance(ast, StatementSequence):
        llvm_statement_sequence(ast)
    elif isinstance(ast, If):
        llvm_if(ast)
    elif isinstance(ast, For):
        llvm_for(ast)
    elif isinstance(ast, While):
        llvm_while(ast)
    elif isinstance(ast, Operator):
        llvm_operator(ast)
    elif isinstance(ast, Function):
        llvm_function(ast)
    elif isinstance(ast, Arguments):
        llvm_arguments(ast)
    elif isinstance(ast, Include):
        llvm_include(ast)
    elif isinstance(ast, Comments):
        llvm_comments(ast)
    elif isinstance(ast, Constant):
        llvm_constant(ast)
    elif isinstance(ast, ReservedType):
        llvm_reserved_type(ast)
    elif isinstance(ast, Variable):
        llvm_variable(ast)
    else:
        raise Exception("Unknown AST")


def get_llvm_type(ast, ignore_array=False):
    if isinstance(ast, Operator):
        return llvm_type_operate(ast)
    elif isinstance(ast, Function):
        return llvm_type_function(ast)
    elif isinstance(ast, Constant):
        return llvm_type_constant(ast)
    elif isinstance(ast, Variable):
        return llvm_type_variable(ast, ignore_array)
    raise Exception("I didn't think the code would get this far")


def llvm_type_function(ast):
    if ast.return_type == "int":
        return 'i32'
    elif ast.return_type == "bool":
        return 'i1'
    elif ast.return_type == "float":
        return 'float'
    elif ast.return_type == "char":
        return 'i8'
    elif ast.return_type == "void":
        return 'void'


def llvm_operator(ast):
    if isinstance(ast, Binary):
        llvm_binary(ast)
    elif isinstance(ast, Unary):
        llvm_unary(ast)
    else:
        raise Exception("Unknown AST")


def llvm_binary(ast):
    if isinstance(ast, Assign):
        llvm_assign(ast)
    elif isinstance(ast, Compare):
        llvm_compare(ast)
    elif isinstance(ast, Operate):
        llvm_operate(ast)
    else:
        raise Exception("Unknown AST")


def llvm_include(ast):
    pass


def llvm_arguments(ast):
    pass


# The llvm code needs to be generated a special way and not in the main function
def llvm_function(ast):
    # Check if stdio is included if yes then use printf
    if AST.stdio:
        # Check if the function is either printf or scanf then try to use them
        if ast.value == "printf":
            get_llvm_print(ast)
            return
        if ast.value == "scanf":
            get_llvm_scan(ast)
            return

    if ast.function_type == "use":
        # Add the arguments for a function in a string
        # TODO: Check llvm arguments structure
        function_arguments = ""
        for child in ast.children[0]:
            if len(function_arguments):
                # Add a separator to the arguments, because there was a previous argument
                function_arguments += ", "
            # Generate the llvm code of the child
            llvm_code(child)
            # We know that the llvm code that has been generated has stored the value in the child as a variable
            if isinstance(child, Variable):
                function_arguments += get_llvm_type(child, child.array) + " " + variable(child)
            else:
                function_arguments += get_llvm_type(child) + " " + variable(child, store=True)

        initialization_line = ast.get_llvm_template()
        initialization_line = initialization_line.format(return_type=get_llvm_type(ast), name=ast.value,
                                                         arg_list=function_arguments)
        function_call = initialization_line
        # Store this value in a llvm variable if the return value is not a void otherwise
        # it just will be a function call
        if ast.return_type != "void":
            function_call = "\t" + variable(ast) + " = " + initialization_line
        llvm.output += function_call
        return
    elif ast.function_type == "declaration":
        return

    # If the function definition is that from main then generate the llvmcode
    global_llvm_code = ""
    if ast.value == "main" and ast.function_type == "definition":
        global_llvm_code = global_llvm(ast.parent)
    # Add the arguments for a function in a string
    # TODO: Check llvm arguments structure
    function_arguments = ""
    for child in ast.children[0]:
        if len(function_arguments):
            # Add a separator to the arguments, because there was a previous argument
            function_arguments += ", "
        # Add the type of the variable
        function_arguments += get_llvm_type(child)
        # Set this child already used in llvm as a variable
        child.get_symbol_table().get_symbol_table(child.value)[child.value].llvm_defined = True

    initialization_line = ast.get_llvm_template()
    initialization_line = initialization_line.format(return_type=get_llvm_type(ast), name=ast.value,
                                                     arg_list=function_arguments)
    llvm.output += initialization_line

    llvm.output += " {\n"

    # We add the global llvm code, if there is any though
    llvm.output += global_llvm_code

    # First get all arguments and store them in their variables to be readable
    if len(ast[0].children):
        llvm.output += "\t; fetching all arguments\n"
    for i in range(len(ast[0].children)):
        code = "\t{variable} = alloca {type}, align {align}\n"
        code += "\tstore {type} %{arg_nr}, {type}* {variable}\n"
        code = code.format(
            variable=variable(ast[0][i], store=True),
            type=get_llvm_type(ast[0][i]),
            align=ast[0][i].get_align(),
            arg_nr=str(i))

        llvm.output += code

    # Generate the llvm code
    for child in ast.children:
        llvm_code(child)
    llvm.output += "}\n"


def global_llvm(ast):
    llvm_output = llvm.output
    llvm.output = ""
    # Assure that we have the root statement sequence
    if ast.parent:
        return ""

    # Iterate over the children and only generate llvm_code for the children that are not function
    for child in ast.children:
        if isinstance(child, Function):
            continue
        # Generate the llvm_code
        llvm_code(child)

    # The llvm code is stored in the llvm code variable of the ast, we need to remove it from
    # there and store it into another return variable for this function
    ret_val = llvm.output
    llvm.output = llvm_output
    return ret_val


def llvm_assign(ast):
    llvm_code(ast[0])
    # First calculate the value to store
    llvm_code(ast[1])

    output = ""
    if isinstance(ast[0], UReref):
        # First we need to load the variable into a temporary var in which we can store the new value
        # Then we store the recently created value into the pointer
        code = ast.get_llvm_template()
        code = code.format(type=get_llvm_type(ast.children[0].children[0])[:-1],
                           temp=variable(ast[1], store=False),
                           location=variable(ast[0].children[0]))  # This line will do a lot more than expected
        output += code

        llvm.output += output
        return

    if isinstance(ast[0], Variable) and ast[0].array:
        code = "\t{temp} = getelementptr inbounds {array_type}, {array_type}* {var_location}, i64 0, i64 {index}\n"
        code += "\tstore {type} {value}, {type}* {temp}, align 4\n"
        code = code.format(type=get_llvm_type(ast.children[0], ignore_array=True),
                           array_type=get_llvm_type(ast.children[0]),
                           temp=ast.get_temp(),
                           var_location=variable(ast[0], store=True),
                           index=ast[0].array_number,
                           value=variable(ast[1]))
        output += code

        llvm.output += output
        return

    # We need to fetch the correct symbol table for the definition
    # Fetch the symbol table of the ast node
    symbol_table = ast.get_symbol_table()
    # We need to get the position of the variable as a child of the symbol_table node which is somewhere a parent
    var_position = ast.get_position()
    symbol_table_position = symbol_table[ast[0].value].position
    parent_nr = 1
    # We iterate over all the symbol tables and check if the item is already in the symbol table or not
    # we do this by checking if the position of the variable is before the declaration. If that is the case
    # Then we need to check the parent of the symbol table and so on so forth
    while var_position < symbol_table_position:
        var_position = ast.get_position(parent_nr)
        # Get the previous symbol table and get its parent to seek there
        symbol_table = symbol_table.parent
        symbol_table_position = symbol_table[ast[0].value].position
        # Increase the parent_nr so it will seek 1 parent deeper
        parent_nr += 1

    # If the variable is not in the global scope then we need to make a variable
    # And check if the corresponding item has already been defined in llvm
    if not symbol_table.is_global(ast[0].value) and not \
            symbol_table[ast[0].value].llvm_defined:
        create_var = "\t{variable} = alloca {llvm_type}, align {align}\n".format(
            variable=variable(ast[0], store=True),
            llvm_type=get_llvm_type(ast[0]),
            align=ast[0].get_align())
        output += create_var
        # The variable has been defined in llvm, so no more generating hereafter
        symbol_table[ast[0].value].llvm_defined = True
    code = ast.get_llvm_template()
    code = code.format(type=get_llvm_type(ast[0]), temp=variable(ast[1], store=False),
                       location=variable(ast[0], store=True))

    output += code

    llvm.output += output


def llvm_statement_sequence(ast):
    # ATTENTION we do not need to generate llvm code for children that are defined in the global scope as
    # variables # TODO
    llvm.output += ast.comments()
    for child in ast.children:
        # If there is no parent, we are the root statement sequence and the child is not a function
        # we do can not generate llvm_code
        if not ast.parent and not isinstance(child, Function):
            continue
        llvm_code(child)
    llvm.output += '\n'


def llvm_if(ast):
    # TODO: fix else

    condition = ast.children[0]
    llvm_code(condition)

    # Make both labels unique
    label_true = "iftrue" + str(ast.id())
    label_false = "iffalse" + str(ast.id())
    code = "\tbr {type} {var}, label %{label_true}, label %{label_false}\n"
    code = code.format(type="i1",
                       var=variable(condition),
                       label_true=label_true,
                       label_false=label_false)
    llvm.output += code

    # Make a unique label for the end
    label_end = "end" + str(ast.id())
    if_statement_sequence = ast.children[1]
    llvm.output += ast.label(label_true) + "\n"
    llvm_code(if_statement_sequence)
    goto(label_end)

    llvm.output += ast.label(label_false) + "\n"
    # If we have 3 children and an else statement, then generate the LLVM code for it
    if len(ast.children) == 3:
        else_statement_sequence = ast.children[2]
        llvm_code(else_statement_sequence)
    goto(label_end)
    llvm.output += ast.label(label_end) + '\n'


def llvm_for(ast):
    # Initialize the for loop
    initialize = ast.children[0]
    llvm_code(initialize)

    # Make for loop label unique
    label_for = "loop" + str(ast.id())
    # This is to avoid a bug in llvm, just dont delete!
    goto(label_for)

    # Make while loop label unique for just after the condition
    label_after_check = "afterCheck" + str(ast.id())
    # Create the label
    llvm.output += ast.label(label_for) + "\n"

    condition = ast.children[1]
    llvm_code(condition)

    # Make a unique label for the end
    label_end = "end" + str(ast.id())
    # Check if we can go further with the loop
    code = "\tbr {type} {var}, label %{label_while}, label %{label_end}\n"
    code = code.format(type="i1",
                       var=variable(condition),
                       label_while=label_after_check,
                       label_end=label_end)
    llvm.output += code
    # Label necessary after the check
    llvm.output += ast.label(label_after_check) + "\n"

    statement_sequence = ast.children[3]
    llvm_code(statement_sequence)

    # Calculate the next step
    iterate = ast.children[2]
    llvm_code(iterate)

    # Loop back to the beginning
    goto(label_for)
    # Make the end of the loop
    llvm.output += ast.label(label_end) + "\n"


def llvm_while(ast):
    # Make while loop label unique
    label_while = "loop" + str(ast.id())
    # This is to avoid a bug in llvm, just dont delete!
    goto(label_while)

    # Make while loop label unique for just after the check condition
    label_after_check = "afterCheck" + str(ast.id())
    # Create the label
    llvm.output += ast.label(label_while) + "\n"

    condition = ast.children[0]
    llvm_code(condition)

    # Make a unique label for the end
    label_end = "end" + str(ast.id())
    # Check if we can go further with the loop
    code = "\tbr {type} {var}, label %{label_while}, label %{label_end}\n"
    code = code.format(type="i1",
                       var=variable(condition),
                       label_while=label_after_check,
                       label_end=label_end)
    llvm.output += code
    # Label necessary after the check
    llvm.output += ast.label(label_after_check) + "\n"

    statement_sequence = ast.children[1]

    llvm_code(statement_sequence)
    # Loop back to the beginning
    goto(label_while)
    # Make the end of the loop
    llvm.output += ast.label(label_end) + "\n"


# Write the llvm version of the ast to the filename
def to_LLVM(ast, filename):
    llvm.output = ""

    # This variable will contain all the variables that are globally defined
    global_declaration_output = ""

    symbol_table = ast.symbol_table.elements
    ptr_types = list()

    # generate variable declarations from the symbol table
    for var in symbol_table:
        element = symbol_table[var]
        element.type.defined = True
        # define all the variables
        LLVM_var_name = "@" + var
        ptr = "*" if symbol_table[var].type.ptr else ""
        LLVM_align = "align"
        if symbol_table[var].type.const:
            LLVM_type = "constant"
        else:
            LLVM_type = "global"
        LLVM_type += " {} undef".format(get_llvm_type(symbol_table[var].type))
        LLVM_align += " {}".format(symbol_table[var].type.get_align())
        global_declaration_output += LLVM_var_name + " = {}, {}\n".format(LLVM_type, LLVM_align)
    if len(symbol_table) > 0:
        global_declaration_output += "\n"
    if not AST.contains_function:
        llvm.output += "define i32 @main() {\n\n"

    llvm_code(ast)

    if not AST.contains_function:
        llvm.output += "\n"
        llvm.output += "ret i32 0\n"
        llvm.output += "}\n\n"

    # If we need to print then create the print function declaration
    if AST.print:
        print_declaration = "declare i32 @printf(i8*, ...)\n"
        llvm.output += print_declaration

    # If we need to scan then create the scan function declaration
    if AST.scan:
        scan_declaration = "declare i32 @__isoc99_scanf(i8*, ...)\n"
        llvm.output += scan_declaration

    # If we have global declarations then prepend them to the code
    if len(global_declaration_output):
        global_declaration_output += llvm.output
        llvm.output = global_declaration_output

    # Write output to the outputfile
    outputFile = open(filename, "w")
    outputFile.write(llvm.output)
    outputFile.close()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Returns the format tags of the ast in a list
def get_format_tags(string):
    _format_tags = list()
    idx = 0
    while idx < len(string):
        # We check for a format tag, because if there is then we need to split the string
        if string[idx] == '%':
            if string[idx - 1] == "\\":  # Huh? I'm confused, why doesn't this crash with the string "%"?
                idx += 1
                continue
            new_idx = idx + 1
            new_string = string[idx]
            while is_number(string[new_idx]):
                new_string += string[new_idx]
                new_idx += 1
                idx += 1
            idx += 2
            _format_tags.append(new_string + string[new_idx])
            continue
        idx += 1

    return _format_tags


def get_tag_type(tag: str):
    if tag == "%d":
        return "int"
    if tag == "%c":
        return "char"
    if tag == "%f":
        return "float"
    if tag == "%s":
        return "string"
    pass


# Returns true when a tag and its argument align
def check_equal_tag_argument(tag: str, argument, function_name):
    # The first and last character of a tag will always form a valid tag from which a type can be deduced
    tag_type = get_tag_type(tag[0] + tag[-1])
    if tag == "%d" and argument.get_type() != 'int':
        raise IncompatibleFunctionType(tag_type, argument.get_type(), function_name)
    elif tag == "%f" and argument.get_type() != 'float':
        raise IncompatibleFunctionType(tag_type, argument.get_type(), function_name)
    elif tag == "%c" and argument.get_type() != 'char':
        raise IncompatibleFunctionType(tag_type, argument.get_type(), function_name)
    elif tag == "%s" and (not isinstance(argument, CString) and not (isinstance(argument, VChar) and argument.array)):
        raise IncompatibleFunctionType(tag_type, argument.get_type(), function_name)
    elif len(tag) <= 2:
        return

    if isinstance(argument, UDeref):
        argument = argument.children[0]
    elif isinstance(argument, Variable) and argument.ptr:
        pass
    # If the argument is not an array then we to raise an error because we cannot scan without an array multiple values
    else:
        raise IncompatibleFunctionType("array[{tag_type}]".format(tag_type=tag_type), argument.get_type(),
                                       function_name)

    number = int(tag[1:-1])
    if number != argument.array_size:
        raise IncompatibleFunctionType("array[{tag_type}]".format(tag_type=tag_type), argument.get_type(),
                                       function_name)


def check_format_tags(format_tags, arguments, function_name):
    for idx in range(len(format_tags)):
        check_equal_tag_argument(format_tags[idx], arguments[idx], function_name)


# This piece of code will create a printf statement if it is necessary
def get_llvm_print(ast):
    # We need to indicate that we are printing so we need to set the ast value of print to true
    AST.print = True
    # In order to get the correct code there are 2 parts in the equation
    # The first one is creating the string to call
    # The second part is making the call to the function with the left over arguments
    # Set up
    # Get the string value
    custom_string = ast[0][0].value

    # Error part
    format_count = ast.get_format_count(custom_string)
    child_count = len(ast[0].children) - 1
    format_tags = get_format_tags(ast[0].children[0].value)
    if format_count != child_count:
        raise CallAmountMismatchError(ast.value, format_count, child_count)
    check_format_tags(format_tags, ast[0].children[1:], "printf")
    # PART 1

    custom_string = ast.to_llvm_string(custom_string)
    string_count = ast.get_real_string_len(custom_string)
    # Create an unique id based on the id of the current function node
    custom_string_id = str(ast.id())
    llvm_string_var = stringVar.format(string_id=custom_string_id, string_len=string_count,
                                       string_val=custom_string)
    # Because this does belong in the global scope we will prepend it to the current
    temp_llvm_output = llvm_string_var
    temp_llvm_output += llvm.output
    llvm.output = temp_llvm_output

    # PART 2
    function_arguments = ""
    for child in ast.children[0]:
        # If we are in the first child it means we are in the string, we do NOT need to pass this as an argument
        # so we use this to set the first argument of the string arguments with the right values in it
        if not len(function_arguments):
            function_arguments = stringArg.format(string_len=string_count, string_id=custom_string_id,
                                                  string_val=child.value)
            continue
        if len(function_arguments):
            # Add a separator to the arguments, because there was a previous argument
            function_arguments += ", "

        # Generate the llvm code of the child
        llvm_code(child)
        # If the type of the child is a string then we need to generate a custom argument
        if child.get_type() == "string":
            function_arguments += llvm_argument(child)
        # If the type of the child is a float then we need to convert it to a bool
        elif get_llvm_type(child) == "float":
            print_type = child.get_llvm_print_type()
            var = str()
            # Because you can't print floats only doubles, we need to first extend it to a double
            if print_type == "double":
                convert_code = VFloat.convert_template("double")
                convert_code = convert_code.format(result=variable(child.parent), value=variable(child))
                var = variable(child.parent)
                llvm.output += convert_code
            else:  # This is the default case
                var = variable(child)

            function_arguments += child.get_llvm_print_type() + " " + var
        # If we find a variable type then we need to check if it is an array
        # because it needs to be another type that needs to be passed through
        elif isinstance(child, Variable):
            # If we have an array we need to store it in a variable and then load this in another variable
            # because it will be a pointer
            if child.array:
                temp = ast.get_temp()
                code = "{result} = getelementptr inbounds {array_type}, {array_type}* {variable}, i64 0, i64 0\n"
                code = code.format(array_type=get_llvm_type(child),
                                   variable=variable(child, store=True),
                                   result=temp)

                llvm.output += code
                function_arguments += get_llvm_type(child, child.array) + "* " + temp
            else:

                # var = variable(child) #, indexed=True, index=child.array_number)
                #
                # function_arguments += get_llvm_type(child, child.array) + " " + var
                # continue
                function_arguments += get_llvm_type(child, child.array) + " " + variable(child)
        else:
            # We know that the llvm code that has been generated has stored the value in the child as a variable
            function_arguments += get_llvm_type(child) + " " + variable(child)

    # We created all the arguments that should go into the function call right now we need to put them in there
    # then we append it to the output of the llvm generation
    insert_string = stringCall.format(string_arg=function_arguments)
    llvm.output += insert_string


# This piece of code will create the scan of the code
def get_llvm_scan(ast):
    # This is mostly the same as print
    # We need to indicate that we are printing so we need to set the ast value of print to true
    AST.scan = True
    # In order to get the correct code there are 2 parts in the equation
    # The first one is creating the string to call
    # The second part is making the call to the function with the left over arguments
    # Set up
    # Get the string value
    custom_string = ast[0][0].value

    # Error part
    format_count = ast.get_format_count(custom_string)
    child_count = len(ast[0].children) - 1
    format_tags = get_format_tags(ast[0].children[0].value)
    if format_count != child_count:
        raise OperatorAmountMismatchError(ast.value, format_count, child_count)
    check_format_tags(format_tags, ast[0].children[1:], "scanf")

    # PART 1
    # Get the string value
    custom_string = ast[0][0].value
    custom_string = ast.to_llvm_string(custom_string)
    string_count = ast.get_real_string_len(custom_string)
    # Create an unique id based on the id of the current function node
    custom_string_id = str(ast.id())
    llvm_string_var = stringVar.format(string_id=custom_string_id, string_len=string_count,
                                       string_val=custom_string)
    # Because this does belong in the global scope we will prepend it to the current
    temp_llvm_output = llvm_string_var
    temp_llvm_output += llvm.output
    llvm.output = temp_llvm_output

    # PART 2
    function_arguments = ""
    for child in ast.children[0]:
        # If we are in the first child it means we are in the string, we do NOT need to pass this as an argument
        # so we use this to set the first argument of the string arguments with the right values in it
        if not len(function_arguments):
            function_arguments = stringArg.format(string_len=string_count, string_id=custom_string_id,
                                                  string_val=child.value)
            continue
        if len(function_arguments):
            # Add a separator to the arguments, because there was a previous argument
            function_arguments += ", "

        # Generate the llvm code of the child
        llvm_code(child)

        # If we find a variable type then we need to check if it is an array
        # because it needs to be another type that needs to be passed through
        if isinstance(child, Variable):
            function_arguments += get_llvm_type(child, child.array) + " " + variable(child)
        else:
            # We know that the llvm code that has been generated has stored the value in the child as a variable
            function_arguments += get_llvm_type(child) + " " + variable(child, store=True)

    # We created all the arguments that should go into the function call right now we need to put them in there
    # then we append it to the output of the llvm generation
    insert_string = scanCall.format(scan_arg=function_arguments)
    llvm.output += insert_string


# Get the variable for the node (and load it from memory if required)
# Store must be true when you want to store into the variable
def variable(ast, store: bool = False, indexed: bool = False, index=0):
    assert isinstance(ast, AST)

    # TODO: move this to their own classes (virtual functions)
    if isinstance(ast, UDeref):
        return variable(ast[0], store=True)
    if isinstance(ast, Variable):
        if store:
            # We need to check if the variable is a global one or a local one
            # If the symbol table is global then we need to return a global variable form
            if ast.get_symbol_table().is_global(ast.value):
                return "@" + ast.value

            # Fetch the symbol table of the ast node
            symbol_table = ast.get_symbol_table()
            # We need to get the position of the variable as a child of
            # the symbol_table node which is somewhere a parent
            var_position = ast.get_position()
            symbol_table_position = symbol_table[ast.value].position
            parent_nr = 1
            # We iterate over all the symbol tables and check if the item is already in the symbol table or not
            # we do this by checking if the position of the variable is before the declaration. If that is the case
            # Then we need to check the parent of the symbol table and so on so forth
            while var_position is None or var_position < symbol_table_position:
                var_position = ast.get_position(parent_nr)
                # Get the previous symbol table and get its parent to seek there
                symbol_table = symbol_table.parent
                symbol_table_position = symbol_table[ast.value].position
                if symbol_table.get_symbol_table(ast.value) != symbol_table:
                    # Ensure we will go 1 ast node higher
                    var_position = -1
                    # Increase the parent_nr so it will seek 1 parent deeper
                    parent_nr += 1
                    continue
                # Increase the parent_nr so it will seek 1 parent deeper
                parent_nr += 1
            # Checks if the symbol table is in the global scope
            # It is the same as checking if the symbol table having parents
            if symbol_table.parent:
                return "%" + ast.value + "." + str(symbol_table.get_symbol_table_id(ast.value))
            return "@" + ast.value
        if indexed:  # Als je aan een bepaalde index een waarde wil assignen
            var = "%.t" + str(ast.get_unique_id())
            index_load(ast, var, index)
            # This loads the pointer type into a normal variable and returns the variable in which is stored
            llvm_load_template = ast.llvm_load_template()
            result = "%.t" + str(ast.get_unique_id())
            llvm_load_template = llvm_load_template.format(result=result,
                                                           type=get_llvm_type(ast, True),
                                                           var=var)
            llvm.output += llvm_load_template
            return result
        else:
            var = "%.t" + str(ast.get_unique_id())
            llvm_load(ast, var)  # Loads the variable in storage into the variable var
            return var
    elif isinstance(ast, UDeref) and store:
        return variable(ast[0], store)

    var = ast.id()

    return "%.v" + str(var)


# Jump to a given label
def goto(label: str):
    llvm.output += "\tbr label %" + label + "\n"


# Variable should be llvm_formated, e.g. %1
def llvm_load(ast, var: str):
    code = ast.get_llvm_template()
    code = code.format(result=var, type=get_llvm_type(ast), var=variable(ast, store=True))
    llvm.output += code


def index_load(ast, result, index):
    code = "\t{result} = getelementptr inbounds {array_type}, {array_type}* {variable}, i64 0, i64 {index}\n"
    code = code.format(result=result, array_type=get_llvm_type(ast),
                       variable=variable(ast.variable, store=True), index=index)
    llvm.output += code


def llvm_argument(ast):
    if isinstance(ast, CString):
        argument = stringArg.format(string_id=variable(ast, True)[2:],
                                    string_len=str(ast.get_real_string_len(ast.value) + 1))
        return argument


from src.Node.AST import AST, StatementSequence, If, For, While, Operator, Function, Arguments, Include, Binary, \
    Assign, VFloat, CString, VInt, VChar, CFloat, CChar, CInt
from src.LLVM.Comments import llvm_comments, Comments
from src.LLVM.Compare import llvm_compare, Compare
from src.LLVM.Constant import llvm_constant, Constant, llvm_type_constant
from src.LLVM.Operate import llvm_operate, Operate, llvm_type_operate, llvm_type_default_operate
from src.LLVM.ReservedType import llvm_reserved_type, ReservedType
from src.LLVM.Unary import llvm_unary, Unary, UReref, UDeref, llvm_type_unary
from src.LLVM.Variable import llvm_variable, Variable, llvm_type_variable
from src.ErrorListener import CallAmountMismatchError, IncompatibleFunctionType
