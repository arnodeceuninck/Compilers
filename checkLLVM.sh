#!/usr/bin/env bash

# This script checks if the output of the llvm code
clang -S -emit-llvm test.c
lli test.ll
g++ -S -fverbose-asm test.c
