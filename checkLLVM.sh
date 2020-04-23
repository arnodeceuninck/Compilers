#!/usr/bin/env bash

clang -S -emit-llvm test.c
lli test.ll
g++ -S -fverbose-asm test.c
