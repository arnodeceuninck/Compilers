def mips_compare(ast):
    operation = ast.operation
    # TODOs = 'one' | 'olt' | 'ogt' | 'ole' | 'oge' | 'oeq'  # TODO: these are floats

    # All operations supported in the LLVMAst are already in this map
    llvm_mips_map = {"slt": "slt",
                     "sgt": "sgt",
                     "ne": "sne",
                     "sle": "sle",
                     "sge": "sge",
                     "eq": "seq",
                     "one": "sne",  # TODO: check whether floats have the same instructions
                     "olt": "slt",
                     "ogt": "sgt",
                     "ole": "sle",
                     "oge": "sge",
                     "oeq": "seq"}

    # TODO: append u when unsigned, don't know if obligatory
    if operation in llvm_mips_map:
        mips.output += "\t{op} $s0, $t0, $t1\n".format(op=llvm_mips_map[operation])
    else:
        raise Exception("YEEEEEEEEET")


from src.MIPS.MIPS import mips_code, mips, variable, get_mips_type
