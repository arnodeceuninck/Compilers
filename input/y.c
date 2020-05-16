#include <stdio.h>

int main() {
  int x = 1;
  x = x + 1;
  x = 1;
  printf("%s %d", "test", x + 1);
  return 1;
}