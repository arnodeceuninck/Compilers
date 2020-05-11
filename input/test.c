#include <stdio.h>

int main(){
    float x = 1.0;
    x = x / x;
    x = x + x;
    x = x - x;
    x = x * x;
    x = x > x;
    x = x < x;
    x = x <= x;
    x = x >= x;
    x = x == x;
    x = x != x;
    x = x % x;
    x = x && x;
    x = x || x;
    printf("test %d", 2);
   	return 1;
}