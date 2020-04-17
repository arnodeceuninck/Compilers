void f(int* a){
	int b = 43;
	*a = b;
	return;
}

int main(){
    int x = 0;
	int* xp = &x;
	f(xp);
	printf(x);
	return 0;
}