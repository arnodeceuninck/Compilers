from gen.cVisitor import cVisitor


class KeyPrinter(cVisitor):
    def visitStart_rule(self, ctx: cVisitor.visitStart_rule):
        print("Oh, a key!")
