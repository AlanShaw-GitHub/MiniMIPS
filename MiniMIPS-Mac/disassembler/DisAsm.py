import re
import struct
from disassembler.functions import *

def disasm(lists):
    e = 0
    text = []
    raw = ''
    positions = {0:0}
    line = 0
    try:
        for instruction in lists:
            line = line + 1
            func = ops.get(int(instruction[0:6],2), 'error')
            if func == 'error':
                #is data
                text.append('    .word 0x' + hex(int(instruction,2))[2:].zfill(8).upper())
                continue
            ins, pos = func(instruction, len(positions), line)
            if pos == -2:
                # is data
                text.append('    .word 0x' + hex(int(instruction, 2))[2:].zfill(8).upper())
                continue
            if pos != -1:
                positions[pos] = len(positions)
            text.append('    '+ins)
    except Exception as e_:
        return raw, e_
    text.append('    j label_0')
    keys = sorted(positions.keys())
    for index, pos in enumerate(keys):
        if pos+index > len(text):
            e = Exception('ERROR : When executing the jump operation, the reference address out of range.')
            break
        text.insert(pos+index,'label_%d:' % positions[pos])
    for i in text:
        raw = raw + i + '\n'
    return raw, e

if __name__ == '__main__':
    fname = '/Users/alan/Desktop/1.coe'
    try:
        # with open(fname, 'r+') as f:
        #     f.read(62)
        #     txt = f.read()
        #     lists = txt.split(',')
        #     lists = [i.replace('\n', '') for i in lists]
        #     lists = [i.replace(';', '') for i in lists]
        #     lists = [bin(int(i, 16))[2:].zfill(32) for i in lists]
        #     text, e = disasm(lists)
        #     if e != 0:
        #         raise e
        #     print(text)
            txt = '00A62020'
            lists = txt.split(',')
            lists = [i.replace('\n', '') for i in lists]
            lists = [i.replace(';', '') for i in lists]
            lists = [bin(int(i, 16))[2:].zfill(32) for i in lists]
            text, e = disasm(lists)
            if e != 0:
                raise e
            print(text)
    except Exception as e:
        print(str(e) + '\n')