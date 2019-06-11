#!/usr/bin/env python3
from typing import List, Dict
import common

def format_disassembly(addr: int, instruction: str) -> str:
    return '0x{:x}\t{}\n'.format(addr, instruction)


def disassemble(bytecode: str) -> str:
    result: str = ''
    for i in range(len(bytecode)):
        ins_byte = ord(bytecode[i])

        # any byte not defined is a nop
        if ins_byte not in common.bytecode_mapping:
            result += format_disassembly(i, 'nop')
            continue

        result += format_disassembly(i, common.bytecode_mapping[ins_byte])
    return result


def main():
    code: str = input('Code: ')
    print()
    result: str = disassemble(code)
    print(result)


if __name__ == "__main__":
    main()
