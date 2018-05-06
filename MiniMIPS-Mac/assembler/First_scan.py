from assembler.asm_utils import *

def first_scan(text):
    length = len(text)
    dicts = {}
    position = 0
    data_area = False
    data_cursor = 0
    text_cursor = 0
    for i in range(length):
        line = i + 1
        try:
            if text[i] == '':
                continue
            if (re.search(r'#', text[i])):
                pos = re.search(r'#', text[i]).span()[0]
                if(text[i][0:pos].strip() == ''):
                    continue
                text[i] = text[i][0:pos]

            if(re.search(r'\.text',text[i])):
                data_area = False
                pos = re.search('\.text',text[i]).span()[1]
                address = text[i][pos:len(text[i])].strip()
                if(address):
                    address = int(address,16)
                    if(position > address):
                        raise Exception('Line %d : Current address can\'t be smaller than cursor.'% line)
                else:
                    address = position
                position = address
                dicts['text_'+str(text_cursor)] = position
                text_cursor = text_cursor + 1
            elif(re.search(r'\.data',text[i])):
                data_area = True
                pos = re.search(r'\.data',text[i]).span()[1]
                address = text[i][pos:len(text[i])].strip()
                if(address):
                    address = int(address,16)
                    if(position > address):
                        raise Exception('Line %d : Current address can\'t be smaller than cursor.'% line)
                else:
                    address = position
                position = address
                dicts['data_'+str(data_cursor)] = position
                data_cursor = data_cursor + 1
            elif(re.search(r':',text[i])):
                pos = re.search(r':',text[i]).span()[0]
                name = text[i][0:pos].strip()
                if(re.search(' ',name)):
                    raise Exception('Line %d : Can\'t contain space between the label.'% line)
                dicts[name] = position
                if(text[i][pos+1:len(text[i])].strip() == ''):
                    continue
                if(data_area):
                    occupy , _ = process_data(text[i][pos+1:len(text[i])].strip(),line)
                    position = position + occupy
                else:
                    param = text[i][pos+1:len(text[i])].strip().split(',')
                    param = [i.strip() for i in param]
                    param[0] = re.sub('[ ]+', ' ', param[0])
                    op, param[0] = param[0].split(' ')
                    if op in pseudo_func:
                        position = position + 8
                    else:
                        position = position + 4
            elif(re.search(r'\.',text[i])):
                if(not data_area):
                    raise Exception('Line %d : Can\'t resolve this symbol in text area.'% line)
                occupy, _ = process_data(text[i].strip(),i)
                position = position + occupy
            else:
                try:
                    param = text[i].split(',')
                    param = [i.strip() for i in param]
                    param[0] = re.sub('[ ]+', ' ', param[0])
                    op, param[0] = param[0].split(' ')
                    if op in pseudo_func:
                        position = position + 8
                    else:
                        position = position + 4
                except Exception as e:
                    position = position + 4
        except Exception as e:
            return dicts,line,e
    return dicts,-1,Exception('None')