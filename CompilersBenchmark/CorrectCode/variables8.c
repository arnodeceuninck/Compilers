#include <stdio.h>

// Should print the numbers 10 20 30

int main(){
	int a[3];
	a[0] = 10;
	a[1] = 20;
	a[2] = 30;
	int i = 1;
	while(i < 4){
		printf("%d; ", a[i-1]);
		i = i+1; // TODO: was i++, but not supported by our compiler
	}
	return 1;
}
