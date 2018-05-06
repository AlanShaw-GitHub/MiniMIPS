from assembler.First_scan import first_scan
from assembler.second_scan import second_scan
import re

def asm(text):
    result = ''
    text = text.split('\n')
    text = [re.sub(r'\t|\\n',' ',i) for i in text]
    symbol_table,line,e = first_scan(text)
    if line != -1:
        return result,line,e,1
    result,line,e = second_scan(text,symbol_table)
    if line != -1:
        return result,line,e,2
    return result,-1,Exception('None'),-1

if __name__ == '__main__':
    # bits = open(r'C:\Users\Alan Shaw\Desktop\2.txt', 'r+')
    # temp = asm(bits.read())[0]
    # i = 0
    # print(len(temp)/32)
    # while i < len(temp):
    #     print(hex(int((i+32)/32)) + '  ' + temp[i:i+32])
    #     i = i + 32
    # bits.close()
    print(hex(int(asm('add $a0, $a1, $a2')[0],2))[2:].zfill(8).upper())
