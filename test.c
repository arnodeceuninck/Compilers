#include <stdio.h>

void test_func(int y, int x) {
    x = y;
    printf("%d", x);
}

int main() {
    test_func(0, 1);
    return 1+1;
}