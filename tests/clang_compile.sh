clang -Wall $1 -o $2 > /dev/null 2>&1
chmod +x $2
eval $2 > $3
exit