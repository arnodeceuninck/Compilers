#!/usr/bin/env bash
# sudo apt-get install spim
tmpfile=$(mktemp)
# No idea what delayed branches and loads does
spim -file $1 > ${tmpfile}
tail -n +6 ${tmpfile} > $2
exit