class SymbolTableElement:
    def __init__(self, location=None, type=None, value=None):
        self.location = None


class SymbolTable:
    def __init__(self):
        self.elements = list()

    def insert(self, location, type, value):
        self.elements.append(SymbolTableElement(location, type, value))
