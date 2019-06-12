#!/usr/bin/env python3
from typing import List, Dict
import argparse
import common


def add(stack: List[int]):
    val1: int = stack.pop()
    val2: int = stack.pop()
    stack.append(val1 + val2)


def mul(stack: List[int]):
    val1: int = stack.pop()
    val2: int = stack.pop()
    stack.append(val1 * val2)


def sub(stack: List[int]):
    val1: int = stack.pop()
    val2: int = stack.pop()
    stack.append(val2 - val1)


def div(stack: List[int]):
    val1: int = stack.pop()
    val2: int = stack.pop()
    stack.append(val2 // val1)


def read(stack: List[int], memory: List[int]):
    addr: int = stack.pop()
    if addr >= 0 and addr <= 0x3fff:
        stack.append(memory[addr])
    else:
        print('\t[-] memory read access violation {}'.format(addr))


def sclone(stack: List[int]):
    n: int = stack.pop() + 1
    stack.append(stack[-n])
    # [-] out of stack bounds %d


def sshift(stack: List[int]):
    n: int = stack.pop() + 1
    stack.append(stack.pop(-n))
    # [-] out of stack %d


def pint(stack: List[int]) -> str:
    return str(stack.pop())


def cmp(stack: List[int]):
    val1: int = stack.pop()
    val2: int = stack.pop()
    if val1 == val2:
        stack.append(0)
    elif val1 < val2:
        stack.append(1)
    else:
        stack.append(-1)


def write(stack: List[int], memory: List[int]):
    addr: int = stack.pop()
    val: int = stack.pop()
    if addr >= 0 and addr <= 0x3fff:
        memory[addr] = val
    else:
        print('\t[-] memory write access violation {}'.format(addr))


def pchar(stack: List[int]) -> str:
    return chr(stack.pop())


def format_debug(addr: int, opcode: str) -> str:
    try:
        instruction: str = common.bytecode_mapping[opcode]
    except KeyError:
        instruction: str = 'nop'
    return '@{}\t{}'.format(addr, instruction)


# def push(stack, value):
#     if len(stack) < 0x400:
#         stack.append(value)
#     else:
#         print('\t[-] Stack overflow')

def execute(bytecode: str, verbose: bool = False):
    output: str = ''
    last_jump: int = -1
    stack: List[int] = []
    memory: List[int] = [0] * 0x4000
    bytecode_len: int = len(bytecode)
    cycles: int = 0
    ip: int = 0
    while ip < bytecode_len:
        cycles += 1
        if cycles > 10000:
            print('[-] Too many cycles')
            break
        ins_byte = ord(bytecode[ip])
        if verbose:
            print(format_debug(ip, ins_byte), end='')

        if ins_byte in common.push_ins:
            stack.append(ins_byte - 0x61)

        try:
            if ins_byte == 0x41:
                add(stack)
            elif ins_byte == 0x42:
                if verbose:
                    print(format_debug(ip, ins_byte), end='')
                break
            elif ins_byte == 0x43:
                ip = stack.pop() - 1
                # print('jumped to {}', ip)
                last_jump = ip + 1
            elif ins_byte == 0x44:
                stack.pop()
            elif ins_byte == 0x45:
                read(stack, memory)
            elif ins_byte == 0x46:
                sclone(stack)
            elif ins_byte == 0x47:
                ip += stack.pop()
            elif ins_byte == 0x48:
                sshift(stack)
            elif ins_byte == 0x49:
                output += pint(stack)
            elif ins_byte == 0x4a:
                cmp(stack)
            elif ins_byte == 0x4b:
                write(stack, memory)
            elif ins_byte == 0x4d:
                mul(stack)
            elif ins_byte == 0x50:
                output += pchar(stack)
            elif ins_byte == 0x52:
                if last_jump == -1:
                    print('\t[-] Empty')
                    break
                else:
                    ip = last_jump - 1
                    last_jump = -1
            elif ins_byte == 0x53:
                sub(stack)
            elif ins_byte == 0x56:
                div(stack)
            elif ins_byte == 0x5a:
                val1: int = stack.pop()
                cond = stack.pop()
                if cond == 0:
                    ip += val1
        except IndexError:
            print('\t[-] Stack underflow')
            break

        if verbose:
            print('\t{}'.format(stack))

        if ip > bytecode_len:
            print('[-] out of code bounds')
            break
        ip += 1

    print('\nOutput:\n{}'.format(output))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='The file containing the code to execute', required=True)
    parser.add_argument('-v', '--verbose', dest='verbose',
                        action='store_true', help='Show debugging information')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        code: str = f.read()

    execute(code, verbose=args.verbose)


if __name__ == "__main__":
    main()
