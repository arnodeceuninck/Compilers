
#include <stdio.h>

float f() {
	return 1.0;
}

// Recursive fibonnaci
int main(){
	float n = f() + f();
	printf("%f", n);
	return 0;
}