clang -Wall $1 -o $2
chmod +x $2
eval $2 > $3
exit