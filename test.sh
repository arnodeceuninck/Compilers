#!/bin/bash

# Ensures that you can compile the file correctly
export PYTHONPATH=$PYTHONPATH:src

# Downloads the jar if it does not already exist in the folder
if [[ ! -f "antlr-4.8-complete.jar" ]]; then
  wget https://www.antlr.org/download/antlr-4.8-complete.jar
fi
# Remove the generated grammar from the folders
if [[ -d "gen" ]]; then
  rm -rf gen/*
fi
if [[ -d "llvm_gen" ]]; then
  rm -rf llvm_gen/*
fi

# Generate the parser to parse our c and llvm files
java -jar antlr-4.8-complete.jar -o gen_llvm -listener -visitor -Dlanguage=Python3 input/llvm.g4
java -jar antlr-4.8-complete.jar -o gen -listener -visitor -Dlanguage=Python3 input/c.g4
# Move the directories to the gen folders
mv gen_llvm/input/* gen_llvm
mv gen/input/* gen
rmdir gen*/input

# make the output folder for the tests
if [[ ! -d "tests/output" ]]; then
  mkdir "tests/output"
fi

# Runs all the tests aka benchmarks with pythons unittests
python3 -m unittest tests/CorrectCodeTests.py tests/CorrectMipsCodeTests.py tests/SemanticErrorTests.py