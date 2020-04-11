from src.Node.AST import AST, For, While


class Break(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: break", fillcolor="{color}"] \n'.format(name=self.id(), color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "; break\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # The loop in which the user situates itself
        loop = self
        # Get the loop in which the break situates itself, it can be situated in an if statement
        while not isinstance(loop, (While, For)):
            loop = loop.parent

        # Handle the break
        end_label = "end" + str(loop.id())
        loop.goto(end_label)


class Continue(AST):
    def __init__(self, value=""):
        AST.__init__(self, value, "#87f5ff")

    def __str__(self):
        return '{name}[label="Reserved Word: Continue", fillcolor="{color}"] \n'.format(name=self.id(),
                                                                                        color=self.color)

    def get_type(self):
        return None  # Has no type

    def comments(self, comment_out: bool = True) -> str:
        return "; continue\n"

    def llvm_code(self):
        AST.llvm_output += self.comments()

        # The loop in which the user situates itself
        loop = self
        # Get the loop in which the break situates itself, it can be situated in an if statement
        while not isinstance(loop, (While, For)):
            loop = loop.parent

        # Handle the continue
        loop_label = "loop" + str(loop.id())
        loop.goto(loop_label)
