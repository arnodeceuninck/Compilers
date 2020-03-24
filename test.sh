export PYTHONPATH=$PYTHONPATH:gen
antlr4 -Dlanguage=Python3 -visitor -Xexact-output-dir -o gen input/c.g4
python3 tests/test.py