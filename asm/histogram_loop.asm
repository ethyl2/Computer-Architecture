; # --------------- Set up
LDI R0,1 ; <- initial num of *s (starts as 1)
LDI R1, 1  ; <- initial num of desired *s (starts as 1)
LDI R2, 2 ; <- num to multiply by (2)
LDI R3, 42 ; (ascii for *)
LDI R4,Loop ; [address of start of loop: the PRA *]

; # --------------------
Loop: 
    PRA R3 ; <- Loop starts here
    LDI R2,2 ; <- num to multiply by (2) (Resets this back from being 64)
    INC R0 ; <- increment the number of asteriks
    CMP R0,R1
    JLE R4 ; R4 holds address to jump to
    LDI R0,1 ; <- initial num of *s (Reset R0 back to 1)
    MUL R1,R2 ; (Increment R1)
    LDI R3, 10 ; (ascii for \n)
    PRA R3
    LDI R3,42 ; (ascii for *)
    LDI R2, 64 ; (Temporarily assign R2 to be 64, the absolute max num of *s we want on a line)
    CMP R1,R2 ; (See if desired num *s is <= than absolute max num *s)
    JLE R4
    HLT