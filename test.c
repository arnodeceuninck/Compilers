#include <stdio.h>

int main(){
    int i = 0;
    while(i < 10){
	    printf("%d", i);
	    if (i == 5){
		    break;
	    }
	    i = i + 1;
	    continue;
	    i = 10;
}
}