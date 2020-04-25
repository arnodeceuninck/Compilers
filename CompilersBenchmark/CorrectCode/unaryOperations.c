#include <stdio.h>
// TODO: test has been changed because ++ and -- not supported
// This should print the numbers 9 - 14
int main(){
	int x = 9;
    int a[2];
	printf("%d; ", -(-9));
	x = x + 1;
    printf("%d; ", x);
    a[0] = 15;
	a[1] = 12;
	x = 12;
	a[1] = a[1] - 1;
	printf("%d; ", a[1]);
    printf("%d; ", x);
    x = x + 1;
    printf("%d; ", x);
	a[0] = a[0] - 1;
    printf("%d; ", a[0]);
    return 1;
}
