#include <stdio.h>

int main()
{
   int n;
   int i = 3;
   int count;
   int c;

   printf("Enter the number of prime numbers required\n");
   scanf("%d",&n);

   if ( n >= 1 )
   {
      printf("First %d prime numbers are :\n",n);
      printf("2\n");
   }

   count = 2;
   while(count <= n){
      c = 2;
      while(c <= i - 1) {
         if ( i%c == 0 ){
            break;
         }
	c = c + 1;
      }
      if(c == i){
         printf("%d\n",i);
         count = count + 1;
      }
      i = i + 1;
   }

   return 0;
}
