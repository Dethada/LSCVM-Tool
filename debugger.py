#!/usr/bin/env python3
from typing import List, Dict
import argparse
import re
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
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
    return '0x{:x}\t{}'.format(addr, instruction)


# def push(stack, value):
#     if len(stack) < 0x400:
#         stack.append(value)
#     else:
#         print('\t[-] Stack overflow')


def print_help() -> str:
    msg = '''
Available commands:
r\t- rerun the code from the start
c\t- continue
b\t- set breakpoint(s); Example `b 0x14 0x20`
sb\t- show breakpoints
d\t- delete breakpoint(s) by index; Example `d 1 3 9`
dall\t- delete all breakpoints
ss\t- show stack
x/\t- Examine memory, possible format specifiers are d/x/s for decimal, hex and string; Example print the values at address 0x40 to 0x54 (0x40 + 20) as hex `x/20x 0x40`
ni\t- run next instruction
q\t- quit
'''
    print(msg)


def disassemble_byte(b: str) -> str:
    ins_byte = ord(b)

    # any byte not defined is a nop
    if ins_byte not in common.bytecode_mapping:
        return 'nop'

    return common.bytecode_mapping[ins_byte]

def format_instructions(bytecode, ip) -> str:
    output = ''
    start = ip - 3
    while start < 0:
        start += 1
    end = ip + 4
    if end > len(bytecode):
        end = len(bytecode)
    for i in range(start, end):
        if i == ip:
            output += '-> 0x{:x} {}\n'.format(i, disassemble_byte(bytecode[i]))
        else:
            output += '   0x{:x} {}\n'.format(i, disassemble_byte(bytecode[i]))
    return output

def format_stack(stack) -> str:
    output = ''
    for i, value in enumerate(stack):
        output += '{}: {}\n'.format(i, value)
    return output

def format_memory(memory, size, print_type, addr) -> str:
    output = ''

    if addr not in range(0x4000) or addr+size-1 not in range(0x4000):
        return 'Invalid memory access\n'

    for i in range(addr, addr+size):
        if print_type == 'd':
            output += '0x{:x}: {}\n'.format(i, memory[i])
        elif print_type == 's':
            output += chr(memory[i])
        elif print_type == 'x':
            output += '0x{:x}: 0x{:x}\n'.format(i, memory[i])
        else:
            return 'Invalid format specified\n'
    return output

def execute(bytecode: str, session):
    output: str = ''
    last_jump: int = -1
    stack: List[int] = []
    memory: List[int] = [0] * 0x4000
    bytecode_len: int = len(bytecode)
    cycles: int = 0
    ip: int = 0
    breakpoints: List[int] = []
    break_next_ins = False
    while ip < bytecode_len:
        if ip == 0 or ip in breakpoints or break_next_ins:
            if break_next_ins:
                break_next_ins = False
            print('Instructions:\n{}\nStack: {}\n'.format(format_instructions(bytecode, ip), stack, memory))
            while True:
                try:
                    command = session.prompt('ldb ➜ ')
                except KeyboardInterrupt:
                    continue  # Ctrl-C pressed. Try again.
                except EOFError:
                    return  # Ctrl-D pressed, quit
                if command == 'r':
                    output = ''
                    last_jump = -1
                    stack = []
                    memory = [0] * 0x4000
                    cycles = 0
                    ip = 0
                elif command == 'c':
                    break
                elif command.startswith('b '):
                    try:
                        breakpoints.extend(
                            map(lambda x: int(x, 16), command[2:].split(' ')))
                    except ValueError:
                        print('Invalid breakpoint(s)')
                    continue
                elif command == 'sb':
                    for i, bp in enumerate(breakpoints):
                        print('Index: {} Address: {}'.format(i, bp))
                    continue
                elif command == 'ss':
                    print(format_stack(stack))
                    continue
                elif command.startswith('x/'):
                    try:
                        cap = re.search(r"x/(\d+)([sxd])\s+(0x[\dabcdef]+)", command)
                        size = int(cap.group(1))
                        print_type = cap.group(2)
                        addr = int(cap.group(3), 16)
                        print(format_memory(memory, size, print_type, addr))
                    except Exception:
                        print('Invalid arguments')
                        continue
                elif command == 'ni':
                    break_next_ins = True
                    break
                elif command.startswith('d '):
                    for i in map(lambda x: int(x), command[2:].split(' ')):
                        try:
                            del breakpoints[i]
                        except IndexError:
                            print('No breakpoint {}'.format(i))
                        else:
                            print('Deleted breakpoint {}'.format(i))
                    continue
                elif command == 'dall':
                    breakpoints = []
                    print('Breakpoints cleared')
                    continue
                elif command == 'help' or command == 'h':
                    print_help()
                    continue
                elif command == 'q':
                    return
                else:
                    print('Unknown command.')
                    print_help()
                    continue

        cycles += 1
        if cycles > 10000:
            print('[-] Too many cycles')
            break
        ins_byte = ord(bytecode[ip])

        if ins_byte in common.push_ins:
            stack.append(ins_byte - 0x61)

        try:
            if ins_byte == 0x41:
                add(stack)
            elif ins_byte == 0x42:
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

        if ip > bytecode_len:
            print('[-] out of code bounds')
            break
        ip += 1

    print('\nOutput:\n{}'.format(output))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='The file containing the code to execute', required=True)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        code: str = f.read()

    history = InMemoryHistory()
    session = PromptSession(
        history=history, auto_suggest=AutoSuggestFromHistory(), enable_history_search=True)

    print('''
  _     ____   ______     ____  __   ____  _           
 | |   / ___| / ___\ \   / /  \/  | |  _ \| |__   __ _ 
 | |   \___ \| |    \ \ / /| |\/| | | | | | '_ \ / _` |
 | |___ ___) | |___  \ V / | |  | | | |_| | |_) | (_| |
 |_____|____/ \____|  \_/  |_|  |_| |____/|_.__/ \__, |
                                                 |___/               
''')
    execute(code, session)



if __name__ == "__main__":
    main()
