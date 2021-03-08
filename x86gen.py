#!/usr/bin/python3
'''Generate *all* possible x86 instructions.

Useful for testing disassemblers and other x86 instruction parsing code. At the
moment only instructions that are able to be disassembled by Capstone are
emitted. I hope to make this behaviour optional at some point.

Where adding a prefix doesn't have any effect on an instruction, a best effort
attempt has been made to not emit the extra instruction, however, removing all
instances of useless instruction repetition will be an ongoing task.'''


import sys


def O(*parts):
    b = []
    for p in parts:
        if isinstance(p, list):
            b.extend(p)
        else:
            b.append(p)
    sys.stdout.buffer.write(bytes(b))
    sys.stdout.flush()


# byte values for operands
_rel = 0x00
_disp = 0x11
_imm = 0x22
_moffs = 0x33
_sel = 0x44
_off = 0x55


# common operand values
disp8 = [_disp]
disp16 = [_disp, _disp]
disp32 = [_disp, _disp, _disp, _disp]
imm8 = [_imm]
imm16 = [_imm, _imm]
imm32 = [_imm, _imm, _imm, _imm]
rel8 = [_rel]
rel16 = [_rel, _rel]
rel32 = [_rel, _rel, _rel, _rel]
moffs8 = [_moffs, _moffs, _moffs, _moffs]
moffs16 = [_moffs, _moffs, _moffs, _moffs]
moffs32 = [_moffs, _moffs, _moffs, _moffs]
ptr16_16 = [_off, _off, _sel, _sel]
ptr16_32 = [_off, _off, _off, _off, _sel, _sel]
m16_16 = [_off, _off, _sel, _sel]
m16_32 = [_off, _off, _off, _off, _sel, _sel]


# prefixes
pos = 0x66 # Operand size override
pps = 0x66 # Precision size override
pas = 0x67 # Address size override
p2b = 0x0f # Two byte opcode
pdp = 0xf2 # Scalar double precision
psp = 0xf3 # Scalar single precision


def modrm16(modonly=None, regonly=None):
    for modrm in range(0xff + 1):
        mod, reg, rm = modrm >> 6, (modrm >> 3) & 7, modrm & 7
        if modonly is not None and mod not in modonly:
            continue
        if regonly is not None and reg not in regonly:
            continue
        disp = []
        if mod == 0 and rm == 6:
            disp = disp16
        elif mod == 1:
            disp = disp8
        elif mod == 2:
            disp = disp16
        yield [modrm] + disp


def modrm32(modonly=None, regonly=None):
    for modrm in range(0xff + 1):
        mod, reg, rm = modrm >> 6, (modrm >> 3) & 7, modrm & 7
        if modonly is not None and mod not in modonly:
            continue
        if regonly is not None and reg not in regonly:
            continue
        if mod == 0 and rm == 5:
            disp = disp32
        elif mod == 1:
            disp = disp8
        elif mod == 2:
            disp = disp32
        else:
            disp = []
        if mod < 3 and rm == 4:
            for sib in range(0xff + 1):
                if sib & 7 == 5 and mod == 0:
                    yield [modrm, sib] + disp32
                else:
                    yield [modrm, sib] + disp
        else:
            yield [modrm] + disp


# ADD r/m8, r8
for b in modrm32():
    O(0x00, b)
for b in modrm16():
    O(pas, 0x00, b)


# ADD r/m16/32, r16/32
for b in modrm32():
    O(0x01, b)
for b in modrm32():
    O(pos, 0x01, b)
for b in modrm16():
    O(pas, 0x01, b)
for b in modrm16():
    O(pas, pos, 0x01, b)


# ADD r8, r/m8
for b in modrm32():
    O(0x02, b)
for b in modrm16():
    O(pas, 0x02, b)


# ADD r16/32, r/m16/32
for b in modrm32():
    O(0x03, b)
for b in modrm32():
    O(pos, 0x03, b)
for b in modrm16():
    O(pas, 0x03, b)
for b in modrm16():
    O(pas, pos, 0x03, b)


# ADD AL, imm8
O(0x04, imm8)


# ADD E?AX, imm16/32
O(0x05, imm32)
O(pos, 0x05, imm16)


# PUSH ES
O(0x06)


# POP ES
O(0x07)


# OR r/m8, r8
for b in modrm32():
    O(0x08, b)
for b in modrm16():
    O(pas, 0x08, b)


# OR r/m16/32, r16/32
for b in modrm32():
    O(0x09, b)
for b in modrm32():
    O(pos, 0x09, b)
for b in modrm16():
    O(pas, 0x09, b)
for b in modrm16():
    O(pas, pos, 0x09, b)


# OR r8, r/m8
for b in modrm32():
    O(0x0a, b)
for b in modrm16():
    O(pas, 0x0a, b)


# OR r16/32, r/m16/32
for b in modrm32():
    O(0x0b, b)
for b in modrm32():
    O(pos, 0x0b, b)
for b in modrm16():
    O(pas, 0x0b, b)
for b in modrm16():
    O(pas, pos, 0x0b, b)


# OR AL, imm8
O(0x0c, imm8)


# OR E?AX, imm16/32
O(0x0d, imm32)
O(pos, 0x0d, imm16)


# PUSH CS
O(0x0e)


# 0x0f (2 byte instructions)


# ADC r/m8, r8
for b in modrm32():
    O(0x10, b)
for b in modrm16():
    O(pas, 0x10, b)


# ADC r/m16/32, r16/32
for b in modrm32():
    O(0x11, b)
for b in modrm32():
    O(pos, 0x11, b)
for b in modrm16():
    O(pas, 0x11, b)
for b in modrm16():
    O(pas, pos, 0x11, b)


# ADC r8, r/m8
for b in modrm32():
    O(0x12, b)
for b in modrm16():
    O(pas, 0x12, b)


# ADC r16/32, r/m16/32
for b in modrm32():
    O(0x13, b)
for b in modrm32():
    O(pos, 0x13, b)
for b in modrm16():
    O(pas, 0x13, b)
for b in modrm16():
    O(pas, pos, 0x13, b)


# ADC AL, imm8
O(0x14, imm8)


# ADC E?AX, imm16/32
O(0x15, imm32)
O(pos, 0x15, imm16)


# PUSH SS
O(0x16)


# POP SS
O(0x17)


# SBB r/m8, r8
for b in modrm32():
    O(0x18, b)
for b in modrm16():
    O(pas, 0x18, b)


# SBB r/m16/32, r16/32
for b in modrm32():
    O(0x19, b)
for b in modrm32():
    O(pos, 0x19, b)
for b in modrm16():
    O(pas, 0x19, b)
for b in modrm16():
    O(pas, pos, 0x19, b)


# SBB r8, r/m8
for b in modrm32():
    O(0x1a, b)
for b in modrm16():
    O(pas, 0x1a, b)


# SBB r16/32, r/m16/32
for b in modrm32():
    O(0x1b, b)
for b in modrm32():
    O(pos, 0x1b, b)
for b in modrm16():
    O(pas, 0x1b, b)
for b in modrm16():
    O(pas, pos, 0x1b, b)


# SBB AL, imm8
O(0x1c, imm8)


# SBB E?AX, imm16/32
O(0x1d, imm32)
O(pos, 0x1d, imm16)


# POP DS
O(0x1e)


# POP DS
O(0x1f)


# AND r/m8, r8
for b in modrm32():
    O(0x20, b)
for b in modrm16():
    O(pas, 0x20, b)


# AND r/m16/32, r16/32
for b in modrm32():
    O(0x21, b)
for b in modrm32():
    O(pos, 0x21, b)
for b in modrm16():
    O(pas, 0x21, b)
for b in modrm16():
    O(pas, pos, 0x21, b)


# AND r8, r/m8
for b in modrm32():
    O(0x22, b)
for b in modrm16():
    O(pas, 0x22, b)


# AND r16/32, r/m16/32
for b in modrm32():
    O(0x23, b)
for b in modrm32():
    O(pos, 0x23, b)
for b in modrm16():
    O(pas, 0x23, b)
for b in modrm16():
    O(pas, pos, 0x23, b)


# AND AL, imm8
O(0x24, imm8)


# AND E?AX, imm16/32
O(0x25, imm32)
O(pos, 0x25, imm16)


# 0x26 ES segment prefix


# DAA
O(0x27)


# SUB r/m8, r8
for b in modrm32():
    O(0x28, b)
for b in modrm16():
    O(pas, 0x28, b)


# SUB r/m16/32, r16/32
for b in modrm32():
    O(0x29, b)
for b in modrm32():
    O(pos, 0x29, b)
for b in modrm16():
    O(pas, 0x29, b)
for b in modrm16():
    O(pas, pos, 0x29, b)


# SUB r8, r/m8
for b in modrm32():
    O(0x2a, b)
for b in modrm16():
    O(pas, 0x2a, b)


# SUB r16/32, r/m16/32
for b in modrm32():
    O(0x2b, b)
for b in modrm32():
    O(pos, 0x2b, b)
for b in modrm16():
    O(pas, 0x2b, b)
for b in modrm16():
    O(pas, pos, 0x2b, b)


# SUB AL, imm8
O(0x2c, imm8)


# SUB E?AX, imm16/32
O(0x2d, imm32)
O(pos, 0x2d, imm16)


# 0x2e CS segment prefix


# DAS
O(0x2f)


# XOR r/m8, r8
for b in modrm32():
    O(0x30, b)
for b in modrm16():
    O(pas, 0x30, b)


# XOR r/m16/32, r16/32
for b in modrm32():
    O(0x31, b)
for b in modrm32():
    O(pos, 0x31, b)
for b in modrm16():
    O(pas, 0x31, b)
for b in modrm16():
    O(pas, pos, 0x31, b)


# XOR r8, r/m8
for b in modrm32():
    O(0x32, b)
for b in modrm16():
    O(pas, 0x32, b)


# XOR r16/32 r/m16/32
for b in modrm32():
    O(0x33, b)
for b in modrm32():
    O(pos, 0x33, b)
for b in modrm16():
    O(pas, 0x33, b)
for b in modrm16():
    O(pas, pos, 0x33, b)


# XOR AL, imm8
O(0x34, imm8)


# XOR E?AX, imm16/32
O(0x35, imm32)
O(pos, 0x35, imm16)


# 0x36 SS segment prefix


# AAA
O(0x37)


# CMP r/m8, r8
for b in modrm32():
    O(0x38, b)
for b in modrm16():
    O(pas, 0x38, b)


# CMP r/m16/32, r16/32
for b in modrm32():
    O(0x39, b)
for b in modrm32():
    O(pos, 0x39, b)
for b in modrm16():
    O(pas, 0x39, b)
for b in modrm16():
    O(pas, pos, 0x39, b)


# CMP r8, r/m8
for b in modrm32():
    O(0x3a, b)
for b in modrm16():
    O(pas, 0x3a, b)


# CMP r16/32, r/m16/32
for b in modrm32():
    O(0x3b, b)
for b in modrm32():
    O(pos, 0x3b, b)
for b in modrm16():
    O(pas, 0x3b, b)
for b in modrm16():
    O(pas, pos, 0x3b, b)


# CMP AL, imm8
O(0x3c, imm8)


# CMP E?AX, imm16/32
O(0x3d, imm32)
O(pos, 0x3d, imm16)


# 0x3e DS segment prefix


# AAS
O(0x3f)


# INC E?(AX|CX|DX|BX|SP|BP|SI|DI)
for op in range(0x40, 0x48):
    O(op)
for op in range(0x40, 0x48):
    O(pos, op)


# DEC E?(AX|CX|DX|BX|SP|BP|SI|DI)
for op in range(0x48, 0x50):
    O(op)
for op in range(0x48, 0x50):
    O(pos, op)


# PUSH E?(AX|CX|DX|BX|SP|BP|SI|DI)
for op in range(0x50, 0x58):
    O(op)
for op in range(0x50, 0x58):
    O(pos, op)


# POP E?(AX|CX|DX|BX|SP|BP|SI|DI)
for op in range(0x58, 0x60):
    O(op)
for op in range(0x58, 0x60):
    O(pos, op)


# PUSHAD?
O(0x60)
O(pos, 0x60)


# POPAD?
O(0x61)
O(pos, 0x61)


# BOUND r16/32, m16/32&16/32
for b in modrm32(modonly=[0, 1, 2]):
    O(0x62, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, 0x62, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0x62, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, 0x62, b)


# ARPL r/m16, r16
for b in modrm32():
    O(0x63, b)
for b in modrm16():
    O(pas, 0x63, b)


# 0x64 FS segment prefix


# 0x65 GS segment prefix


# 0x66 Operand/Precision size override


# 0x67 Address size override


# PUSH imm16/32
O(0x68, imm32)
O(pos, 0x68, imm16)


# IMUL r16/32, r/m16/32, imm16/32
for b in modrm32():
    O(0x69, b, imm32)
for b in modrm32():
    O(pos, 0x69, b, imm16)
for b in modrm16():
    O(pas, 0x69, b, imm32)
for b in modrm16():
    O(pas, pos, 0x69, b, imm16)


# PUSH imm8
O(0x6a, imm8)


# IMUL r16/32, r/m16/32, imm8
for b in modrm32():
    O(0x6b, b, imm8)
for b in modrm32():
    O(pos, 0x6b, b, imm8)
for b in modrm16():
    O(pas, 0x6b, b, imm8)
for b in modrm16():
    O(pas, pos, 0x6b, b, imm8)


# INS m8
O(0x6c)


# INS m16/32
O(0x6d)
O(pos, 0x6d)


# OUTS m8
O(0x6e)


# OUTS m16/32
O(0x6f)
O(pos, 0x6f)


# J(O|NO|C|NC|Z|NZ|NA|A|S|NS|PE|PO|L|NL|NG|G) rel8
for op in range(0x70, 0x80):
    O(op, rel8)


# (ADD|OR|ADC|SBB|AND|SUB|XOR|CMP) r/m8, imm8
for b in modrm32():
    O(0x80, b, imm8)
for b in modrm16():
    O(pas, 0x80, b, imm8)


# (ADD|OR|ADC|SBB|AND|SUB|XOR|CMP) r/m16/32, imm16/32
for b in modrm32():
    O(0x81, b, imm32)
for b in modrm32():
    O(pos, 0x81, b, imm16)
for b in modrm16():
    O(pas, 0x81, b, imm32)
for b in modrm16():
    O(pas, pos, 0x81, b, imm16)


# (ADD|OR|ADC|SBB|AND|SUB|XOR|CMP) r/m8, imm8
for b in modrm32():
    O(0x82, b, imm8)
for b in modrm16():
    O(pas, 0x82, b, imm8)


# (ADD|OR|ADC|SBB|AND|SUB|XOR|CMP) r/m16/32, imm8
for b in modrm32():
    O(0x83, b, imm8)
for b in modrm32():
    O(pos, 0x83, b, imm8)
for b in modrm16():
    O(pas, 0x83, b, imm8)
for b in modrm16():
    O(pas, pos, 0x83, b, imm8)


# TEST r/m8, r8
for b in modrm32():
    O(0x84, b)
for b in modrm16():
    O(pas, 0x84, b)


## TEST r/m16/32, r16/32
for b in modrm32():
    O(0x85, b)
for b in modrm32():
    O(pos, 0x85, b)
for b in modrm16():
    O(pas, 0x85, b)
for b in modrm16():
    O(pas, pos, 0x85, b)


# XCHG r/m8, r8
for b in modrm32():
    O(0x86, b)
for b in modrm16():
    O(pas, 0x86, b)


## XCHG r/m16/32, r16/32
for b in modrm32():
    O(0x87, b)
for b in modrm32():
    O(pos, 0x87, b)
for b in modrm16():
    O(pas, 0x87, b)
for b in modrm16():
    O(pas, pos, 0x87, b)


# MOV r/m8, r8
for b in modrm32():
    O(0x88, b)
for b in modrm16():
    O(pas, 0x88, b)


## MOV r/m16/32, r16/32
for b in modrm32():
    O(0x89, b)
for b in modrm32():
    O(pos, 0x89, b)
for b in modrm16():
    O(pas, 0x89, b)
for b in modrm16():
    O(pas, pos, 0x89, b)


# MOV r8, r/m8
for b in modrm32():
    O(0x8a, b)
for b in modrm16():
    O(pas, 0x8a, b)


## MOV r16/32, r/m16/32
for b in modrm32():
    O(0x8b, b)
for b in modrm32():
    O(pos, 0x8b, b)
for b in modrm16():
    O(pas, 0x8b, b)
for b in modrm16():
    O(pas, pos, 0x8b, b)


# MOV r/m16/32, Sreg
for b in modrm32(regonly=[0, 1, 2, 3, 4, 5]):
    O(0x8c, b)
for b in modrm16(regonly=[0, 1, 2, 3, 4, 5]):
    O(pas, 0x8c, b)


# LEA r16/32, m
for b in modrm32(modonly=[0, 1, 2]):
    O(0x8d, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, 0x8d, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0x8d, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, 0x8d, b)


# MOV Sreg, r/m16
for b in modrm32(regonly=[0, 1, 2, 3, 4, 5]):
    O(0x8e, b)
for b in modrm16(regonly=[0, 1, 2, 3, 4, 5]):
    O(pas, 0x8e, b)


# POP r/m16/32
for b in modrm32(regonly=[0]):
    O(0x8f, b)
for b in modrm32(regonly=[0]):
    O(pos, 0x8f, b)
for b in modrm16(regonly=[0]):
    O(pas, 0x8f, b)
for b in modrm16(regonly=[0]):
    O(pas, pos, 0x8f, b)


# XCHG E?AX, E?(AX|CX|DX|BX|SP|BP|SI|DI)
for op in range(0x90, 0x98):
    O(op)
for op in range(0x90, 0x98):
    O(pos, op)


# C(BW|WDE)
O(0x98)
O(pos, 0x98)


# C(WD|DQ)
O(0x99)
O(pos, 0x99)


# CALLF ptr16:16/32
O(0x9a, ptr16_32)
O(pos, 0x9a, ptr16_16)


# WAIT
O(0x9b)


# PUSHFD?
O(0x9c)
O(pos, 0x9c)


# POPFD?
O(0x9d)
O(pos, 0x9d)


# SAHF
O(0x9e)


# LAHF
O(0x9f)


# MOV AL, moffs8
O(0xa0, moffs8)


# MOV E?AX, moffs16/32
O(0xa1, moffs32)
O(pos, 0xa1, moffs16)


# MOV moffs8, AL
O(0xa2, moffs8)


# MOV moffs16/32, E?AX
O(0xa3, moffs32)
O(pos, 0xa3, moffs16)


# MOVSB
O(0xa4)


# MOVS(W|D)
O(0xa5)
O(pos, 0xa5)


# CMPSB
O(0xa6)


# CMPS(W|D)
O(0xa7)
O(pos, 0xa7)


# TEST AL, imm8
O(0xa8, imm8)


# TEST E?AX, imm16/32
O(0xa9, imm32)
O(pos, 0xa9, imm16)


# STOSB
O(0xaa)


# STOS(W|D)
O(0xab)
O(pos, 0xab)


# LODSB
O(0xac)


# LODS(W|D)
O(0xad)
O(pos, 0xad)


# SCASB
O(0xae)


# SCAS(W|D)
O(0xaf)
O(pos, 0xaf)


# MOV (AL|CL|DL|BL|AH|CH|DH|BH), imm8
for op in range(0xb0, 0xb8):
    O(op, imm8)


# MOV E?(AX|CX|DX|BX|SP|BP|SI|DI), imm16/32
for op in range(0xb8, 0xc0):
    O(op, imm32)
for op in range(0xb8, 0xc0):
    O(pos, op, imm16)



# (ROL|ROR|RCL|RCR|SHL|SHR|SAL|SAR) r/m8, imm8
for b in modrm32():
    O(0xc0, b, imm8)
for b in modrm16():
    O(pas, 0xc0, b, imm8)


# (ROL|ROR|RCL|RCR|SHL|SHR|SAL|SAR) r/m16/32, imm8
for b in modrm32():
    O(0xc1, b, imm8)
for b in modrm32():
    O(pos, 0xc1, b, imm8)
for b in modrm16():
    O(pas, 0xc1, b, imm8)
for b in modrm16():
    O(pas, pos, 0xc1, b, imm8)


# RETN imm16
O(0xc2, imm16)


# RETN
O(0xc3)


# LES ES, r16/32, m16:16/32
for b in modrm32(modonly=[0, 1, 2]):
    O(0xc4, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, 0xc4, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0xc4, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, 0xc4, b)


# LDS DS, r16/32, m16:16/32
for b in modrm32(modonly=[0, 1, 2]):
    O(0xc5, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, 0xc5, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0xc5, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, 0xc5, b)


# MOV r/m8, imm8
for b in modrm32(regonly=[0]):
    O(0xc6, b, imm8)
for b in modrm16(regonly=[0]):
    O(pas, 0xc6, b, imm8)


# MOV r/m16/32, imm16/32
for b in modrm32(regonly=[0]):
    O(0xc7, b, imm32)
for b in modrm32(regonly=[0]):
    O(pos, 0xc7, b, imm16)
for b in modrm16(regonly=[0]):
    O(pas, 0xc7, b, imm32)
for b in modrm16(regonly=[0]):
    O(pas, pos, 0xc7, b, imm16)


# ENTER
O(0xc8, imm16, imm8)


# LEAVE
O(0xc9)


# RETF imm16
O(0xca, imm16)


# RETF
O(0xcb)


# INT3
O(0xcc)


# INT imm8
O(0xcd, imm8)


# INTO
O(0xce)


# IRETD?
O(0xcf)
O(0x66, 0xcf)


# (ROL|ROR|RCL|RCR|SHL|SHR|SAL|SAR) r/m8, 1
for b in modrm32():
    O(0xd0, b)
for b in modrm16():
    O(pas, 0xd0, b)


# (ROL|ROR|RCL|RCR|SHL|SHR|SAL|SAR) r/m16/32, 1
for b in modrm32():
    O(0xd1, b)
for b in modrm32():
    O(pos, 0xd1, b)
for b in modrm16():
    O(pas, 0xd1, b)
for b in modrm16():
    O(pas, pos, 0xd1, b)


# (ROL|ROR|RCL|RCR|SHL|SHR|SAL|SAR) r/m8, CL
for b in modrm32():
    O(0xd2, b)
for b in modrm16():
    O(pas, 0xd2, b)


# (ROL|ROR|RCL|RCR|SHL|SHR|SAL|SAR) r/m16/32, CL
for b in modrm32():
    O(0xd3, b)
for b in modrm32():
    O(pos, 0xd3, b)
for b in modrm16():
    O(pas, 0xd3, b)
for b in modrm16():
    O(pas, pos, 0xd3, b)


# AAM AL, AH(, imm8)?
O(0xd4, 0x0a)
O(0xd4, imm8)


# AAD AL, AH(, imm8)?
O(0xd5, 0x0a)
O(0xd5, imm8)


# SALC
O(0xd6)


# XLAT AL, m8
O(0xd7)


# (FADD|FMUL|FCOM|FCOMP|FSUB|FSUBR|FDIV|FDIVR) ST STi/m32real
for b in modrm32():
    O(0xd8, b)
for b in modrm16():
    O(pas, 0xd8, b)


# FLD ST STi/m32real
for b in modrm32(regonly=[0]):
    O(0xd9, b)
for b in modrm16(regonly=[0]):
    O(pas, 0xd9, b)
# FXCH ST, STi
for b in modrm32(modonly=[3], regonly=[1]):
    O(0xd9, b)
# FST m32real, ST
for b in modrm32(modonly=[0, 1, 2], regonly=[2]):
    O(0xd9, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[2]):
    O(pas, 0xd9, b)
# FNOP
O(0xd9, 0xd0)
# FSTP STi/m32real, ST
for b in modrm32(regonly=[3]):
    O(0xd9, b)
for b in modrm16(regonly=[3]):
    O(pas, 0xd9, b)
# FLDENV m14/28
for b in modrm32(modonly=[0, 1, 2], regonly=[4]):
    O(0xd9, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[4]):
    O(pas, 0xd9, b)
# FCHS ST
O(0xd9, 0xe0)
# FABS ST
O(0xd9, 0xe1)
# FTST ST
O(0xd9, 0xe4)
# FXAM ST
O(0xd9, 0xe5)
# FLDCW m16
for b in modrm32(modonly=[0, 1, 2], regonly=[5]):
    O(0xd9, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[5]):
    O(pas, 0xd9, b)
# FLD1 ST
O(0xd9, 0xe8)
# FLDL2T ST
O(0xd9, 0xe9)
# FLDL2E ST
O(0xd9, 0xea)
# FLDPI ST
O(0xd9, 0xeb)
# FLDLG2 ST
O(0xd9, 0xec)
# FLDLN2 ST
O(0xd9, 0xed)
# FLDZ ST
O(0xd9, 0xee)
# FN?STENV m14/28
for b in modrm32(modonly=[0, 1, 2], regonly=[6]):
    O(0xd9, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[6]):
    O(pas, 0xd9, b)
# (F2XM1|FYL2X|FPTAN|FPATAN|FXTRACT|FPREM1|FDECSTP|FINCSTP)
for b in modrm32(modonly=[3], regonly=[6]):
    O(0xd9, b)
# FN?STCW m16
for b in modrm32(modonly=[0, 1, 2], regonly=[7]):
    O(0xd9, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[7]):
    O(pas, 0xd9, b)
# (FPREM|FYL2XP1|FSQRT|FSINCOS|FRNDINT|FSCALE|FSIN|FCOS)
for b in modrm32(modonly=[3], regonly=[7]):
    O(0xd9, b)


# (FIADD|FIMUL|FICOM|FICOMP|FISUB|FISUBR|FIDIV|FIDIVR) ST, m32int
for b in modrm32(modonly=[0, 1, 2]):
    O(0xda, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0xda, b)
# (FCMOVB|FCMOVE|FCMOVBE|FCMOVU) ST, STi
for b in modrm32(modonly=[3], regonly=[0, 1, 2, 3]):
    O(0xda, b)
# FUCOMPP ST, ST1
O(0xda, 0xe9)


# (FILD|FISTTP|FIST|FISTP|FCMOVNB|FCMOVNE|FCMOVENBE|FCMOVNU)
for b in modrm32(regonly=[0, 1, 2, 3]):
    O(0xdb, b)
for b in modrm16(regonly=[0, 1, 2, 3]):
    O(pas, 0xdb, b)
# FNENI
O(0xdb, 0xe0)
# FNDISI
O(0xdb, 0xe1)
# FNCLEX
O(0xdb, 0xe2)
# FNINIT
O(0xdb, 0xe3)
# FNSETPM
O(0xdb, 0xe4)
# (FLD|FSTP)
for b in modrm32(modonly=[0, 1, 2], regonly=[5, 7]):
    O(0xdb, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[5, 7]):
    O(pas, 0xdb, b)
# (FUCOMI|FCOMI)
for b in modrm32(modonly=[3], regonly=[5, 6]):
    O(0xdb, b)


# (FADD|FMUL|FCOM|FCOM2|FCOMP|FCOMP3|FSUB|FSUBR|FDIV|FDIVR)
for b in modrm32():
    O(0xdc, b)
for b in modrm16():
    O(pas, 0xdc, b)


# (FLD|FISTTP|FST|FSTP|FFREE|FXCH4)
for b in modrm32(regonly=[0, 1, 2, 3]):
    O(0xdd, b)
for b in modrm16(regonly=[0, 1, 2, 3]):
    O(pas, 0xdd, b)
# (FRSTOR|FUCOM|FUCOMP)
for b in modrm32(modonly=[3], regonly=[4, 5]):
    O(0xdd, b)
# (FN?SAVE|FN?STSW)
for b in modrm32(modonly=[0, 1, 2], regonly=[6, 7]):
    O(0xdd, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[6, 7]):
    O(pas, 0xdd, b)


# (FIADD|FIMUL|FICOM|FICOMP|FISUB|FISUBR|FIDIV|FIDIVR)
for b in modrm32(modonly=[0, 1, 2]):
    O(0xde, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0xde, b)
# (FADDP|FMULP|FCOMP5|FSUBRP|FSUBP|FDIVRP|FDIVP)
for b in modrm32(modonly=[3], regonly=[0, 1, 2, 4, 5, 6, 7]):
    O(0xde, b)
# FCOMPP
O(0xde, 0xd9)


# (FILD|FISTTP|FIST|FISTP|FBLD|FBSTP|FISTP)
for b in modrm32(modonly=[0, 1, 2]):
    O(0xdf, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, 0xdf, b)
# (FFREEP|FXCH7|FSTP8|FSTP9|FUCOMIP|FCOMIP)
for b in modrm32(modonly=[3], regonly=[0, 1, 2, 3, 5, 6]):
    O(0xdf, b)
# FNSTSW
O(0xdf, 0xe0)


# LOOPNZ E?CX, rel8
O(0xe0, rel8)
O(pas, 0xe0, rel8)


# LOOPZ E?CX, rel8
O(0xe1, rel8)
O(pas, 0xe1, rel8)


# LOOP E?CX, rel8
O(0xe2, rel8)
O(pas, 0xe2, rel8)


# JCXZ rel8, E?CX
O(0xe3, rel8)
O(pas, 0xe3, rel8)


# IN AL, imm8
O(0xe4, imm8)


# IN E?AX, imm8
O(0xe5, imm8)
O(pos, 0xe5, imm8)


# OUT imm8, AL
O(0xe6, imm8)


# OUT imm8, E?AX
O(0xe7, imm8)
O(pos, 0xe7, imm8)


# CALL rel16/32
O(0xe8, rel32)
O(pos, 0xe8, rel16)


# JMP rel16/32
O(0xe9, rel32)
O(pos, 0xe9, rel16)


# JMPF ptr16:16/32
O(0xea, ptr16_32)
O(pos, 0xea, ptr16_16)


# JMP rel8
O(0xeb, rel8)


# IN AL, DX
O(0xec)


# IN E?AX, DX
O(0xed)
O(pos, 0xed)


# OUT DX, AL
O(0xee)


# OUT DX, E?AX
O(0xef)
O(pos, 0xef)


# 0xf0 Lock prefix


# INT1
O(0xf1)


# 0xf2 (REPNZ|REP) Repeat string operation or Scalar double-precision prefix


# 0xf3 (REPZ|REP) Repeat string operation or Scalar single-precision prefix


# HALT
O(0xf4)


# CMC
O(0xf5)


# TEST r/m8, imm8
for b in modrm32(regonly=[0, 1]):
    O(0xf6, b, imm8)
for b in modrm16(regonly=[0, 1]):
    O(pas, 0xf6, b, imm8)
# (NOT|NEG|MUL|IMUL|DIV|IDIV)
for b in modrm32(regonly=[2, 3, 4, 5, 6, 7]):
    O(0xf6, b)
for b in modrm16(regonly=[2, 3, 4, 5, 6, 7]):
    O(pas, 0xf6, b)


# TEST r/m16/32, imm16/32
for b in modrm32(regonly=[0, 1]):
    O(0xf7, b, imm32)
for b in modrm32(regonly=[0, 1]):
    O(pos, 0xf7, b, imm16)
for b in modrm16(regonly=[0, 1]):
    O(pas, 0xf7, b, imm32)
for b in modrm16(regonly=[0, 1]):
    O(pas, pos, 0xf7, b, imm16)
# (NOT|NEG|MUL|IMUL|DIV|IDIV)
for b in modrm32(regonly=[2, 3, 4, 5, 6, 7]):
    O(0xf7, b)
for b in modrm32(regonly=[2, 3, 4, 5, 6, 7]):
    O(pos, 0xf7, b)
for b in modrm16(regonly=[2, 3, 4, 5, 6, 7]):
    O(pas, 0xf7, b)
for b in modrm16(regonly=[2, 3, 4, 5, 6, 7]):
    O(pas, pos, 0xf7, b)


# CLC
O(0xf8)


# STC
O(0xf9)


# CLI
O(0xfa)


# STI
O(0xfb)


# CLD
O(0xfc)


# STD
O(0xfd)


# (INC|DEC) r/m8
for b in modrm32(regonly=[0, 1]):
    O(0xfe, b)
for b in modrm16(regonly=[0, 1]):
    O(pas, 0xfe, b)


# (INC|DEC|CALL|JMP|PUSH) r/m16/32
for b in modrm32(regonly=[0, 1, 2, 4, 6]):
    O(0xff, b)
for b in modrm32(regonly=[0, 1, 2, 4, 6]):
    O(pos, 0xff, b)
for b in modrm16(regonly=[0, 1, 2, 4, 6]):
    O(pas, 0xff, b)
for b in modrm16(regonly=[0, 1, 2, 4, 6]):
    O(pas, pos, 0xff, b)
# (CALLF|JMPF) m16:16/32
for b in modrm32(modonly=[0, 1, 2], regonly=[3, 5]):
    O(0xff, b)
for b in modrm32(modonly=[0, 1, 2], regonly=[3, 5]):
    O(pos, 0xff, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[3, 5]):
    O(pas, 0xff, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[3, 5]):
    O(pas, pos, 0xff, b)


# (SLDT|STR|LLDT|LTR|VERR|VERW)
for b in modrm32(regonly=[0, 1, 2, 3, 4, 5]):
    O(p2b, 0x00, b)
for b in modrm16(regonly=[0, 1, 2, 3, 4, 5]):
    O(pas, p2b, 0x00, b)


# SGDT
for b in modrm32(modonly=[0, 1, 2], regonly=[0]):
    O(p2b, 0x01, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[0]):
    O(pas, p2b, 0x01, b)
# VMCALL
O(p2b, 0x01, 0xc1)
# VMLAUNCH
O(p2b, 0x01, 0xc2)
# VMRESUME
O(p2b, 0x01, 0xc3)
# VMXOFF
O(p2b, 0x01, 0xc4)
# SIDT
for b in modrm32(modonly=[0, 1, 2], regonly=[1]):
    O(p2b, 0x01, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[1]):
    O(pas, p2b, 0x01, b)
# MONITOR
O(p2b, 0x01, 0xc8)
# MWAIT
O(p2b, 0x01, 0xc9)
# CLAC
O(p2b, 0x01, 0xca)
# STAC
O(p2b, 0x01, 0xca)
# LGDT
for b in modrm32(modonly=[0, 1, 2], regonly=[2]):
    O(p2b, 0x01, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[2]):
    O(pas, p2b, 0x01, b)
# XGETBV
O(p2b, 0x01, 0xd0)
# XSETBV
O(p2b, 0x01, 0xd1)
# (LIDT|VMRUN|VMMCALL|VMLOAD|VMSAVE|STGI|CLGI|SKINIT|INVLPGA)
for b in modrm32(modonly=[0, 1, 2], regonly=[3]):
    O(p2b, 0x01, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[3]):
    O(pas, p2b, 0x01, b)
# SMSW
for b in modrm32(regonly=[4]):
    O(p2b, 0x01, b)
for b in modrm16(regonly=[4]):
    O(pas, p2b, 0x01, b)
# LMSW
for b in modrm32(regonly=[6]):
    O(p2b, 0x01, b)
for b in modrm16(regonly=[6]):
    O(pas, p2b, 0x01, b)
# INVLPG
for b in modrm32(modonly=[0, 1, 2], regonly=[7]):
    O(p2b, 0x01, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[7]):
    O(pas, p2b, 0x01, b)
# SWAPGS
O(p2b, 0x01, 0xf8)
# RTDSCP
O(p2b, 0x01, 0xf9)


# LAR
for b in modrm32():
    O(p2b, 0x02, b)
for b in modrm32():
    O(pos, p2b, 0x02, b)
for b in modrm16():
    O(pas, p2b, 0x02, b)
for b in modrm16():
    O(pas, pos, p2b, 0x02, b)


# LSL
for b in modrm32():
    O(p2b, 0x03, b)
for b in modrm32():
    O(pos, p2b, 0x03, b)
for b in modrm16():
    O(pas, p2b, 0x03, b)
for b in modrm16():
    O(pas, pos, p2b, 0x03, b)


# 0x0f 0x04 NA


# 0x0f 0x05 NA


# CLTS
O(p2b, 0x06)


# 0x0f 0x07 NA


# INVD
O(p2b, 0x08)


# WBINVD
O(p2b, 0x09)


# 0x0f 0x0a NA


# UD2
O(p2b, 0x0b)


# 0x0f 0x0c NA


# Capstone doesn't disassemble this so we'll skip it
# (PREFETCH|PREFETCHW|PREFETCHWT1)
#for b in modrm32(modonly=[0, 1, 2], regonly=[0, 1, 2]):
#    O(p2b, 0x0d, b)
#for b in modrm16(modonly=[0, 1, 2], regonly=[0, 1, 2]):
#    O(pas, p2b, 0x0d, b)


# FEMMS
O(p2b, 0x0e)


# 0x0f 0x0f Reserved


# (MOVUPS|MOVSS|MOVUPD|MOVSD) xmm, xmm/m32/64/218
for b in modrm32():
    O(p2b, 0x10, b)
for b in modrm32():
    O(pos, p2b, 0x10, b)
for b in modrm32():
    O(psp, p2b, 0x10, b)
for b in modrm32():
    O(pdp, p2b, 0x10, b)
for b in modrm16():
    O(pas, p2b, 0x10, b)
for b in modrm16():
    O(pas, pos, p2b, 0x10, b)
for b in modrm16():
    O(pas, psp, p2b, 0x10, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x10, b)


# (MOVUPS|MOVSS|MOVUPD|MOVSD) xmm/m32/64/218, xmm
for b in modrm32():
    O(p2b, 0x11, b)
for b in modrm32():
    O(pos, p2b, 0x11, b)
for b in modrm32():
    O(psp, p2b, 0x11, b)
for b in modrm32():
    O(pdp, p2b, 0x11, b)
for b in modrm16():
    O(pas, p2b, 0x11, b)
for b in modrm16():
    O(pas, pos, p2b, 0x11, b)
for b in modrm16():
    O(pas, psp, p2b, 0x11, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x11, b)


# (MOVHLPS|MOVLPS|MOVLPD|MOVDDUP|MOVSLDUP)
for b in modrm32():
    O(p2b, 0x12, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x12, b)
for b in modrm32():
    O(psp, p2b, 0x12, b)
for b in modrm32():
    O(pdp, p2b, 0x12, b)
for b in modrm16():
    O(pas, p2b, 0x12, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x12, b)
for b in modrm16():
    O(pas, psp, p2b, 0x12, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x12, b)


# (MOVLPS|MOVLPD)
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x13, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x13, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x13, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x13, b)


# (UNPCKLPS|UNPCKLPD)
for b in modrm32():
    O(p2b, 0x14, b)
for b in modrm32():
    O(pos, p2b, 0x14, b)
for b in modrm16():
    O(pas, p2b, 0x14, b)
for b in modrm16():
    O(pas, pos, p2b, 0x14, b)


# (UNPCKHPS|UNPCKHPD)
for b in modrm32():
    O(p2b, 0x15, b)
for b in modrm32():
    O(pos, p2b, 0x15, b)
for b in modrm16():
    O(pas, p2b, 0x15, b)
for b in modrm16():
    O(pas, pos, p2b, 0x15, b)


# (MOVLHPS|MOVHPS|MOVHPD|MOVHDUP)
for b in modrm32():
    O(p2b, 0x16, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x16, b)
for b in modrm32():
    O(psp, p2b, 0x16, b)
for b in modrm16():
    O(pas, p2b, 0x16, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x16, b)
for b in modrm16():
    O(pas, psp, p2b, 0x16, b)


# (MOVHPS|MOVHPD)
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x17, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x17, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x17, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x17, b)


# (PREFETCHNTA|PREFETCH0|PREFETCH1|PREFETCH2)
for b in modrm32(modonly=[0, 1, 2], regonly=[0, 1, 2, 3]):
    O(p2b, 0x18, b)
for b in modrm16(modonly=[0, 1, 2], regonly=[0, 1, 2, 3]):
    O(pas, p2b, 0x18, b)
# HINT_NOP
for b in modrm32(regonly=[4, 5, 6, 7]):
    O(p2b, 0x18, b)
for b in modrm32(regonly=[4, 5, 6, 7]):
    O(pos, p2b, 0x18, b)
for b in modrm16(regonly=[4, 5, 6, 7]):
    O(pas, p2b, 0x18, b)
for b in modrm16(regonly=[4, 5, 6, 7]):
    O(pas, pos, p2b, 0x18, b)


# HINT_NOP
for b in modrm32():
    O(p2b, 0x19, b)
for b in modrm32():
    O(pos, p2b, 0x19, b)
for b in modrm16():
    O(pas, p2b, 0x19, b)
for b in modrm16():
    O(pas, pos, p2b, 0x19, b)


# NOTE: It gets a bit weird here just do things supported by Capstone
# HINT_NOP
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x1a, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x1a, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x1a, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x1a, b)


# NOTE: It gets a bit weird here just do things supported by Capstone
# HINT_NOP
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x1b, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x1b, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x1b, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x1b, b)


# NOTE: It gets a bit weird here just do things supported by Capstone
# HINT_NOP
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x1c, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x1c, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x1c, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x1c, b)


# NOTE: It gets a bit weird here just do things supported by Capstone
# HINT_NOP
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x1d, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x1d, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x1d, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x1d, b)


# NOTE: It gets a bit weird here just do things supported by Capstone
# HINT_NOP
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x1e, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x1e, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x1e, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x1e, b)


# NOTE: It gets a bit weird here just do things supported by Capstone
# HINT_NOP
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x1f, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x1f, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x1f, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x1f, b)


# NOTE: not really modrm, since mod 00, 01, 10 map to 11
# MOV r32, CRn
for b in range(0xff + 1):
    O(p2b, 0x20, b)


# NOTE: not really modrm, since mod 00, 01, 10 map to 11
# MOV r32, DRn
for b in range(0xff + 1):
    O(p2b, 0x21, b)


# NOTE: not really modrm, since mod 00, 01, 10 map to 11
# MOV CRn, r32
for b in range(0xff + 1):
    O(p2b, 0x22, b)


# NOTE: not really modrm, since mod 00, 01, 10 map to 11
# MOV DRn, r32
for b in range(0xff + 1):
    O(p2b, 0x23, b)


# 0x0f 0x24-0x27 NA


# (MOVAPS|MOVAPD) xmm, xmm/m128
for b in modrm32():
    O(p2b, 0x28, b)
for b in modrm32():
    O(pos, p2b, 0x28, b)
for b in modrm16():
    O(pas, p2b, 0x28, b)
for b in modrm16():
    O(pas, pos, p2b, 0x28, b)


# (MOVAPS|MOVAPD) xmm/m128, xmm
for b in modrm32():
    O(p2b, 0x29, b)
for b in modrm32():
    O(pos, p2b, 0x29, b)
for b in modrm16():
    O(pas, p2b, 0x29, b)
for b in modrm16():
    O(pas, pos, p2b, 0x29, b)


# (CVTPI2PS|CVTSI2SS|CVTPI2PD|CVTSI2SD)
for b in modrm32():
    O(p2b, 0x2a, b)
for b in modrm32():
    O(pos, p2b, 0x2a, b)
for b in modrm32():
    O(psp, p2b, 0x2a, b)
for b in modrm32():
    O(pdp, p2b, 0x2a, b)
for b in modrm16():
    O(pas, p2b, 0x2a, b)
for b in modrm16():
    O(pas, pos, p2b, 0x2a, b)
for b in modrm16():
    O(pas, psp, p2b, 0x2a, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x2a, b)


# (MOVNTPS|MOVNTPD)
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x2b, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x2b, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, p2b, 0x2b, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x2b, b)


# (CVTTPS2PI|CVTTSS2SI|CVTTPD2PI|CVTTSD2SI)
for b in modrm32():
    O(p2b, 0x2c, b)
for b in modrm32():
    O(pos, p2b, 0x2c, b)
for b in modrm32():
    O(psp, p2b, 0x2c, b)
for b in modrm32():
    O(pdp, p2b, 0x2c, b)
for b in modrm16():
    O(pas, p2b, 0x2c, b)
for b in modrm16():
    O(pas, pos, p2b, 0x2c, b)
for b in modrm16():
    O(pas, psp, p2b, 0x2c, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x2c, b)


# (CVTPS2PI|CVTSS2SI|CVTPD2PI|CVTSD2SI)
for b in modrm32():
    O(p2b, 0x2d, b)
for b in modrm32():
    O(pos, p2b, 0x2d, b)
for b in modrm32():
    O(psp, p2b, 0x2d, b)
for b in modrm32():
    O(pdp, p2b, 0x2d, b)
for b in modrm16():
    O(pas, p2b, 0x2d, b)
for b in modrm16():
    O(pas, pos, p2b, 0x2d, b)
for b in modrm16():
    O(pas, psp, p2b, 0x2d, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x2d, b)


# (UCOMISS|UCOMISD)
for b in modrm32():
    O(p2b, 0x2e, b)
for b in modrm32():
    O(pos, p2b, 0x2e, b)
for b in modrm16():
    O(pas, p2b, 0x2e, b)
for b in modrm16():
    O(pas, pos, p2b, 0x2e, b)


# (COMISS|COMISD)
for b in modrm32():
    O(p2b, 0x2f, b)
for b in modrm32():
    O(pos, p2b, 0x2f, b)
for b in modrm16():
    O(pas, p2b, 0x2f, b)
for b in modrm16():
    O(pas, pos, p2b, 0x2f, b)


# WRMSR
O(p2b, 0x30)


# RDTSC
O(p2b, 0x31)


# RDMSR
O(p2b, 0x32)


# RDPMC
O(p2b, 0x33)


# SYSENTER
O(p2b, 0x34)


# SYSEXIT
O(p2b, 0x35)


# 0x0f 0x36 NA


# GETSEC
O(p2b, 0x37)


# NOTE: Variation on modrm for 0x0f 0x39 (byte + modrm)
# (PSHUFB|PHADDW|PHADDD|PHADDSW|PMADDUBSW|PHSUBW|PHSUBD|PHSUBSW|PSIGNB|PSIGNW|PSIGND|PMULHRSW)
for o in range(0x0b + 1):
    for b in modrm32():
        O(p2b, 0x38, o, b)
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# (PBLENDVB|BLENDVPS|BLENDVPD|PTEST)
for o in (0x10, 0x14, 0x15, 0x17):
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# (PABSB|PABSW|PABSD)
for o in range(0x1c, 0x1e + 1):
    for b in modrm32():
        O(p2b, 0x38, o, b)
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# (PMOVSXBW|PMOVSXBD|PMOVSXBQ|PMOVSXWD|PMOVSXWQ|PMOVSXDQ)
for o in range(0x20, 0x25 + 1):
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# (PMULDQ|PCMPEQQ)
for o in (0x28, 0x29):
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# MOVNTDQA
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x38, 0x2a, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x38, 0x2a, b)
# PACKUSDW
for b in modrm32():
    O(pos, p2b, 0x38, 0x2b, b)
for b in modrm16():
    O(pas, pos, p2b, 0x38, 0x2b, b)
# (PMOVZXBW|PMOVZXBD|PMOVZXBQ|PMOVZXWD|PMOVZXWQ|PMOVZXDQ)
for o in range(0x30, 0x35 + 1):
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# (PCMPGTQ|PMINSB|PMINSD|PMINUW|PMINUD|PMAXSB|PMAXSD|PMAXUW|PMAXUD|PMULLD|PHMINPOSUW)
for o in range(0x37, 0x41 + 1):
    for b in modrm32():
        O(pos, p2b, 0x38, o, b)
    for b in modrm16():
        O(pas, pos, p2b, 0x38, o, b)
# (INVEPT|INVVPID)
for o in (0x80, 0x81):
    for b in modrm32(modonly=[0, 1, 2]):
        O(pos, p2b, 0x38, o, b)
    for b in modrm16(modonly=[0, 1, 2]):
        O(pas, pos, p2b, 0x38, o, b)
# MOVBE r16/32, m16/32
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x38, 0xf0, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x38, 0xf0, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x38, 0xf0, b)
# CRC32 r32, r/m8
for b in modrm32():
    O(pdp, p2b, 0x38, 0xf0, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x38, 0xf0, b)
# MOVBE m16/32, r16/32
for b in modrm32(modonly=[0, 1, 2]):
    O(p2b, 0x38, 0xf1, b)
for b in modrm32(modonly=[0, 1, 2]):
    O(pos, p2b, 0x38, 0xf1, b)
for b in modrm16(modonly=[0, 1, 2]):
    O(pas, pos, p2b, 0x38, 0xf1, b)
# CRC32 r32, r/m16/32
for b in modrm32():
    O(pdp, p2b, 0x38, 0xf1, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x38, 0xf1, b)


# NOTE: 0x0f 0x39 NA


# NOTE: Variation on modrm for 0x0f 0x3a (byte + modrm)
# (ROUNDPS|ROUNDPD|ROUNDSS|ROUNDSD|BLENDPS|BLENDPD|PBLENDW)
for o in range(0x08, 0x0e + 1):
    for b in modrm32():
        O(pos, p2b, 0x3a, o, b, imm8)
    for b in modrm16():
        O(pas, pos, p2b, 0x3a, o, b, imm8)
# PALIGNR
for b in modrm32():
    O(p2b, 0x3a, 0x0f, b, imm8)
for b in modrm32():
    O(pos, p2b, 0x3a, 0x0f, b, imm8)
for b in modrm16():
    O(pas, p2b, 0x3a, 0x0f, b, imm8)
for b in modrm16():
    O(pas, pos, p2b, 0x3a, 0x0f, b, imm8)
# (PEXTRB|PEXTRW|PEXTRD|EXTRACTPS)
for o in range(0x14, 0x17 + 1):
    for b in modrm32():
        O(pos, p2b, 0x3a, o, b, imm8)
    for b in modrm16():
        O(pas, pos, p2b, 0x3a, o, b, imm8)
# (PINSRB|INSERTPS|PINSRD)
for o in range(0x20, 0x22 + 1):
    for b in modrm32():
        O(pos, p2b, 0x3a, o, b, imm8)
    for b in modrm16():
        O(pas, pos, p2b, 0x3a, o, b, imm8)
# (DPPS|DPPD|MPSADBW)
for o in range(0x40, 0x42 + 1):
    for b in modrm32():
        O(pos, p2b, 0x3a, o, b, imm8)
    for b in modrm16():
        O(pas, pos, p2b, 0x3a, o, b, imm8)
# (PCMPESTRM|PCMPESTRI|PCMPISTRM|PCMPISTRI)
for o in range(0x60, 0x63 + 1):
    for b in modrm32():
        O(pos, p2b, 0x3a, o, b, imm8)
    for b in modrm16():
        O(pas, pos, p2b, 0x3a, o, b, imm8)


# NOTE: 0x0f 0x3b-0x3f NA


# (CMOVO|CMOVNO|CMOVB|CMOVNB|CMOVZ|CMOVNZ|CMOVBE|CMOVNBE|CMOVS|CMOVNS|CMOVP|CMOVNP|CMOVL|CMOVNL|CMOVLE|CMOVNLE)
for op in range(0x40, 0x4f + 1):
    for b in modrm32():
        O(p2b, op, b)
    for b in modrm32():
        O(pos, p2b, op, b)
    for b in modrm16():
        O(pas, p2b, op, b)
    for b in modrm16():
        O(pas, pos, p2b, op, b)


# (MOVMSKPS|MOVMSKPD)
for b in modrm32(modonly=[3]):
    O(p2b, 0x50, b)
for b in modrm32(modonly=[3]):
    O(pos, p2b, 0x50, b)


# (SQRTPS|SQRTSS|SQRTPD|SQRTSD)
for b in modrm32():
    O(p2b, 0x51, b)
for b in modrm32():
    O(pos, p2b, 0x51, b)
for b in modrm32():
    O(pdp, p2b, 0x51, b)
for b in modrm32():
    O(psp, p2b, 0x51, b)
for b in modrm16():
    O(pas, p2b, 0x51, b)
for b in modrm16():
    O(pas, pos, p2b, 0x51, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x51, b)
for b in modrm16():
    O(pas, psp, p2b, 0x51, b)


# (RSQRTPS|RSQRTSS)
for b in modrm32():
    O(p2b, 0x52, b)
for b in modrm32():
    O(psp, p2b, 0x52, b)
for b in modrm16():
    O(pas, p2b, 0x52, b)
for b in modrm16():
    O(pas, psp, p2b, 0x52, b)


# (RCPPS|RCPSS)
for b in modrm32():
    O(p2b, 0x53, b)
for b in modrm32():
    O(psp, p2b, 0x53, b)
for b in modrm16():
    O(pas, p2b, 0x53, b)
for b in modrm16():
    O(pas, psp, p2b, 0x53, b)


# (ANDPS|ANDPD)
for b in modrm32():
    O(p2b, 0x54, b)
for b in modrm32():
    O(pos, p2b, 0x54, b)
for b in modrm16():
    O(pas, p2b, 0x54, b)
for b in modrm16():
    O(pas, pos, p2b, 0x54, b)


# (ANDNPS|ANDNPD)
for b in modrm32():
    O(p2b, 0x55, b)
for b in modrm32():
    O(pos, p2b, 0x55, b)
for b in modrm16():
    O(pas, p2b, 0x55, b)
for b in modrm16():
    O(pas, pos, p2b, 0x55, b)


# (ORPS|ORPD)
for b in modrm32():
    O(p2b, 0x56, b)
for b in modrm32():
    O(pos, p2b, 0x56, b)
for b in modrm16():
    O(pas, p2b, 0x56, b)
for b in modrm16():
    O(pas, pos, p2b, 0x56, b)


# (XORPS|XORPD)
for b in modrm32():
    O(p2b, 0x57, b)
for b in modrm32():
    O(pos, p2b, 0x57, b)
for b in modrm16():
    O(pas, p2b, 0x57, b)
for b in modrm16():
    O(pas, pos, p2b, 0x57, b)


# (ADDPS|ADDSS|ADDPD|ADDSD)
for b in modrm32():
    O(p2b, 0x58, b)
for b in modrm32():
    O(pos, p2b, 0x58, b)
for b in modrm32():
    O(pdp, p2b, 0x58, b)
for b in modrm32():
    O(psp, p2b, 0x58, b)
for b in modrm16():
    O(pas, p2b, 0x58, b)
for b in modrm16():
    O(pas, pos, p2b, 0x58, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x58, b)
for b in modrm16():
    O(pas, psp, p2b, 0x58, b)


# (MULPS|MULSS|MULPD|MULSD)
for b in modrm32():
    O(p2b, 0x59, b)
for b in modrm32():
    O(pos, p2b, 0x59, b)
for b in modrm32():
    O(pdp, p2b, 0x59, b)
for b in modrm32():
    O(psp, p2b, 0x59, b)
for b in modrm16():
    O(pas, p2b, 0x59, b)
for b in modrm16():
    O(pas, pos, p2b, 0x59, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x59, b)
for b in modrm16():
    O(pas, psp, p2b, 0x59, b)


# (CVTPS2PD|CVTPD2PS|CVTSS2SD|CVTSD2SS)
for b in modrm32():
    O(p2b, 0x5a, b)
for b in modrm32():
    O(pos, p2b, 0x5a, b)
for b in modrm32():
    O(pdp, p2b, 0x5a, b)
for b in modrm32():
    O(psp, p2b, 0x5a, b)
for b in modrm16():
    O(pas, p2b, 0x5a, b)
for b in modrm16():
    O(pas, pos, p2b, 0x5a, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x5a, b)
for b in modrm16():
    O(pas, psp, p2b, 0x5a, b)


# (CVTDQ2PS|CVTPS2DQ|CVTTPS2DQ)
for b in modrm32():
    O(p2b, 0x5b, b)
for b in modrm32():
    O(pos, p2b, 0x5b, b)
for b in modrm32():
    O(psp, p2b, 0x5b, b)
for b in modrm16():
    O(pas, p2b, 0x5b, b)
for b in modrm16():
    O(pas, pos, p2b, 0x5b, b)
for b in modrm16():
    O(pas, psp, p2b, 0x5b, b)


# (SUBPS|SUBSS|SUBPD|SUBSD)
for b in modrm32():
    O(p2b, 0x5c, b)
for b in modrm32():
    O(pos, p2b, 0x5c, b)
for b in modrm32():
    O(pdp, p2b, 0x5c, b)
for b in modrm32():
    O(psp, p2b, 0x5c, b)
for b in modrm16():
    O(pas, p2b, 0x5c, b)
for b in modrm16():
    O(pas, pos, p2b, 0x5c, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x5c, b)
for b in modrm16():
    O(pas, psp, p2b, 0x5c, b)


# (MINPS|MINSS|MINPD|MINSD)
for b in modrm32():
    O(p2b, 0x5d, b)
for b in modrm32():
    O(pos, p2b, 0x5d, b)
for b in modrm32():
    O(pdp, p2b, 0x5d, b)
for b in modrm32():
    O(psp, p2b, 0x5d, b)
for b in modrm16():
    O(pas, p2b, 0x5d, b)
for b in modrm16():
    O(pas, pos, p2b, 0x5d, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x5d, b)
for b in modrm16():
    O(pas, psp, p2b, 0x5d, b)


# (DIVPS|DIVSS|DIVPD|DIVSD)
for b in modrm32():
    O(p2b, 0x5e, b)
for b in modrm32():
    O(pos, p2b, 0x5e, b)
for b in modrm32():
    O(pdp, p2b, 0x5e, b)
for b in modrm32():
    O(psp, p2b, 0x5e, b)
for b in modrm16():
    O(pas, p2b, 0x5e, b)
for b in modrm16():
    O(pas, pos, p2b, 0x5e, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x5e, b)
for b in modrm16():
    O(pas, psp, p2b, 0x5e, b)


# (MAXPS|MAXSS|MAXPD|MAXSD)
for b in modrm32():
    O(p2b, 0x5f, b)
for b in modrm32():
    O(pos, p2b, 0x5f, b)
for b in modrm32():
    O(pdp, p2b, 0x5f, b)
for b in modrm32():
    O(psp, p2b, 0x5f, b)
for b in modrm16():
    O(pas, p2b, 0x5f, b)
for b in modrm16():
    O(pas, pos, p2b, 0x5f, b)
for b in modrm16():
    O(pas, pdp, p2b, 0x5f, b)
for b in modrm16():
    O(pas, psp, p2b, 0x5f, b)
