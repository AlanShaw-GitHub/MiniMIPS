from utils.register import *
import re

def asm_abs(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_add(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error' :
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0,length=5) \
           + num2bin(32,length=6)

def asm_addu(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(33, length=6)

def asm_addi(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(8, length=6) + rs + rt + num2bin(int(param[2]),length=16)

def asm_addiu(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(9, length=6) + rs + rt + num2bin(int(param[2]), length=16)

def asm_and(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(36, length=6)
def asm_andi(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(12, length=6) + rs + rt + num2bin(int(param[2]), length=16)

def asm_clo(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(28, length=6) + rs + num2bin(0,length=5) + rd + \
           num2bin(0, length=5) +num2bin(33, length=6)

def asm_clz(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(28, length=6) + rs + num2bin(0, length=5) + rd + \
           num2bin(0, length=5) + num2bin(32, length=6)

def asm_div(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(26, length=6)

def asm_divu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(27, length=6)

def asm_mult(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(24, length=6)

def asm_multu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(25, length=6)

def asm_mul(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(28, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(2, length=6)

def asm_mulo(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_mulou(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_madd(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(28, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(0, length=6)

def asm_maddu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(28, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(1, length=6)

def asm_msub(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(28, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(4, length=6)

def asm_neg(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_negu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_nor(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(39, length=6)

def asm_not(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_or(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(37, length=6)

def asm_ori(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(13, length=6) + rs + rt + num2bin(int(param[2]), length=16)

def asm_rem(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_remu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sll(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rd == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if(re.sub('[0-9]+','',param[2])):
        raise Exception('Line %d : sll->shamt can only be a number.' % line)
    return num2bin(0, length=6) + num2bin(0,length=5) + rt + rd + \
           num2bin(int(param[2]), length=5) + num2bin(0, length=6)

def asm_sllv(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    rs = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(4, length=6)

def asm_sra(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rd == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[2])):
        raise Exception('Line %d : srl->shamt can only be a number.' % line)
    return num2bin(0, length=6) + num2bin(0, length=5) + rt + rd + \
           num2bin(int(param[2]), length=5) + num2bin(3, length=6)


def asm_srav(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    rs = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(7, length=6)

def asm_srl(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rd == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[2])):
        raise Exception('Line %d : srl->shamt can only be a number.' % line)
    return num2bin(0, length=6) + num2bin(0, length=5) + rt + rd + \
           num2bin(int(param[2]), length=5) + num2bin(2, length=6)


def asm_srlv(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    rs = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(6, length=6)

def asm_rol(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ror(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sub(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(34, length=6)

def asm_subu(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(35, length=6)

def asm_xor(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(38, length=6)

def asm_xori(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[2])):
        raise Exception('Line %d : xori->imm can only be a number.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(int(param[2]), length=16)

def asm_lui(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    if rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[1])):
        raise Exception('Line %d : lui->imm can only be a number.' % line)
    return num2bin(15, length=6) + num2bin(0, length=5) + rt + \
           num2bin(int(param[1]), length=16)

def asm_li(param,line,symbol_table,position):
    return asm_lui([param[0], str(0)], line, symbol_table, position) + \
           asm_ori([param[0], param[0], param[1]], line, symbol_table, position)

def asm_slt(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(42, length=6)

def asm_sltu(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + num2bin(0, length=5) \
           + num2bin(43, length=6)

def asm_slti(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[2])):
        raise Exception('Line %d : slti->imm can only be a number.' % line)
    return num2bin(10, length=6) + rs + rt + \
           num2bin(int(param[2]), length=16)

def asm_sltiu(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[2])):
        raise Exception('Line %d : sll->shamt can only be a number.' % line)
    return num2bin(11, length=6) + rs + rt + \
           num2bin(int(param[2]), length=16)

def asm_seq(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sge(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sgeu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sgt(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sgtu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sle(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sleu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sne(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_b(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bclf(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bclt(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_beq(param,line,symbol_table,position):
    result = num2bin(4,length=6)
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or rt == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset/4),length=16)
    result = result + rs + rt + offset
    return result

def asm_bgez(param,line,symbol_table,position):
    result = num2bin(1, length=6)
    rs = register.get(param[0], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + num2bin(1, length=5) + offset
    return result

def asm_bgezal(param,line,symbol_table,position):
    result = num2bin(1, length=6)
    rs = register.get(param[0], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + num2bin(17, length=5) + offset
    return result

def asm_bgtz(param,line,symbol_table,position):
    result = num2bin(7, length=6)
    rs = register.get(param[0], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + num2bin(0, length=5) + offset
    return result
def asm_blez(param,line,symbol_table,position):
    result = num2bin(6, length=6)
    rs = register.get(param[0], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + num2bin(0, length=5) + offset
    return result
def asm_bltzal(param,line,symbol_table,position):
    result = num2bin(1, length=6)
    rs = register.get(param[0], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + num2bin(16, length=5) + offset
    return result

def asm_bltz(param,line,symbol_table,position):
    result = num2bin(1, length=6)
    rs = register.get(param[0], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + num2bin(0, length=5) + offset
    return result

def asm_bne(param,line,symbol_table,position):
    result = num2bin(5, length=6)
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if not re.sub('[0-9]+', '', param[2]):
        label = int(param[2],10)
    else:
        label = symbol_table.get(param[2],'error')
    if rs == 'error' or rt == 'error' or label == 'error':
        raise Exception('Line %d : No such register or label.' % line)
    offset = label - (position + 4)
    offset = num2bin(int(offset / 4), 16)
    result = result + rs + rt + offset
    return result

def asm_beqz(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bge(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bgeu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bgt(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bgtu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ble(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bleu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_blt(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bltu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_bnez(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_j(param,line,symbol_table,position):
    result = num2bin(2,length=6)
    if(re.sub(r'[0-9]+','',param[0]) != ''):
        place = symbol_table.get(param[0],'error')
        if(place == 'error'):
            raise Exception('Line %d : No such symbol.' % line)
        return result + num2bin(int(place/4),26)
    else:
        return result + num2bin(int(param[0]),26)

def asm_jal(param,line,symbol_table,position):
    result = num2bin(3,length=6)
    if (re.sub(r'[0-9]+', '', param[0]) != ''):
        place = symbol_table.get(param[0], 'error')
        if (place == 'error'):
            raise Exception('Line %d : No such symbol.' % line)
        return result + num2bin(int(place / 4), 26)
    else:
        return result + num2bin(int(param[0]), 26)

def asm_jalr(param,line,symbol_table,position):
    result = num2bin(0,length=6)
    rs = register.get(param[0],'error')
    rd = register.get(param[1],'error')
    if rs == 'error' or rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = rs + '00000' + rd + '00000' + num2bin(9,length=6)
    return result

def asm_jr(param,line,symbol_table,position):
    result = '000000'
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + '00000'*3 + num2bin(8,length=6)

def asm_teq(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(52, length=6)

def asm_teqi(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error' :
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[1])):
        raise Exception('Line %d : teqi->imm can only be a number.' % line)
    return num2bin(1, length=6) + rs + \
           num2bin(12, length=5) + num2bin(int(param[1]), length=16)

def asm_tge(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(48, length=6)

def asm_tgeu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(49, length=6)

def asm_tgei(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[1])):
        raise Exception('Line %d : tgei->imm can only be a number.' % line)
    return num2bin(1, length=6) + rs + \
           num2bin(8, length=5) + num2bin(int(param[1]), length=16)

def asm_tgeiu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[1])):
        raise Exception('Line %d : tgei->imm can only be a number.' % line)
    return num2bin(1, length=6) + rs + \
           num2bin(9, length=5) + num2bin(int(param[1]), length=16)

def asm_tlt(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(50, length=6)

def asm_tltu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + \
           num2bin(0, length=10) + num2bin(51, length=6)

def asm_tlti(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[1])):
        raise Exception('Line %d : tlti->imm can only be a number.' % line)
    return num2bin(1, length=6) + rs + \
           num2bin(10, length=5) + num2bin(int(param[1]), length=16)

def asm_tltiu(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    if (re.sub('[0-9]+', '', param[1])):
        raise Exception('Line %d : tltiu->imm can only be a number.' % line)
    return num2bin(1, length=6) + rs + \
           num2bin(11, length=5) + num2bin(int(param[1]), length=16)

def asm_la(param,line,symbol_table,position):
    imm = symbol_table.get(param[1],'error')
    if imm == 'error':
        raise Exception('Line %d : No such label.' % line)
    return asm_lui([param[0],str(0)],line,symbol_table,position) + \
           asm_ori([param[0],param[0],str(imm)],line,symbol_table,position)

def asm_lb(param,line,symbol_table,position):
    result = num2bin(32, length=6)
    rt = register.get(param[0], 'error')
    if(re.sub(r'[0-9]+\(\$[a-z][0-9]\)','',param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(',param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos+2:len(param[1])-1]
    rs = register.get('$'+reg,'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset),length=16)
    return result

def asm_lbu(param,line,symbol_table,position):
    result = num2bin(36, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_lh(param,line,symbol_table,position):
    result = num2bin(33, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_lhu(param,line,symbol_table,position):
    result = num2bin(37, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_lw(param,line,symbol_table,position):
    result = num2bin(35, length=6)
    print(param)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_lwcl(param,line,symbol_table,position):
    result = num2bin(49, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_lwl(param,line,symbol_table,position):
    result = num2bin(34, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_lwr(param,line,symbol_table,position):
    result = num2bin(38, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_ld(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ulh(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ulhu(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ulw(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ll(param,line,symbol_table,position):
    result = num2bin(48, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_sb(param,line,symbol_table,position):
    result = num2bin(40, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_sh(param,line,symbol_table,position):
    result = num2bin(41, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_sw(param,line,symbol_table,position):
    result = num2bin(43, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_swcl(param,line,symbol_table,position):
    result = num2bin(49, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_sdcl(param,line,symbol_table,position):
    result = num2bin(61, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_swl(param,line,symbol_table,position):
    result = num2bin(42, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_swr(param,line,symbol_table,position):
    result = num2bin(46, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_sd(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_ush(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_usw(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_sc(param,line,symbol_table,position):
    result = num2bin(56, length=6)
    rt = register.get(param[0], 'error')
    if (re.sub(r'[0-9]+\(\$[a-z][0-9]\)', '', param[1])):
        raise Exception('Line %d : Unsupported format for operation \'lb\'' % line)
    pos = re.search(r'\(', param[1]).span()[0]
    offset = param[1][0:pos]
    reg = param[1][pos + 2:len(param[1]) - 1]
    rs = register.get('$' + reg, 'error')
    if rt == 'error' or rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    result = result + rs + rt + num2bin(int(offset), length=16)
    return result

def asm_move(param,line,symbol_table,position):
    return asm_add([param[0],param[1],'$zero'],line,symbol_table,position)
def asm_mfhi(param,line,symbol_table,position):
    rd = register.get(param[0],'error')
    if rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0,length=6) + num2bin(0,length=10) + rd + \
            num2bin(0,length=5) + num2bin(16,length=6)

def asm_mflo(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    if rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + num2bin(0, length=10) + rd + \
           num2bin(0, length=5) + num2bin(18, length=6)

def asm_mthi(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + \
           num2bin(0, length=15) + num2bin(17, length=6)

def asm_mtlo(param,line,symbol_table,position):
    rs = register.get(param[0], 'error')
    if rs == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + \
           num2bin(0, length=15) + num2bin(19, length=6)

def asm_mfc0(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    rd = register.get(param[1], 'error')
    if rt == 'error' or rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(16, length=6) + num2bin(0, length=5) + rt + rd +\
           num2bin(0, length=11)

def asm_mfcl(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    fs = register.get(param[1], 'error')
    if rt == 'error' or fs == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(17, length=6) + num2bin(0, length=5) + rt + fs + \
           num2bin(0, length=11)

def asm_mtc0(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rt = register.get(param[1], 'error')
    if rt == 'error' or rd == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(16, length=6) + num2bin(4, length=5) + rt + rd + \
           num2bin(0, length=11)

def asm_mtc1(param,line,symbol_table,position):
    rt = register.get(param[0], 'error')
    fs = register.get(param[1], 'error')
    if fs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(17, length=6) + num2bin(4, length=5) + rt + fs + \
           num2bin(0, length=11)

def asm_movn(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + \
           num2bin(11, length=11)

def asm_movz(param,line,symbol_table,position):
    rd = register.get(param[0], 'error')
    rs = register.get(param[1], 'error')
    rt = register.get(param[2], 'error')
    if rd == 'error' or rs == 'error' or rt == 'error':
        raise Exception('Line %d : No such register.' % line)
    return num2bin(0, length=6) + rs + rt + rd + \
           num2bin(10, length=11)

def asm_movf(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_movt(param,line,symbol_table,position):
    raise Exception('Line %d : Current opreation not supported.'% line)
def asm_eret(param,line,symbol_table,position):
    return num2bin(16,length=6) + num2bin(1,length=1) + num2bin(1,length=19) +\
            num2bin(24,length=6)

def asm_syscall(param,line,symbol_table,position):
    return num2bin(12,length=32)
def asm_break(param,line,symbol_table,position):
    if(re.sub('[0-9]+','',param[0])):
        raise Exception('Line %d : break operation can only accept a number .' % line)
    return '000000' + num2bin(int(param[0]),length=20) + num2bin(13,length=6)
def asm_nop(param,line,symbol_table,position):
    return num2bin(0,length=32)


def num2bin(num,length):
    if(num >= 0):
        temp = bin(num).replace('0b','')
        while(len(temp) < length):
            temp = '0' + temp
        return temp
    else:
        num = -num+1
        temp = bin(num).replace('0b','')
        result = ''
        for i in range(len(temp)):
            if temp[i] == '0':
                result = result + '1'
            else:
                result = result + '0'
        while len(result) < length - 1:
            result = '0' + result
        result = '1' + result
        return result


functions = {'abs': asm_abs,
 'add': asm_add,
 'addi': asm_addi,
 'addiu': asm_addiu,
 'addu': asm_addu,
 'and': asm_and,
 'andi': asm_andi,
 'b': asm_b,
 'bclf': asm_bclf,
 'bclt': asm_bclt,
 'beq': asm_beq,
 'beqz': asm_beqz,
 'bge': asm_bge,
 'bgeu': asm_bgeu,
 'bgez': asm_bgez,
 'bgezal': asm_bgezal,
 'bgt': asm_bgt,
 'bgtu': asm_bgtu,
 'bgtz': asm_bgtz,
 'ble': asm_ble,
 'bleu': asm_bleu,
 'blez': asm_blez,
 'blt': asm_blt,
 'bltu': asm_bltu,
 'bltz': asm_bltz,
 'bltzal': asm_bltzal,
 'bne': asm_bne,
 'bnez': asm_bnez,
 'clo': asm_clo,
 'clz': asm_clz,
 'div': asm_div,
 'divu': asm_divu,
 'eret': asm_eret,
 'j': asm_j,
 'jal': asm_jal,
 'jalr': asm_jalr,
 'jr': asm_jr,
 'la': asm_la,
 'lb': asm_lb,
 'lbu': asm_lbu,
 'ld': asm_ld,
 'lh': asm_lh,
 'lhu': asm_lhu,
 'li': asm_li,
 'll': asm_ll,
 'lui': asm_lui,
 'lw': asm_lw,
 'lwcl': asm_lwcl,
 'lwl': asm_lwl,
 'lwr': asm_lwr,
 'madd': asm_madd,
 'maddu': asm_maddu,
 'mfc0': asm_mfc0,
 'mfcl': asm_mfcl,
 'mfhi': asm_mfhi,
 'mflo': asm_mflo,
 'move': asm_move,
 'movf': asm_movf,
 'movn': asm_movn,
 'movt': asm_movt,
 'movz': asm_movz,
 'msub': asm_msub,
 'mtc0': asm_mtc0,
 'mtc1': asm_mtc1,
 'mthi': asm_mthi,
 'mtlo': asm_mtlo,
 'mul': asm_mul,
 'mulo': asm_mulo,
 'mulou': asm_mulou,
 'mult': asm_mult,
 'multu': asm_multu,
 'neg': asm_neg,
 'negu': asm_negu,
 'nop': asm_nop,
 'nor': asm_nor,
 'not': asm_not,
 'or': asm_or,
 'ori': asm_ori,
 'rem': asm_rem,
 'remu': asm_remu,
 'rol': asm_rol,
 'ror': asm_ror,
 'sb': asm_sb,
 'sc': asm_sc,
 'sd': asm_sd,
 'sdcl': asm_sdcl,
 'seq': asm_seq,
 'sge': asm_sge,
 'sgeu': asm_sgeu,
 'sgt': asm_sgt,
 'sgtu': asm_sgtu,
 'sh': asm_sh,
 'sle': asm_sle,
 'sleu': asm_sleu,
 'sll': asm_sll,
 'sllv': asm_sllv,
 'slt': asm_slt,
 'slti': asm_slti,
 'sltiu': asm_sltiu,
 'sltu': asm_sltu,
 'sne': asm_sne,
 'sra': asm_sra,
 'srav': asm_srav,
 'srl': asm_srl,
 'srlv': asm_srlv,
 'sub': asm_sub,
 'subu': asm_subu,
 'sw': asm_sw,
 'swcl': asm_swcl,
 'swl': asm_swl,
 'swr': asm_swr,
 'syscall': asm_syscall,
 'teq': asm_teq,
 'teqi': asm_teqi,
 'tge': asm_tge,
 'tgei': asm_tgei,
 'tgeiu': asm_tgeiu,
 'tgeu': asm_tgeu,
 'tlt': asm_tlt,
 'tlti': asm_tlti,
 'tltiu': asm_tltiu,
 'tltu': asm_tltu,
 'ulh': asm_ulh,
 'ulhu': asm_ulhu,
 'ulw': asm_ulw,
 'ush': asm_ush,
 'usw': asm_usw,
 'xor': asm_xor,
 'xori': asm_xori,
 'break': asm_break}


pseudo_func = ['li','la']