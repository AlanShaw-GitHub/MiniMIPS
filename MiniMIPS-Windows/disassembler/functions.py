import re
from utils.register import reverse_register

def disasm_ops00(instruction, pos, line):
    func = ops00.get(int(instruction[26:32], 2), 'error')
    if func == 'error':
        return '', -2
    return func(instruction, pos, line)

def disasm_ops01(instruction, pos, line):
    func = ops01.get(int(instruction[26:32], 2), 'error')
    if func == 'error':
        return '', -2
    return func(instruction, pos, line)

def disasm_j(instruction, pos, line):
    ins = 'j ' + 'label_%d' % pos
    return ins, int(instruction[6:32],2)

def disasm_jal(instruction, pos, line):
    ins = 'jal ' + 'label_%d' % pos
    return ins, int(instruction[6:32], 2)

def disasm_beq(instruction, pos, line):
    ins = 'beq ' + reverse_register.get(int(instruction[6:11],2),'error')+', '\
          + reverse_register.get(int(instruction[11:16],2),'error')+', ' + 'label_%d' % pos
    if re.search('error',ins):
        raise Exception('Line %d : No such register.' % line)
    print(line + int(int_comp(instruction[16:32]),10))
    return ins, line + int(int_comp(instruction[16:32]),10)

def disasm_bne(instruction, pos, line):
    return 'bne'+disasm_beq(instruction, pos, line)[0][3:], disasm_beq(instruction, pos, line)[1]

def disasm_blez(instruction, pos, line):
    ins = 'blez ' + reverse_register.get(int(instruction[6:11], 2), 'error') \
          + ', ' + 'label_%d' % pos
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, line + int(int_comp(instruction[16:32]),10)

def disasm_bgtz(instruction, pos, line):
    return 'bgtz'+disasm_blez(instruction, pos, line)[0][4:], disasm_blez(instruction, pos, line)[1]

def disasm_addi(instruction, pos, line):
    ins = 'addi ' + reverse_register.get(int(instruction[6:11],2),'error')+', '\
          + reverse_register.get(int(instruction[11:16],2),'error')+', ' + int_comp(instruction[16:32])
    if re.search('error',ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_addiu(instruction, pos, line):
    ins = 'addiu ' + reverse_register.get(int(instruction[6:11], 2), 'error') + ', ' \
          + reverse_register.get(int(instruction[11:16], 2), 'error') + ', ' + str(int(instruction[16:32]))
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_slti(instruction, pos, line):
    return 'slti'+disasm_addi(instruction, pos, line)[0][4:], disasm_addi(instruction, pos, line)[1]

def disasm_sltiu(instruction, pos, line):
    return 'sltiu'+disasm_addiu(instruction, pos, line)[0][5:], disasm_addiu(instruction, pos, line)[1]

def disasm_andi(instruction, pos, line):
    return 'andi'+disasm_addi(instruction, pos, line)[0][4:], disasm_addi(instruction, pos, line)[1]

def disasm_ori(instruction, pos, line):
    return 'ori'+disasm_addi(instruction, pos, line)[0][4:], disasm_addi(instruction, pos, line)[1]

def disasm_xori(instruction, pos, line):
    return 'xori'+disasm_addi(instruction, pos, line)[0][4:], disasm_addi(instruction, pos, line)[1]

def disasm_lui(instruction, pos, line):
    ins = 'lui ' + reverse_register.get(int(instruction[11:16], 2), 'error') \
          + ', ' + int_comp(instruction[16:32])
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_ops16(instruction, pos, line):
    func = ops16.get(int(instruction[26:32], 2), 'error')
    if func == 'error':
        return '', -2
    return func(instruction, pos, line)

def disasm_ops17(instruction, pos, line):
    func = ops17.get(int(instruction[26:32], 2), 'error')
    if func == 'error':
        return '', -2
    return func(instruction, pos, line)

def disasm_ops18(instruction, pos, line):
    func = ops18.get(int(instruction[26:32], 2), 'error')
    if func == 'error':
        return '', -2
    return func(instruction, pos, line)

def disasm_beql(instruction, pos, line):
    return 'beql'+disasm_beq(instruction, pos, line)[0][3:], disasm_beq(instruction, pos, line)[1]

def disasm_bnel(instruction, pos, line):
    return 'bnel'+disasm_beq(instruction, pos, line)[0][3:], disasm_beq(instruction, pos, line)[1]

def disasm_blezl(instruction, pos, line):
    return 'blezl'+disasm_blez(instruction, pos, line)[0][4:], disasm_blez(instruction, pos, line)[1]

def disasm_bgtzl(instruction, pos, line):
    return 'bgtz'+disasm_blez(instruction, pos, line)[0][4:], disasm_blez(instruction, pos, line)[1]

def disasm_ops28(instruction, pos, line):
    func = ops28.get(int(instruction[26:32], 2), 'error')
    if func == 'error':
        return '', -2
    return func(instruction, pos, line)
def disasm_lb(instruction, pos, line):
    ins = 'lb ' + reverse_register.get(int(instruction[11:16], 2), 'error') + ', '\
            + int_comp(instruction[16:32])+'('+ reverse_register.get(int(instruction[6:11], 2), 'error') + ')'
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_lh(instruction, pos, line):
    return 'lh'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lwl(instruction, pos, line):
    return 'lwl'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lw(instruction, pos, line):
    return 'lw'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lbu(instruction, pos, line):
    return 'lbu'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lhu(instruction, pos, line):
    return 'lhu'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lwr(instruction, pos, line):
    return 'lw'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sb(instruction, pos, line):
    return 'sb'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sh(instruction, pos, line):
    return 'sh'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_swl(instruction, pos, line):
    return 'swl'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sw(instruction, pos, line):
    return 'sw'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_swr(instruction, pos, line):
    return 'swr'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_cache(instruction, pos, line):
    return 'cache'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_ll(instruction, pos, line):
    return 'll'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lwc1(instruction, pos, line):
    return 'lwc1'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_lwc2(instruction, pos, line):
    return 'lwc2'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_pref(instruction, pos, line):
    return 'pref'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_ldc1(instruction, pos, line):
    return 'ldc1'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_ldc2(instruction, pos, line):
    return 'ldc2'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sc(instruction, pos, line):
    return 'sc'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_swc1(instruction, pos, line):
    return 'swc1'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_swc2(instruction, pos, line):
    return 'swc2'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sdc1(instruction, pos, line):
    return 'sdc1'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sdc2(instruction, pos, line):
    return 'sdc2'+disasm_lb(instruction, pos, line)[0][2:], disasm_lb(instruction, pos, line)[1]

def disasm_sll(instruction, pos, line):
    ins = 'sll ' + reverse_register.get(int(instruction[16:21], 2), 'error') + ', ' \
          + reverse_register.get(int(instruction[11:16], 2), 'error') + ', ' + str(int(instruction[21:26],2))
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_srl(instruction, pos, line):
    return 'srl'+disasm_sll(instruction, pos, line)[0][3:], disasm_sll(instruction, pos, line)[1]

def disasm_sra(instruction, pos, line):
    return 'sra'+disasm_sll(instruction, pos, line)[0][3:], disasm_sll(instruction, pos, line)[1]

def disasm_sllv(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_srlv(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_srav(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_jr(instruction, pos, line):
    ins = 'jr ' + reverse_register.get(int(instruction[6:11], 2), 'error')
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_jalr(instruction, pos, line):
    ins = 'jalr ' + reverse_register.get(int(instruction[16:21], 2), 'error') + ', ' + \
    reverse_register.get(int(instruction[6:11], 2), 'error')
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_movz(instruction, pos, line):
    return 'movz'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_movn(instruction, pos, line):
    return 'movn'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_syscall(instruction, pos, line):
    ins = 'syscall'
    return ins, -1
def disasm_break(instruction, pos, line):
    ins = 'break'
    return ins, -2
def disasm_sync(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_mfhi(instruction, pos, line):
    ins = 'mfhi ' + reverse_register.get(int(instruction[16:21], 2), 'error')
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_mthi(instruction, pos, line):
    ins = 'mthi ' + reverse_register.get(int(instruction[6:11], 2), 'error')
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1

def disasm_mflo(instruction, pos, line):
    return 'mflo'+disasm_mfhi(instruction, pos, line)[0][4:], disasm_mfhi(instruction, pos, line)[1]

def disasm_mtlo(instruction, pos, line):
    return 'mtlo'+disasm_mthi(instruction, pos, line)[0][4:], disasm_mthi(instruction, pos, line)[1]

def disasm_mult(instruction, pos, line):
    ins = ''
    return ins, -2
def disasm_multu(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_div(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_divu(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_add(instruction, pos, line):
    ins = 'add ' + reverse_register.get(int(instruction[16:21], 2), 'error') + ', ' + \
        reverse_register.get(int(instruction[6:11], 2), 'error') + ', ' + \
          reverse_register.get(int(instruction[11:16], 2), 'error')
    if re.search('error', ins):
        raise Exception('Line %d : No such register.' % line)
    return ins, -1
def disasm_addu(instruction, pos, line):
    return 'addu'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_sub(instruction, pos, line):
    return 'sub'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_subu(instruction, pos, line):
    return 'subu'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_and(instruction, pos, line):
    return 'and'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_or(instruction, pos, line):
    return 'or'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_xor(instruction, pos, line):
    return 'xor'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_nor(instruction, pos, line):
    return 'nor'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_slt(instruction, pos, line):
    return 'slt'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_sltu(instruction, pos, line):
    return 'sltu'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]

def disasm_tge(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_tgeu(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_tlt(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_tltu(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_teq(instruction, pos, line):
    ins = '' 
    return ins, -2
def disasm_tne(instruction, pos, line):
    ins = '' 
    return ins, -2

def disasm_mul(instruction, pos, line):
    return 'mul'+disasm_add(instruction, pos, line)[0][3:], disasm_add(instruction, pos, line)[1]


ops = {
    0: disasm_ops00,
    1: disasm_ops01,
    2: disasm_j,
    3: disasm_jal,
    4: disasm_beq,
    5: disasm_bne,
    6: disasm_blez,
    7: disasm_bgtz,
    8: disasm_addi,
    9: disasm_addiu,
    10: disasm_slti,
    11: disasm_sltiu,
    12: disasm_andi,
    13: disasm_ori,
    14: disasm_xori,
    15: disasm_lui,
    16: disasm_ops16,
    17: disasm_ops17,
    18: disasm_ops18,
    20: disasm_beql,
    21: disasm_bnel,
    22: disasm_blezl,
    23: disasm_bgtzl,
    28: disasm_ops28,
    32: disasm_lb,
    33: disasm_lh,
    34: disasm_lwl,
    35: disasm_lw,
    36: disasm_lbu,
    37: disasm_lhu,
    38: disasm_lwr,
    40: disasm_sb,
    41: disasm_sh,
    42: disasm_swl,
    43: disasm_sw,
    46: disasm_swr,
    47: disasm_cache,
    48: disasm_ll,
    49: disasm_lwc1,
    50: disasm_lwc2,
    51: disasm_pref,
    53: disasm_ldc1,
    54: disasm_ldc2,
    56: disasm_sc,
    57: disasm_swc1,
    58: disasm_swc2,
    61: disasm_sdc1,
    62: disasm_sdc2
}

ops00 = {
    0: disasm_sll,
    2: disasm_srl,
    3: disasm_sra,
    4: disasm_sllv,
    6: disasm_srlv,
    7: disasm_srav,
    8: disasm_jr,
    9: disasm_jalr,
    10: disasm_movz,
    11: disasm_movn,
    12: disasm_syscall,
    13: disasm_break,
    15: disasm_sync,
    16: disasm_mfhi,
    17: disasm_mthi,
    18: disasm_mflo,
    19: disasm_mtlo,
    24: disasm_mult,
    25: disasm_multu,
    26: disasm_div,
    27: disasm_divu,
    32: disasm_add,
    33: disasm_addu,
    34: disasm_sub,
    35: disasm_subu,
    36: disasm_and,
    37: disasm_or,
    38: disasm_xor,
    39: disasm_nor,
    42: disasm_slt,
    43: disasm_sltu,
    48: disasm_tge,
    49: disasm_tgeu,
    50: disasm_tlt,
    51: disasm_tltu,
    52: disasm_teq,
    54: disasm_tne
}

ops01 = {

}

ops16 = {

}

ops17 = {

}

ops18 = {

}

ops28 = {
    2: disasm_mul
}

def int_comp(str_):
    if(str_[0] == '1'):
        tmp = int(str_[1:],2)
        return str(-tmp + 1)
    else:
        return str(int(str_,2))