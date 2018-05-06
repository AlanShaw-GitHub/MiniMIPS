import re
from assembler.functions import *

def process_data(text,line):
    occupy = 0
    value = ''
    if(re.search(r'\.asciiz',text)):
        pos = re.search(r'\.asciiz',text).span()[1]
        str = text[pos:len(text)].strip().replace('\"','')
        occupy = 4*(int(len(str)/4)+1)
        value = change_radix('str2bin',str)
    elif(re.search(r'\.ascii',text)):
        pos = re.search(r'\.ascii',text).span()[1]
        str = text[pos:len(text)].strip().replace('\"','')
        occupy = 4*(int(len(str)/4)+1)
        value = change_radix('str2bin',str)
    elif (re.search(r'\.byte', text)):
        pos = re.search(r'\.byte',text)[1]
        str = text[pos:len(text)].strip()
        str = str.split(',')
        str = [i.strip() for i in str]
        for i in str:
            value = value + change_radix('hex2bin',i,1)
        while (len(value) % 32 != 0):
            value = value + '00000000'
        occupy = int(len(value)/8)
    elif (re.search(r'\.half', text)):
        pos = re.search(r'\.half',text).span()[1]
        str = text[pos:len(text)].strip()
        str = str.split(',')
        str = [i.strip() for i in str]
        for i in str:
            value = value + change_radix('hex2bin',i,2)
        while (len(value) % 32 != 0):
            value = value + '00000000'*2
        occupy = int(len(value)/8)
    elif (re.search(r'\.word', text)):
        pos = re.search(r'\.word',text).span()[1]
        str = text[pos:len(text)].strip()
        str = str.split(',')
        str = [i.strip() for i in str]
        for i in str:
            value = value + change_radix('hex2bin',i,4)
        occupy = int(len(value)/8)
    elif (re.search(r'\.space', text)):
        pos = re.search(r'\.space', text).span()[1]
        str = text[pos:len(text)].strip()
        if(re.sub('[0-9]','',str) != ''):
            raise Exception('Line %d : ".space" must be followed by a number.'% line)
        number = int(str)
        if(number % 4 != 0):
            raise Exception('Line %d : Not aligned by 4.' % line)
        for i in range(number):value = value + '00000000'
        occupy = number
    else:
        raise Exception('Line %d : Can\'t resolve this label.'% line)
    return occupy,value

def process_text(text,line,dicts,position):
    pseudo = False
    param = text.split(',')
    op = ''
    if param[0] not in ['syscall','nop']:
        param = [i.strip() for i in param]
        param[0] = re.sub('[ ]+',' ',param[0])
        op ,param[0] = param[0].split(' ')
    else:
        op = param[0]
    func = functions.get(op,'error')
    if func == 'error':
        raise Exception('Line %d : Current operation not found.' % line)
    value = func(param,line,dicts,position)
    if len(value) != 32 and len(value) != 64:
        raise Exception('Line %d : Unexpected ERROR!(operation bin code length does not equal to 32' % line)
    if op in pseudo_func:
        pseudo = True
    return value,pseudo

def change_radix(flag,str,num = 1):
    if(flag == 'str2bin'):
        byte = ''
        for i in range(len(str)):
            temp = bin(ord(str[i])).replace('0b','')
            while len(temp) != 8:
                temp = '0' + temp
            byte = byte + temp
        while len(byte) % 32 != 0:
            byte = byte + '00000000'
        return byte
    if(flag == 'hex2bin'):
        temp = bin(int(str,16)).replace('0b','')
        while len(temp) != num*8:
            temp = '0' + temp
        return temp
