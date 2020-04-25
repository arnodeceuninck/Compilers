#include <stdio.h>

int main(){
    int x[3];
    x[2] = 3;
    int z = 2;
    int y = x[z];
    printf("%d", y);
//    int y = x[2];
}
