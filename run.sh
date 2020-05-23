#export PYTHONPATH=$PYTHONPATH:gen
#antlr4 -Dlanguage=Python3 -visitor -Xexact-output-dir -o gen input/c.g4
#python3 src/main.py input/test.c

# Asumes you're in the folder compilers
#mkdir "tests/output"
mkdir "output"
antlr4 -o gen -listener -visitor -Dlanguage=Python3 -lib input input/llvm.g4
antlr4 -o gen_llvm -listener -visitor -Dlanguage=Python3 -lib input input/c.g4
python3 src/main.py input/y.c # y.c is the file we're going to compile