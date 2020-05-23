# Asumes you're in the folder compiolers
mkdir "tests/output"
mkdir "output"
antlr4 -o gen -listener -visitor -Dlanguage=Python3 -lib input input/llvm.g4
antlr4 -o gen_llvm -listener -visitor -Dlanguage=Python3 -lib input input/c.g4
python3 src/main.py input/y.c # y.c is the file we're going to compile

#python3 src/main.py input/y.c
#python3 src/test.py output/compiled.ll