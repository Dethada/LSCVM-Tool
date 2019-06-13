#!/usr/bin/env python3
from typing import List, Dict
import argparse
import common


def push_generator(num: int) -> str:
    result = ''
    if num == 0:
        return 'a'
    for i in range(num):
        if i == 0:
            result += 'b'
        else:
            result += 'bA'
    return result


def print_str(string: str) -> str:
    result = ''
    for c in string:
        result += '{}P'.format(push_generator(ord(c)))
    return result


def get_labels(instructions: List[str]) -> Dict[str, int]:
    ins_len = 0
    labels = {}
    for ins in instructions:
        if ins:
            if ins.startswith('push'):
                num = int(ins[5:], 16)
                ins_len += len(push_generator(num))
            elif ins.startswith('print'):
                string = ins[6:]
                ins_len += len(print_str(string))
            elif ins.startswith('.label_'):
                labels[ins] = ins_len
            else:
                ins_len += 1
    return labels


def assemble(instructions: List[str], start: int = 0, stop: int = -1) -> str:
    result = ''
    labels = get_labels(instructions)
    if stop == -1:
        stop = len(instructions)
    # print(labels)
    for i in range(start, stop):
        ins = instructions[i]
        if ins:
            if ins.startswith('push'):
                num = int(ins[5:], 16)
                result += push_generator(num)
            elif ins.startswith('print'):
                string = ins[6:]
                result += print_str(string)
            elif ins.startswith('jmpl'):
                label = ins[5:]
                target_addr = labels[label]
                if target_addr < len(result):
                    result += '{}{}'.format(push_generator(target_addr),
                                            chr(common.instruction_mapping['jmp']))
                else:
                    result += '{}{}'.format(push_generator(target_addr),
                                            chr(common.instruction_mapping['ipadd']))
            else:
                try:
                    result += chr(common.instruction_mapping[ins])
                except KeyError:
                    pass
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='The file containing the assembly code of LSCVM', required=True)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        instructions: List[str] = f.readlines()

    result: str = assemble(instructions)
    print(result)


if __name__ == "__main__":
    main()
