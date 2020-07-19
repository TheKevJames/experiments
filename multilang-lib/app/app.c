#include "lib.h"
#include <stdio.h>

int main(void) {
    NimMain();
    for(int i = 1; i < 40; ++i) {
        printf("fib(%d) = %d\n", i, fib(i));
    }
    return 0;
}
