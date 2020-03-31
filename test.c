int main(){
    int x = 2;
    int* y = &x;
    if (*y && x) {
        *y = 2;
    }
}