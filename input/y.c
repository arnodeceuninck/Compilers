#include <stdio.h>

int f(int x) {
    printf("%d %f\n", x+1, 1.0);
    return 8;
}

int main(){
    int x =1;
    x = f(x+1*x);
    printf("%d", x);
    return x+1;
}