# LSCVM Tool

Tool for solving LSCVM challenges in CDDC 2019

## Info

Max stack size is `0x3ff` `1023`

Max Number of Cycles `0x2710` `10000`

Fgets reads `0x1000` `4096` chars of instructions

VM memory size is `0x3fff`

## Instruction Set

| Opcode (Hex) | Opcode (Char) | Assmebly | Comment |
|---|---|---|---|
| Default | NIL | nop | no operation, waste cycle |
| 0x0a | \n | nop | no operation, waste cycle |
| 0x20 | \s | nop | no operation, waste cycle |
| 0x41 | A | add | Pop 2 values from stack and push the addition |
| 0x42 | B | hlt | Stop executing code |
| 0x43 | C | jmp | Pop and jump to value |
| 0x44 | D | pop | Pop a value and do nothing |
| 0x45 | E | read | Pop addr and push val. `0` <= addr <= `0x3fff` |
| 0x46 | F | sclone | pop value n and (clone) push n+1 th previous stack value |
| 0x47 | G | ipadd | Pop value and add it to IP |
| 0x48 | H | sshift | pop value n and shift n+1 th previous stack value to the top of the stack |
| 0x49 | I | pint | Pop value and Print as int |
| 0x4a | J | cmp | 0 if equal, 1 if first pop is smaller else `0xffffffff`. `0` <= addr <= `0x3fff` |
| 0x4b | K | write | first pop is addr, 2nd pop is value to write |
| 0x4d | M | mul | Pop 2 values from stack and push the multiplication |
| 0x50 | P | pchar | Pops value from stack and print as char |
| 0x52 | R | rjmp | Jump to previous jump location, cant do twice in a row, because it consumes the previous jump location. |
| 0x53 | S | sub | subtract 1st pop from 2nd pop push result |
| 0x56 | V | div | Divide (floor) 2nd pop by 1st pop and push result |
| 0x5a | Z | ipcadd | conditional add to IP, if 2nd pop is 0, add 1st pop to IP |
| 0x61 | a | p0 | Push 0x00 to stack |
| 0x62 | b | p1 | Push 0x01 to stack |
| 0x63 | c | p2 | Push 0x02 to stack |
| 0x64 | d | p3 | Push 0x03 to stack |
| 0x65 | e | p4 | Push 0x04 to stack |
| 0x66 | f | p5 | Push 0x05 to stack |
| 0x67 | g | p6 | Push 0x06 to stack |
| 0x68 | h | p7 | Push 0x07 to stack |
| 0x69 | i | p8 | Push 0x08 to stack |
| 0x6a | j | p9 | Push 0x09 to stack |

## Sample codes
```
print welcome msg
cfMcfMhiMfAhiMfAhiMfAeiMaAeiMjAhhcMMdAgjcMMcAhhcMMhAhhcMMgAhhcMMbAdfgMMhAijMfAeiMaAgjcMMaAdfgMMhAeehMMfAeehMMeAeehMMcAhhcMMhAjjMfAeiMaAeehMMaAeehMMcAgjcMMdAhjMeAeiMaAhhcMMcAhhcMMdAhhcMMdAeehMMaAjjMcAeehMMeAhhcMMgAhhcMMfAhhcMMhAijMeAeiMiAijMfAjjMfAhjMeAjjMcAijMeAeiMaAgjcMMdAeehMMeAeiMaAhhcMMdAgjcMMbAgjcMMdAhhcMMbAgjcMMaAhhcMMdAjjMgAeiMaAhiMfAhiMfAhiMfAcfMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

print 'password: '
eiMaAhiMcAeiMaAhhcMMcAeehMMcAgjcMMdAeehMMhAeehMMdAeehMMdAdfgMMhAijMiAPPPPPPPPPPP

print ', Good Bye!\n'
cfMcfMeiMbAhhcMMdAefgMMbAhjMdAeiMaAhhcMMcAgjcMMdAgjcMMdAhjMiAeiMaAghMcAPPPPPPPPPPPPP

print '[-] Password mismatch'
cfMhhcMMgAhhcMMbAeehMMeAdfgMMhAgjcMMbAeehMMdAhhcMMhAgjcMMbAeiMaAhhcMMcAeehMMcAgjcMMdAeehMMhAeehMMdAeehMMdAdfgMMhAijMiAeiMaAdfgMMdAghMdAdfgMMbAPPPPPPPPPPPPPPPPPPPPPP

print 'Wrong ID'
cfMhhcMMcAhhcMMhAeiMaAhhcMMfAgjcMMcAgjcMMdAeehMMcAjjMgAeiMaAdfgMMdAghMdAdfgMMbAPPPPPPPPPPPPP

bbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbACbbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAPbbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAPB
```