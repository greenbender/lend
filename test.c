#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/mman.h>
#include "ld32.h"


int main(int argc, char **argv) {
    void *addr, *op;
    struct stat buf;
    int fd;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s filename\n", argv[0]);
        return -1;
    }

    fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        perror("open");
        return -2;
    }

    if (fstat(fd, &buf) < 0) {
        perror("fstat");
        return -3;
    }

    op = addr = mmap(NULL, buf.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (addr == MAP_FAILED) {
        perror("mmap");
        return -4;
    }

    while (op < addr + buf.st_size) {
        unsigned int len = length_disasm(op);
        printf("%d\n", len);
        op += len;
    }

    return 0;
}
