# coding:utf8
import sys
import os
import pyperclip

def split_text_at_period(text,split_len = 5000):
    split_num=int(len(text)/split_len)
    text_list = [text]

    for i in range(split_num):
        tmp_list = text_list[i][split_len*i:split_len*(i+1)].rsplit('\n',1)
        text_list[i] = tmp_list[0]
        text_list.append(tmp_list[1] + text[split_len*(i+1):])


    return text_list



if __name__ == "__main__":
    #with open('udemy.txt') as f:
    #    base_text = f.read()
    print('Delete annoying indention from clipboard')
    base_text = pyperclip.paste()
    replace_text = base_text.replace('\r\n', '')
    replace_text = replace_text.replace('.', '.\n')
    pyperclip.copy(replace_text)

    text_len = len(replace_text)
    if text_len > 5000:
        print('Over 5000 char. Text length :'+str(text_len))
        #replace_text_list = replace_text[:5000].rsplit('\r\n',1)
        #replace_text_list[1] = replace_text_list[1] + replace_text[5000:]

        text_list = split_text_at_period(replace_text)
        f = open('udemy.txt', 'w')
        for text in text_list:
            #pyperclip.copy(text)
            f.write(text)
            f.writelines('\r\n')
        
        f.close()

    #print(base_text)
    #print(replace_text)
