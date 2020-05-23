wget https://www.antlr.org/download/antlr-4.8-complete.jar
java -jar antlr-4.8-complete.jar -fo gen -listener -visitor -Dlanguage=Python3 input/llvm.g4
java -jar antlr-4.8-complete.jar -fo gen_llvm -listener -visitor -Dlanguage=Python3 input/c.g4
mkdir "tests/output"
python3 src/main.py input/y.c # y.c is the file we're going to compile
python3 -m unittest tests/CorrectCodeTests.py tests/CorrectMipsCodeTests.py tests/SemanticErrorTests.py