#include <stdio.h>

int main(){
    int i = 0;
    for(i = 0; i < 10; i++){
	    printf("%d", i);
	    if (i == 5){
	        float y = 0;
		    break;
	    } else {
	        continue;
	    }
	    i = 10;
}
printf("%d", i);
}