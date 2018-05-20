import re
import struct
from disassembler.functions import *

def disasm(lists):
    e = 0
    text = []
    raw = ''
    positions = {}
    line = 0
    try:
        for instruction in lists:
            line = line + 1
            func = ops.get(int(instruction[0:6],2), 'error')
            #print(func,' ',line)
            if func == 'error':
                #is data
                text.append('    .word 0x' + hex(int(instruction,2))[2:].zfill(8).upper())
                continue
            ins, pos = func(instruction, positions, line)
            if pos == -2:
                # is data
                text.append('    .word 0x' + hex(int(instruction, 2))[2:].zfill(8).upper())
                continue
            if pos != -1:
                if positions.get(pos, '') == '':
                    positions[pos] = len(positions)
            text.append('    '+ins)
    except Exception as e_:
        return raw, e_
    keys = sorted(positions.keys())
    i = 0
    for index, pos in enumerate(keys):
        if pos+index-i > len(text) or pos+index-i < 0:
            i = i + 1
            continue
        text.insert(pos+index-i,'label_%d:' % positions[pos])
    for i in text:
        raw = raw + i + '\n'
    return raw, e

if __name__ == '__main__':
    fname = r'C:\Users\alan\Desktop\1.coe'
    try:
        with open(fname, 'r+') as f:
            f.read(62)
            txt = f.read()
            lists = txt.split(',')
            lists = [i.replace('\n', '') for i in lists]
            lists = [i.replace(';', '') for i in lists]
            lists = [bin(int(i, 16))[2:].zfill(32) for i in lists]
            text, e = disasm(lists)
            if e != 0:
                raise e
            print(text)
        #     txt = '00A62020'
        #     lists = txt.split(',')
        #     lists = [i.replace('\n', '') for i in lists]
        #     lists = [i.replace(';', '') for i in lists]
        #     lists = [bin(int(i, 16))[2:].zfill(32) for i in lists]
        #     text, e = disasm(lists)
        #     if e != 0:
        #         raise e
        #     print(text)
    except Exception as e:
        print(str(e) + '\n')