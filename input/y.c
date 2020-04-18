#include <stdio.h>

void f(int x) {
    printf("%d", x);
    return;
}

int main(){
    int x =1;
    f(x+1);
    return 0;
}