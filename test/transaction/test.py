
import struct

B =  struct.pack("<L", 1)
A = struct.pack("<L", 1)

C = (
    B + A
)

print C