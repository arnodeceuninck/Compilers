#include <stdio.h>

void f(int x) {
    printf("%d %f", x+1, 1.0);
    return;
}

int main(){
    int x =1;
    f(x+1*x);
    return 0;
}