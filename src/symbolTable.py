from src.ErrorListener import VariableRedeclarationError, UndeclaredVariableError

class SymbolTableElement:
    def __init__(self, type=None):
        self.type = type


class SymbolTable:
    def __init__(self):
        self.elements = dict()

    # Overloads the [] operator
    def __getitem__(self, location) -> SymbolTableElement:
        if location not in self.elements:
            raise UndeclaredVariableError(location)
        else:
            return self.elements[location]

    def insert(self, location, type):
        if location not in self.elements:
            self.elements[location] = SymbolTableElement(type)
        else:
            raise VariableRedeclarationError(location)
            # print("Variable", location, "already in the symbol table.")

    def update(self, location, value):
        self.elements[location].value = value

    def __str__(self):
        # If there is no symbol table to construct then return the empty string
        if not len(self.elements):
            return ""
        # start the table node
        table = "\tsubgraph cluster_0 {\n" \
                "\t\ttbl [\n" \
                "\t\t\tshape=plaintext\n" \
                "\t\t\tlabel=<\n" \
                "\t\t\t\t<table border='0' cellborder='1' cellspacing='0'>\n" \
                "\t\t\t\t\t<tr><td>location</td><td>type</td></tr>\n"
        # add all the row elements
        for key in self.elements:
            custom_type = self.elements[key].type
            var_type = "const " if custom_type.const else ""
            var_type += custom_type.type
            var_type += "*" if custom_type.ptr else ""
            table += "\t\t\t\t\t\t<tr><td>{}</td><td>{}</td></tr>\n".format(key, var_type)
        # finish the table node
        table += "\t\t\t\t</table>\n" \
                 "\t\t\t>];\n" \
                 "\t\tlabel = \"Symbol Table\";\n" \
                 "\t}\n"
        return table
