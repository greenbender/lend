/*
x86 Length Disassembler.
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


/* implemented tables */
#define PREFIX_T (1 << 0)
#define MODRM2_T (1 << 1)
#define MODRM_T  (1 << 2)
#define DATA1_T  (1 << 3)
#define DATA2_T  (1 << 4)
#define DATA66_T (1 << 5)
#define DATA12_T (1 << 6)


/* configure tables */
#ifndef USE_T
#define USE_T (MODRM2_T|MODRM_T|DATA1_T|DATA66_T|DATA12_T)
#endif


/* table macros */
#ifdef USE_T
#define BITMASK32(                                          \
    b00, b01, b02, b03, b04, b05, b06, b07,                 \
    b08, b09, b0a, b0b, b0c, b0d, b0e, b0f,                 \
    b10, b11, b12, b13, b14, b15, b16, b17,                 \
    b18, b19, b1a, b1b, b1c, b1d, b1e, b1f                  \
) (                                                         \
    (b00 <<  0) | (b01 <<  1) | (b02 <<  2) | (b03 <<  3) | \
    (b04 <<  4) | (b05 <<  5) | (b06 <<  6) | (b07 <<  7) | \
    (b08 <<  8) | (b09 <<  9) | (b0a << 10) | (b0b << 11) | \
    (b0c << 12) | (b0d << 13) | (b0e << 14) | (b0f << 15) | \
    (b10 << 16) | (b11 << 17) | (b12 << 18) | (b13 << 19) | \
    (b14 << 20) | (b15 << 21) | (b16 << 22) | (b17 << 23) | \
    (b18 << 24) | (b19 << 25) | (b1a << 26) | (b1b << 27) | \
    (b1c << 28) | (b1d << 29) | (b1e << 30) | (b1f << 31)   \
)
static int CHECK_TABLE(const unsigned int t[8], unsigned char v) {
    return (t[v >> 5] >> (v & 0x1f)) & 1;
}
#endif


/* CHECK_PREFIX */
#if defined(USE_T) && (USE_T & PREFIX_T)
static const unsigned int prefix_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 0 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 1 */
    BITMASK32(0,0,0,0,0,0,1,0, 0,0,0,0,0,0,1,0,  /* 2 */
              0,0,0,0,0,0,1,0, 0,0,0,0,0,0,1,0), /* 3 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 4 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 5 */
    BITMASK32(0,0,0,0,1,1,1,1, 0,0,0,0,0,0,0,0,  /* 6 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 7 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 8 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 9 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* a */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* b */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* c */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* d */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* e */
              1,0,1,1,0,0,0,0, 0,0,0,0,0,0,0,0)  /* f */
};
#define CHECK_PREFIX(v) CHECK_TABLE(prefix_t, v)
#else
static int CHECK_PREFIX(unsigned char v) {
    return
        (v & 0xe7) == 0x26 ||
        (v & 0xfc) == 0x64 ||
        (v & 0xfe) == 0xf2 ||
        v == 0xf0;
}
#endif


/* CHECK_PREFIX_66 */
static int CHECK_PREFIX_66(unsigned char v) {
    return v == 0x66;
}


/* CHECK_PREFIX_67 */
static int CHECK_PREFIX_67(unsigned char v) {
    return v == 0x67;
}


/* CHECK_0F */
static int CHECK_0F(unsigned char v) {
    return v == 0x0f;
}


/* CHECK_MODRM2 */
#if defined(USE_T) && (USE_T & MODRM2_T)
static const unsigned int modrm2_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(1,1,1,1,0,0,0,0, 0,0,0,0,0,1,0,0,  /* 0 */
              1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1), /* 1 */
    BITMASK32(1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1,  /* 2 */
              0,0,0,0,0,0,0,0, 1,0,1,0,0,0,0,0), /* 3 */
    BITMASK32(1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,  /* 4 */
              1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1), /* 5 */
    BITMASK32(1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,  /* 6 */
              1,1,1,1,1,1,1,0, 1,1,1,1,1,1,1,1), /* 7 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 8 */
              1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1), /* 9 */
    BITMASK32(0,0,0,1,1,1,0,0, 0,0,0,1,1,1,1,1,  /* a */
              1,1,1,1,1,1,1,1, 1,0,1,1,1,1,1,1), /* b */
    BITMASK32(1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,  /* c */
              1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1), /* d */
    BITMASK32(1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,  /* e */
              1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0)  /* f */
};
#define CHECK_MODRM2(v) CHECK_TABLE(modrm2_t, v)
#else
/* TODO: Fix this */
static int CHECK_MODRM2(unsigned char v) {
    unsigned char a = v & 0xfc;
    unsigned char b = v & 0xfe;
    return
        (v & 0xf0) == 0x90 ||
        (v & 0xf8) == 0xb0 ||
        (v & 0xf6) == 0xa4 ||
        a == 0x00 ||
        a == 0xbc ||
        b == 0xba ||
        b == 0xc0 ||
        v == 0xa3 ||
        v == 0xab ||
        v == 0xaf;
}
#endif


/* CHECK_DATA12 */
#if defined(USE_T) && (USE_T & DATA12_T)
static const unsigned int data12_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 0 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 1 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 2 */
              0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0), /* 3 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 4 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 5 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 6 */
              1,1,1,1,0,0,0,0, 0,0,0,0,0,0,0,0), /* 7 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 8 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 9 */
    BITMASK32(0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0,  /* a */
              0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0), /* b */
    BITMASK32(0,0,1,0,1,1,1,0, 0,0,0,0,0,0,0,0,  /* c */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* d */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* e */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0)  /* f */
};
#define CHECK_DATA12(v) CHECK_TABLE(data12_t, v)
#else
static int CHECK_DATA12(unsigned char v) {
    return
        (v & 0xfc) == 0x70 ||
        v == 0x3a ||
        v == 0xa4 ||
        v == 0xac ||
        v == 0xba ||
        v == 0xc2 ||
        v == 0xc4 ||
        v == 0xc5 ||
        v == 0xc6;
}
#endif


/* CHECK_DATA662 */
static int CHECK_DATA662(unsigned char v) {
    return (v & 0xf0) == 0x80;
}


/* CHECK_CRDR2 - For MOV from/to CRx/DRx/TRx mod=3 */
static int CHECK_CRDR2(unsigned char v) {
    return (v & 0xfc) == 0x20;
}


/* CHECK_OP3 - 3 byte opcode */
static int CHECK_OP3(unsigned char v) {
    return v == 0x38 || v == 0x3a;
}


/* CHECK_MODRM */
#if defined(USE_T) && (USE_T & MODRM_T)
static const unsigned int modrm_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(1,1,1,1,0,0,0,0, 1,1,1,1,0,0,0,0,  /* 0 */
              1,1,1,1,0,0,0,0, 1,1,1,1,0,0,0,0), /* 1 */
    BITMASK32(1,1,1,1,0,0,0,0, 1,1,1,1,0,0,0,0,  /* 2 */
              1,1,1,1,0,0,0,0, 1,1,1,1,0,0,0,0), /* 3 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 4 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 5 */
    BITMASK32(0,0,1,1,0,0,0,0, 0,1,0,1,0,0,0,0,  /* 6 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 7 */
    BITMASK32(1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,  /* 8 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 9 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* a */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* b */
    BITMASK32(1,1,0,0,1,1,1,1, 0,0,0,0,0,0,0,0,  /* c */
              1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1), /* d */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* e */
              0,0,0,0,0,0,1,1, 0,0,0,0,0,0,1,1)  /* f */
};
#define CHECK_MODRM(v) CHECK_TABLE(modrm_t, v)
#else
static int CHECK_MODRM(unsigned char v) {
    unsigned char a = v & 0xfc;
    unsigned char b = v & 0xfe;
    return
        (v & 0xc4) == 0x00 ||
        (v & 0xf0) == 0x80 ||
        (v & 0xf8) == 0xd8 ||
        (v & 0xf6) == 0xf6 ||
        a == 0xc4 ||
        a == 0xd0 ||
        b == 0x62 ||
        b == 0xc0 ||
        v == 0x69 ||
        v == 0x6b;
}
#endif


/* CHECK_TEST */
static int CHECK_TEST(unsigned char v) {
    return v == 0xf6 || v == 0xf7;
}


/* CHECK_DATA1 - imm8 */
#if defined(USE_T) && (USE_T & DATA1_T)
static const unsigned int data1_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0,  /* 0 */
              0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0), /* 1 */
    BITMASK32(0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0,  /* 2 */
              0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0), /* 3 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 4 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 5 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,1,1,0,0,0,0,  /* 6 */
              1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1), /* 7 */
    BITMASK32(1,0,1,1,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 8 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 9 */
    BITMASK32(0,0,0,0,0,0,0,0, 1,0,0,0,0,0,0,0,  /* a */
              1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0), /* b */
    BITMASK32(1,1,0,0,0,0,1,0, 1,0,0,0,0,1,0,0,  /* c */
              0,0,0,0,1,1,0,0, 0,0,0,0,0,0,0,0), /* d */
    BITMASK32(1,1,1,1,1,1,1,1, 0,0,0,1,0,0,0,0,  /* e */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0)  /* f */
};
#define CHECK_DATA1(v) CHECK_TABLE(data1_t, v)
#else
static int CHECK_DATA1(unsigned char v) {
    unsigned char a = v & 0xf8;
    unsigned char b = v & 0xfe;
    return
        (v & 0xf0) == 0x70 ||
        (v & 0xc7) == 0x04 ||
        a == 0xb0 ||
        a == 0xe0 ||
        b == 0x6a ||
        b == 0x82 ||
        b == 0xc0 ||
        b == 0xd4 ||
        v == 0x80 ||
        v == 0xa8 ||
        v == 0xc6 ||
        v == 0xc8 ||
        v == 0xcd ||
        v == 0xeb;
}
#endif


/* CHECK_DATA2 - imm16 or ptr16:16/32 (the two additional bytes *must* be added
 * for this to work for both cases, and for ENTER which is imm8 and imm16 */
#if defined(USE_T) && (USE_T & DATA2_T)
static const unsigned int data2_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 0 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 1 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 2 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 3 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 4 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 5 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 6 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 7 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 8 */
              0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0), /* 9 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* a */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* b */
    BITMASK32(0,0,1,0,0,0,0,0, 1,0,1,0,0,0,0,0,  /* c */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* d */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0,  /* e */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0)  /* f */
};
#define CHECK_DATA2(v) CHECK_TABLE(data2_t, v)
#else
static int CHECK_DATA2(unsigned char v) {
    return v == 0x9a || v == 0xc2 || v == 0xc8 || v == 0xca || v == 0xea;
}
#endif


/* CHECK_DATA66 */
#if defined(USE_T) && (USE_T & DATA66_T)
static const unsigned int data66_t[] = {
           /* 0 1 2 3 4 5 6 7  8 9 a b c d e f */
    BITMASK32(0,0,0,0,0,1,0,0, 0,0,0,0,0,1,0,0,  /* 0 */
              0,0,0,0,0,1,0,0, 0,0,0,0,0,1,0,0), /* 1 */
    BITMASK32(0,0,0,0,0,1,0,0, 0,0,0,0,0,1,0,0,  /* 2 */
              0,0,0,0,0,1,0,0, 0,0,0,0,0,1,0,0), /* 3 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 4 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 5 */
    BITMASK32(0,0,0,0,0,0,0,0, 1,1,0,0,0,0,0,0,  /* 6 */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* 7 */
    BITMASK32(0,1,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  /* 8 */
              0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0), /* 9 */
    BITMASK32(0,0,0,0,0,0,0,0, 0,1,0,0,0,0,0,0,  /* a */
              0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1), /* b */
    BITMASK32(0,0,0,0,0,0,0,1, 0,0,0,0,0,0,0,0,  /* c */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0), /* d */
    BITMASK32(0,0,0,0,0,0,0,0, 1,1,1,0,0,0,0,0,  /* e */
              0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0)  /* f */
};
#define CHECK_DATA66(v) CHECK_TABLE(data66_t, v)
#else
static int CHECK_DATA66(unsigned char v) {
    return
        (v & 0xc7) == 0x05 ||
        (v & 0xf8) == 0xb8 ||
        (v & 0x7e) == 0x68 ||
        v == 0x81 ||
        v == 0x9a ||
        v == 0xa9 ||
        v == 0xc7 ||
        v == 0xea;
}
#endif


/* CHECK_MEM67 */
static int CHECK_MEM67(unsigned char v) {
    return (v & 0xfc) == 0xa0;
}


/* length_disasm */
unsigned int length_disasm(const void *opcode0) {
    const unsigned char *opcode = opcode0;
    unsigned int flag = 0, crdr = 0;
    unsigned int msize = 0, dsize = 0;
    unsigned int ddef = 4, mdef = 4;
    unsigned char op;

    /* prefix */
    do {
        op = *opcode++;
        if (CHECK_PREFIX_66(op)) ddef = 2;
        if (CHECK_PREFIX_67(op)) mdef = 2;
    } while (CHECK_PREFIX(op));

    /* two byte opcode */
    if (CHECK_0F(op)) {
        op = *opcode++;
        if (CHECK_MODRM2(op)) flag = 1;
        if (CHECK_DATA12(op)) dsize = 1;
        else if (CHECK_DATA662(op)) dsize = ddef;
        if (CHECK_CRDR2(op)) crdr = 1;
        if (CHECK_OP3(op)) opcode++;
    }

    /* one byte opcode */
    else {
        if (CHECK_MODRM(op)) flag = 1;
        if (CHECK_DATA1(op)) dsize = 1;
        else if (CHECK_DATA66(op)) dsize = ddef;
        if (CHECK_DATA2(op)) dsize += 2;
        if (CHECK_TEST(op) && !(*opcode & 0x30)) dsize += (op & 1) ? ddef : 1;
        if (CHECK_MEM67(op)) msize = mdef;
    }

    /* modrm */
    if (flag) {
        unsigned char modrm = *opcode++;
        unsigned char mod = crdr ? 0x03 : modrm >> 6;
        if (mod != 0x03) {
            unsigned char rm  = modrm & 0x07;
            if (mod == 0x01) msize++;
            if (mod == 0x02) msize += mdef;
            if (mdef == 2) {
                if ((mod == 0x00) && (rm == 0x06)) msize += 2;
            } else {
                if (rm == 0x04) rm = *opcode++ & 0x07;
                if (rm == 0x05 && mod == 0x00) msize += 4;
            }
        }
    }

    opcode += msize + dsize;

    return opcode - (const unsigned char *)opcode0;
}
