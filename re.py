#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# 属性:
# 1.string: 匹配时使用的文本。
# 2.re: 匹配时使用的Pattern对象。
# 3.pos: 文本中正则表达式开始搜索的索引。值与Pattern.match()和Pattern.seach()方法的同名参数相同。
# 4.endpos: 文本中正则表达式结束搜索的索引。值与Pattern.match()和Pattern.seach()方法的同名参数相同。
# 5.lastindex: 最后一个被捕获的分组在文本中的索引。如果没有被捕获的分组，将为None。
# 6.lastgroup: 最后一个被捕获的分组的别名。如果这个分组没有别名或者没有被捕获的分组，将为None。
# 
# 方法：
# 1.group([group1, …]):
# 获得一个或多个分组截获的字符串；指定多个参数时将以元组形式返回。group1可以使用编号也可以使用别名；编号0代表整个匹配的子串；不填写参数时，返回group(0)；没有截获字符串的组返回None；截获了多次的组返回最后一次截获的子串。
# 2.groups([default]):
# 以元组形式返回全部分组截获的字符串。相当于调用group(1,2,…last)。default表示没有截获字符串的组以这个值替代，默认为None。
# 3.groupdict([default]):
# 返回以有别名的组的别名为键、以该组截获的子串为值的字典，没有别名的组不包含在内。default含义同上。
# 4.start([group]):
# 返回指定的组截获的子串在string中的起始索引（子串第一个字符的索引）。group默认值为0。
# 5.end([group]):
# 返回指定的组截获的子串在string中的结束索引（子串最后一个字符的索引+1）。group默认值为0。
# 6.span([group]):
# 返回(start(group), end(group))。
# 7.expand(template):
# 将匹配到的分组代入template中然后返回。template中可以使用\id或\g、\g引用分组，但不能使用编号0。\id与\g是等价的；但\10将被认为是第10个分组，如果你想表达\1之后是字符’0’，只能使用\g0。


import re

pattern0 = re.compile(r'world')
string0 = 'hello world!'

pattern1 = re.compile(r'(\w+) (\w+)(?P<sign>.*)')
string1 = 'hello world!'

# match() and search() 区别在于:
# match()函数只检测re是不是在string的开始位置匹配
# search()会扫描整个string查找匹配
# 他们拥有相同的属性和方法
m0 = re.match(pattern0, string0)
s0 = re.search(pattern0, string0)

if m0:
    print m0.group()
else:
    print "re.match(pattern0, string0) failure"

if s0:
    print s0.group()
else:
    print "re.search(pattern0, string0) failure"

m1 = re.match(pattern1, string1)

print "m1.string: ", m1.string
print "m1.re: ", m1.re
print "m1.pos: ", m1.pos
print "m1.endpos: ", m1.endpos
print "m1.lastindex: ", m1.lastindex
print "m1.group(): ", m1.group()
print "m1.group(1,2): ", m1.group(1,2)
print "m1.groups(): ", m1.groups()
print "m1.groupdict(): ", m1.groupdict()
print "m1.start(2): ", m1.start(2)
print "m1.end(2): ", m1.end(2)
print "m1.span(2): ", m1.span(2)
print r"m1.expand(r'\g \g\g'): ", m1.expand(r'\2 \1\3')


# re.findall()

pattern = re.compile(r'\d+')
List = re.findall(pattern, 'one1two2three3four4fifty-four54')
print List


