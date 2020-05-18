
#include <stdio.h>

int f() {
	return 1;
}

void g() {
    printf("yeet");
}

// Recursive fibonnaci
int main(){
	int n = f();
	g();
	printf("%d", n);
	printf("yeet");
	return 0;
}