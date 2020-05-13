def printa():
    print("a")

def printb():
    print("b")

test = {"a": printa, "b": printb}
test["b"]()