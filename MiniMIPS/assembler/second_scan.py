from assembler.asm_utils import *

def second_scan(text,symbol_table):
    length = len(text)
    position = 0
    data_area = False
    result = ''
    text = [i.strip() for i in text]
    for i in range(length):
        try:
            line = i + 1
            if text[i] == '':
                continue
            if (re.search(r'#', text[i])):
                pos = re.search(r'#', text[i]).span()[0]
                if(text[i][0:pos].strip() == ''):
                    continue
                text[i] = text[i][0:pos]

            if (re.search(r'\.text', text[i])):
                data_area = False
                pos = re.search('\.text', text[i]).span()[1]
                address = text[i][pos:len(text[i])].strip()
                address = int(address, 16)
                while (address > position):
                    position = position + 1
                    result = result + '00000000'
            elif (re.search(r'\.data', text[i])):
                data_area = True
                pos = re.search('\.data', text[i]).span()[1]
                address = text[i][pos:len(text[i])].strip()
                address = int(address, 16)
                while (address > position):
                    position = position + 1
                    result = result + '00000000'

            elif (re.search(r':', text[i])):
                pos = re.search(r':', text[i]).span()[0]
                if (text[i][pos + 1:len(text[i])].strip() == ''):
                    continue
                if (data_area):
                    occupy, value = process_data(text[i][pos + 1:len(text[i])].strip(), line)
                    position = position + occupy
                    result = result + value
                else:
                    value,pseudo = process_text(text[i][pos + 1:len(text[i])].strip(),line,symbol_table,position)
                    result = result + value
                    if pseudo:
                        position = position + 8
                    else:
                        position = position + 4
            elif (re.search(r'\.', text[i])):
                if (not data_area):
                    raise Exception('Line %d : Can\'t resolve this symbol in text area.' % line)
                occupy, value = process_data(text[i].strip(), line)
                position = position + occupy
                result = result + value
            else:
                value,pseudo = process_text(text[i].strip(),line,symbol_table,position)
                if pseudo:
                    position = position + 8
                else:
                    position = position + 4
                result = result + value
        except Exception as e:
            return result,line,e
    return result,-1,Exception('None')