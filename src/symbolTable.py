class SymbolTableElement:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value


class SymbolTable:
    def __init__(self):
        self.elements = dict()

    def insert(self, location, type, value):
        self.elements[location] = SymbolTableElement(type, value)

    def update(self, location, value):
        self.elements[location].value = value
