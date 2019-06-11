from typing import Dict, Iterable

bytecode_mapping: Dict[int, str] = {
    0x0a: 'nop',
    0x20: 'nop',
    0x41: 'add',
    0x42: 'hlt',
    0x43: 'jmp',
    0x44: 'pop',
    0x45: 'read',
    0x46: 'sclone',
    0x47: 'ipadd',
    0x48: 'sshift',
    0x49: 'pint',
    0x4a: 'cmp',
    0x4b: 'write',
    0x4d: 'mul',
    0x50: 'pchar',
    0x52: 'rjmp',
    0x53: 'sub',
    0x56: 'div',
    0x5a: 'ipcadd',
    0x61: 'p0',
    0x62: 'p1',
    0x63: 'p2',
    0x64: 'p3',
    0x65: 'p4',
    0x66: 'p5',
    0x67: 'p6',
    0x68: 'p7',
    0x69: 'p8',
    0x6a: 'p9',
}

push_ins: Iterable[int] = range(0x61, 0x6b)
# arithmetic_ins = [0x41, 0x4d, 0x53, 0x56]
# consumption_ins = [0x43, 0x44, 0x45]
# consumption_ins.extend(arithmetic_ins)

instruction_mapping: Dict[str, int] = {v: k for k, v in bytecode_mapping.items()}
