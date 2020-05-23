#export PYTHONPATH=$PYTHONPATH:gen
#antlr4 -Dlanguage=Python3 -visitor -Xexact-output-dir -o gen input/c.g4
#python3 src/main.py input/test.c

# Asumes you're in the folder compilers
#mkdir "tests/output"
wget https://www.antlr.org/download/antlr-4.8-complete.jar
java -jar antlr-4.8-complete.jar -o gen -listener -visitor -Dlanguage=Python3 input/llvm.g4
mv gen/input/* gen
java -jar antlr-4.8-complete.jar -o gen_llvm -listener -visitor -Dlanguage=Python3 input/c.g4
mv gen_llvm/input/* gen_llvm
mkdir "output"
python3 src/main.py input/y.c # y.c is the file we're going to compile