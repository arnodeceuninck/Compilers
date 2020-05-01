#include <stdio.h>

const int x = 10;
int y = 1 + x;
int f();

// Should print the numbers 10 20 30 40

int main(){
	printf("%d;", x);
	int x = 20;

	printf("%d;", x);
    x = 30;
	if (1){

		printf("%d;", x);
		int x = 40;
		printf("%d;", x);
	}
	f();
	return 1;
}


int f() {
    printf("%d", y);
}