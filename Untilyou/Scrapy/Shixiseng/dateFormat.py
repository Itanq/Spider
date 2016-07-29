#!/usr/bin/python

import re
import os
import sys
import json

# 把给定的字符串变成一行
def BeLine(Str, douhao):
    line = ""
    for ch in Str:
        if ch=='\n':
            continue
        else:
            line += ch
    line += douhao
    line += '\n'
    return line

# 提取文本中json数据成列表的形式
def TextToList(text):
    f = open(text, "r+")
    date = f.read()
    List = []
    Str = ""
    size = len(date)
    for i in range(size):
        Str += date[i]
        if date[i]=='}':
            List.append(Str)
            Str = ""
    f.close()
    return List

def YouWant(Str):
    line = ""
    # 去除jobclass空值
    pos = Str.find('jobClass') + 10
    tmp = Str[pos+1:pos+3]
    # 防止jobClass为空值
    if tmp!="[]":
        Str = Str[:pos]+""+Str[pos+5:]
    size = len(Str)
    # 去除中括号
    for i in range(size):
        # 没有的值设为默认值值
        if Str[i]=='[' and Str[i+1]==']':
            line += '"www.untilyou.com"'
        if Str[i]=='[' or Str[i]==']':
            continue
        line += Str[i]
    return line

def FixJson(fileName):
    f = open('ans.json', 'w+')
    f.write(' ')
    List = TextToList(fileName)
    c = 0
    count = len(List)
    douhao = ''
    for li in List:
        c = c + 1
        if c==count:
            douhao = ''
        else:
            douhao = ','
        line = BeLine(li, douhao)
        line = YouWant(line)
        f.write(line)
    f.seek(0, os.SEEK_SET)
    f.write('[')
    f.seek(0, os.SEEK_END)
    f.write(']')
    f.close()
        
fileName = 'shixiseng.json'
FixJson(fileName)
print("success")
