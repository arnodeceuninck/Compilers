
#include <stdio.h>

char f(char c) {
	return c;
}

// Recursive fibonnaci
int main(){
	char f = f('c');
	printf("%c", f);
	return 0;
}