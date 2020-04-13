from src.ErrorListener import VariableRedeclarationError, UndeclaredVariableError


class SymbolTableElement:
    def __init__(self, type=None):
        self.type = type


class SymbolTable:
    dot_output = ""

    def __init__(self, id):
        self.elements = dict()
        self.parent = None  # The next symbol table to use
        self.children = list()  # The children of the symbol table
        self._id = id  # This is the same as the node in the ast

    # Returns the symbol table that contains the specific variable
    def __get_symbol_table(self, location):
        if location not in self.elements:
            # If the variable isnt found in the elements then we need to search in the parents
            cur_parent = self.parent
            # Check while it still has parents and the location is not found
            while cur_parent and location not in cur_parent.elements:
                cur_parent[location]
                cur_parent = cur_parent.parent
            # If the location has been found then we return the element otherwise we return an error
            if location in cur_parent.elements:
                return cur_parent
            raise UndeclaredVariableError(location)
        else:  # These variables are global variables and do not need to be changed in return value
            return self

    # Overloads the [] operator
    def __getitem__(self, location) -> SymbolTableElement:
        return self.__get_symbol_table(location).elements[location]

    # Returns the id of the symbol table where we can find the variable in
    def get_symbol_table_id(self, location) -> int:
        return self.__get_symbol_table(location).id()

    # Check if the variable is global
    def is_global(self, location):
        return self.__get_symbol_table(location).parent is None

    def id(self):
        return self._id

    def insert(self, location, type):
        if location not in self.elements:
            self.elements[location] = SymbolTableElement(type)
        else:
            raise VariableRedeclarationError(location)
            # print("Variable", location, "already in the symbol table.")

    def __str__(self):
        # If there is no symbol table to construct then return the empty string
        if not len(self.elements):
            return ""
        # start the table node
        # A table has a unique id
        table = "\t\ttbl{id} [\n".format(id=self.id())
        table += "\t\t\tshape=plaintext\n" \
                 "\t\t\tlabel=<\n" \
                 "\t\t\t\t<table border='0' cellborder='1' cellspacing='0'>\n"
        # Create the header of the table so it can match the ast node ids based on eyesight of the user
        table += "\t\t\t\t\t<tr><td colspan=\"2\"><b>{tableId}</b></td></tr>\n".format(tableId=self.id())
        table += "\t\t\t\t\t<tr><td>location</td><td>type</td></tr>\n"
        # add all the row elements
        for key in self.elements:
            custom_type = self.elements[key].type
            var_type = "const " if custom_type.const else ""
            var_type += custom_type.get_type()
            var_type += "*" if custom_type.ptr else ""
            table += "\t\t\t\t\t<tr><td>{}</td><td>{}</td></tr>\n".format(key, var_type)
        # finish the table node
        table += "\t\t\t\t</table>\n" \
                 "\t\t\t>];\n"
        return table

    def __dot_node(self):
        # create the symbol table
        SymbolTable.dot_output += str(self)
        # The output needs to be the id + The label itself
        for child in self.children:
            child.__dot_node()

    def __dot_connections(self):
        # Make the connections between the parent and the child(ren)
        for child in self.children:
            SymbolTable.dot_output += "\t\ttbl" + str(self.id()) + " -> " + "tbl" + str(child.id()) + "\n"
            child.__dot_connections()

    def to_dot(self):
        # Being the cluster subgraph
        SymbolTable.dot_output = "\tsubgraph cluster_0 {\n"

        # Make the dot nodes
        self.__dot_node()
        # Make the dot connections between the symbol tables
        self.__dot_connections()

        # Finish the cluster subgraph
        SymbolTable.dot_output += "\t\tlabel = \"Symbol Table\";\n" \
                                  "\t}\n"
