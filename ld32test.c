/*
x86 Length Disassembler test.
Copyright (C) 2013 Byron Platt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <string.h>

#include "ld32.h"

/* how many opcodes should we length disassemble */
#define OPCODES 10

int main(void) {

    int i;
    void *opcode;
    unsigned int length;

    for (i=0, opcode=main; i<OPCODES; i++) {
        length = length_disasm(opcode);
        opcode = (char *)opcode + length;
        printf("%d\n", length);
    }

    return 0;
}
