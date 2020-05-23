#include <stdio.h>

int main(){
    // Test for printing char*
    char a[5];
    a[0] = 'H';
    a[1] = 'e';
    a[2] = 'l';
    a[3] = 'l';
    a[4] = 'o';
    printf("%s World!\n", a);

    printf("Enter a 5-character string:");
	scanf("%5s", &a);
	printf("%s", a);
	return 1;
}