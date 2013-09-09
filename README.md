lend
====

Tiny x86 Length Disassembler

The inspiration for the design of this x86 length disassembler came from
Zdisasm by Z0MBiE (I can't actually find this on his page but it's around,
just google code search for zdisasm.h) and three ideas presented nicely in a
single forum thread:

http://www.devmaster.net/forums/showthread.php?t=2311

The three ideas came from the following posts:

1. The original post by Nick (a purely logical length disassembler)
2. The post by earlnsk (a Russian switch case length disassembler)
   The Russian length disassembler can be found here:
       http://hack-expo.void.ru/groups/blt/text/disasm.txt (Russian)
       http://z0mbie.daemonlab.org/disasme.txt (English)
3. The post by WolfgangSt (bitmap lookup tables)

With these ideas I decided to make a tiny length disassemler in c.

My length disassembler can use logical statements or lookup tables (32 byte
bitmap tables) to perform the checks required to determine instruction length.
Currently the smallest footprint I have managed is 589 bytes (LengthDisasm
function length + 4x32 byte lookup tables). I'm sure there are further
optimizations possible (even without using assembly).

I haven't looked into it too much but I don't think it would to too difficult
to adapt this approach for x86_64.
