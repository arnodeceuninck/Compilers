mkdir "tests/output"
#mkdir "output"
antlr4 -o gen -listener -visitor -Dlanguage=Python3 input/llvm.g4
antlr4 -o gen_llvm -listener -visitor -Dlanguage=Python3 input/c.g4
python3 -m unittest tests/CorrectCodeTests.py tests/CorrectMipsCodeTests.py tests/SemanticErrorTests.py