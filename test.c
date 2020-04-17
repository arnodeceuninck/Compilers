#include <stdio.h>

void f(int* a){
	int b = 43;
	*a = b;
	return;
}

int main(){
    int x = 0;
	int* xp = &x;
	f(xp);
	printf("%d", x);
	return 0;
}