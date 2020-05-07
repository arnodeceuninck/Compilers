#include <stdio.h>

int a[2];

// Should print the numbers 1 2 3

int main(){
	int x = 3.0;
	a[1] = 2;
	printf("%d; %d; %d;", x, a[1], x);
	return 1;
}