# Makefile for x86 Length Disassembler.
# Copyright (C) 2013 Byron Platt
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#CC=x86_64-w64-mingw32-gcc

# the -m32 is just for the test program
CFLAGS=-m32 -Wall -ansi -Os
LDFLAGS=-m32

SRCS=$(wildcard *.c)
OBJS=$(SRCS:.c=.o)

ld32test: $(OBJS)

clean:
	rm -f $(OBJS)
