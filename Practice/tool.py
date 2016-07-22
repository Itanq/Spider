#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Tool():
    '''
        处理页面标签
    '''
    # 去除img标签,7位空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接
    removeAddr = re.compile('<a.*?>|</a>')
    # 去除额外的标签
    removeExtraTag = re.compile('<.*?>')
    # 把换行的标签换为 \n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 把制表格<td>替换为\t
    replaceTD = re.compile('<td>')
    # 将段落开头替换为\n+tab
    replacePara = re.compile('<p.*?>')
    # 将换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()




