
#include <stdio.h>

int f() {
	return 1;
}

// Recursive fibonnaci
int main(){
	int n = f() + f();
	printf("%d", n);
	return 0;
}