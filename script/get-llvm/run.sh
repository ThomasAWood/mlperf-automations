#!/bin/bash
clang_bin=${MLC_LLVM_CLANG_BIN_WITH_PATH}
${clang_bin} --version > tmp-ver.out
test $? -eq 0 || exit 1
