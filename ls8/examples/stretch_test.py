#results should be
# AND - 4
# OR  - 31
# XOR - 27
# NOT - 240
# SHR - 3
# SHL - 60
# MOD - 3
10000010 # LDI R0,15
00000000
00001111
10000010 # LDI R1,20
00000001
00010100
10101000 # AND R0, R1
00000000
00000001
01000111 # PRN R0
00000000
10000010 # LDI R0,15
00000000
00001111
10000010 # LDI R1,20
00000001
00010100
10101010 # OR R0, R1
00000000
00000001
01000111 # PRN R0
00000000
10000010 # LDI R0,15
00000000
00001111
10000010 # LDI R1,20
00000001
00010100
10101011 # XOR R0, R1
00000000
00000001
01000111 # PRN R0
00000000
10000010 # LDI R0,15
00000000
00001111
01101001 # NOT R0, R1
00000000
01000111 # PRN R0
00000000
10000010 # LDI R0,15
00000000
00001111
10000010 # LDI R1,2
00000001
00000010
10101101 # SHR R0, R1
00000000
00000001
01000111 # PRN R0
00000000
10000010 # LDI R0,15
00000000
00001111
10000010 # LDI R1,2
00000001
00000010
10101100 # SHL R0, R1
00000000
00000001
01000111 # PRN R0
00000000
10000010 # LDI R0,15
00000000
00001111
10000010 # LDI R1,4
00000001
00000100
10100100 # MOD R0, R1
00000000
00000001
01000111 # PRN R0
00000000
00000001 #HLT