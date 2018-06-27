import re
'''
. 匹配任意字符 （除了\n）
[...] 匹配任意字符集 
\d\/D 匹配数字 / 非数字
\s/\S 匹配空白/非空白字符
\w/\W 匹配单词字符 [a-zA-Z0-9]/非单词字符
* 匹配前一个字符0次或者无限次
+ 匹配前一个字符1次或者无限次
? 匹配前一个字符0次或者1次
{m}/{m,n}匹配前一个字符m次或者n次
*? / +? / ?? 匹配模式变为非贪婪匹配(尽可能的匹配少的字符)
^ 匹配字符串开头
$ 匹配字符串的结尾
| 匹配左右任意一个表达式
(ab) 括号中表达式作为一个分组
\<number> 引用编号为number的分组匹配到的字符串，编号从1开始
(?P<name>)分组取一个别名
(?P=name) 引用别名为name的分组匹配到的字符串

'''
str111 = "Ben Lyonssss"

pa = re.compile(r"(ben)", re.I)
print(type(pa)) # <class '_sre.SRE_Pattern'>
ma = pa.match(str111)
print(ma) #<_sre.SRE_Match object; span=(0, 3), match='Ben'>
res = ma.group()
ress = ma.groups()
print(ress) # ('Ben',)
print(res) # Ben
print(ma.re) #re.compile('Ben')
print(ma.string) #Ben Lyonssss
print(ma.span()) #(0, 3)


pa = re.compile(r"{\w+}")
str1 = "{asdasd}"
ma = pa.match(str1)
res = ma.group()
print(res)


pa1 = re.compile(r"[A-Z][a-z]*")
str1 = "Aa"
ma = pa1.match(str1)
res = ma.group()
print(res)

# 非贪婪模式
ma = re.match(r"[0-9][a-z]+?", "1bbb")
print(ma.group())

# 匹配xml

ma = re.match(r"<([\w]+>)[\w]+</\1", "<book>python</book>")
print(ma.group())
print(ma.groups()) # 取分组匹配到的字符串, 以元组的形式返回
ma = re.match(r"<(?P<mark>[\w]+>)[\w]+</(?P=mark)", "<book>python</book>")
print(ma.group())

# sub 函数高级使用
def add1(match):
    val = match.group()
    val = int(val) + 1
    return str(val)


print(re.sub(r"\d+", add1, "iii111"))









