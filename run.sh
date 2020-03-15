export PYTHONPATH=$PYTHONPATH:gen
antlr4 -Dlanguage=Python3 -Xexact-output-dir -o gen input/c.g4
python3 src/main.py input/test.c