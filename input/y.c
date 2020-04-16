int mul(int x, int y){
    int z = x * y;
    return z;
}
/*
* My program
*/
int main(){
int x = 1;
while (x < 10) {
int result = mul(x, 2);
if ( x > 5) {
result = mul(result, x);
}
printf(result); //show the result