#!/bin/bash

# Assumes you're in the folder compilers
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
# Removes the empty input directories
rmdir gen*/input

# make the output folder
if [[ ! -d "output" ]]; then
  mkdir "output"
fi

# y.c is the file we're going to compile, but can be any file
python3 src/main.py input/y.c
