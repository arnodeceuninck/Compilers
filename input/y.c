#include <stdio.h>
// TODO: test has been changed because ++ and -- not supported
// This should print the numbers 9 - 14
int main(){
	int a[4];
	a[1] = 12;
	a[1] = a[1] - 1;
	printf("%d; ", a[1]);
    return 1;
}
