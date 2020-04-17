void f(int* a){
	int b = 43;
}

int main(){
    int x = 0;
	int* xp = &x;
	f(xp);
	printf(x);
}