// Box.asm  --  Nand to Tetris I capstone, Part C
// K = 23
//   start row = 23        -> first word address = 16384 + 32*23 = 17120
//   height    = 20 rows
//   width     = 16 * ((23 mod 4) + 1) = 16 * 4 = 64 pixels = 4 words
// While any key is pressed the box is black; when released it is white.
//
// Variables:  color = -1 (black) or 0 (white)
//             addr  = first word of the current row
//             rows  = rows still to draw
//             cols  = words still to draw in this row
//             ptr   = address of the word being written

(MAIN)
    @KBD
    D=M
    @DRAW
    D;JNE           // a key is pressed -> draw black
    @color
    M=0             // no key -> white
    @FILL
    0;JMP

(DRAW)
    @color
    M=-1            // black = all 16 bits set

(FILL)
    @17120          // SCREEN + 32*23 (row 23, column 0)
    D=A
    @addr
    M=D
    @20             // 20 rows tall
    D=A
    @rows
    M=D

(ROWLOOP)
    @4              // 4 words = 64 pixels wide
    D=A
    @cols
    M=D
    @addr
    D=M
    @ptr
    M=D             // ptr = start of this row

(COLLOOP)
    @color
    D=M
    @ptr
    A=M
    M=D             // write one word
    @ptr
    M=M+1           // next word
    @cols
    M=M-1
    D=M
    @COLLOOP
    D;JGT           // more words in this row?

    @32             // move down one screen row (32 words)
    D=A
    @addr
    M=M+D
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT           // more rows?

    @MAIN           // start again (checks the keyboard again)
    0;JMP
