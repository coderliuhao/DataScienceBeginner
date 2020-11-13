import re

# re.match(pattern,string,flags=0)
#pattern为正则表达式
#string为要匹配的字符串
#flag 为标志位，控制正则表达式匹配方式，如是否区分大小写，多行匹配等等
print(re.match("www","www.nowcoder.com").span())#起始位置匹配
print(re.match("com","www.nowcoder.com"))#不在起始位置匹配

#example
line="Cats are smarter than dogs"

match_obj=re.match(r"(.*) are (.*?) .*",line,re.M|re.I)
### ".*"表示任意匹配除换行符("\n","\r")之外的任何单个或多个字符
"""match方法返回一个匹配的对象，该对象的group方法(group(),group(num))用于获取匹配表达式,group(num=0)匹配的整个表达式的字符串，可以一次输入多个组号，返回包含那些组对应值的元组。"""

"""group()参数为空时，返回包含全部小组字符的元组，与group(0)等价"""


if match_obj:
    print("match_obj.group():",match_obj.group())
    print("match_obj.group(0):",match_obj.group(0))
    print("match_obj.group(1):",match_obj.group(1))
    print("match_obj.group(2):",match_obj.group(2))
    print("match_obj.group(1,2):",match_obj.group(1,2))
else:
    print("NO Match")


#re.search方法:扫描整个字符串并返回第一个成功的匹配
#re.search(pattern,string,flags=0)参数含义与match相同

"""使用re.search()方法，成功匹配到时返回一个匹配的对象，该对象同样具有group()方法，用法与match中的group相同；若没有成功匹配到字符串，返回None"""

print(re.search("www","www.nowcode.com").span())
print(re.search("com","www.nowcode.com").span())


search_obj=re.search(r"(.*) are (.*?) .*",line,re.M|re.I)

if search_obj:
    print("search_obj.group():",search_obj.group())
    print("search_obj.group(0):",search_obj.group(0))
    print("search_obj.group(1):",search_obj.group(1))
    print("search_obj.group(2):",search_obj.group(2))
    print("search_obj.group(1,2):",search_obj.group(1,2))
else:
    print("Nothinh found")

"""re.match与re.search的区别：re.match只匹配字符串开始，如果字符串开始不符合正则表达式，则匹配失败，返回None;re.search匹配整个字符串，知道找到一个匹配。"""


match_d=re.match(r"dogs",line,re.M|re.I)
search_d=re.search(r"dogs",line,re.M|re.I)

if match_d:
    print("match --> match_d.group():",match_d.group())
else:
    print("No match")

if search_d:
    print("search --> search_d.group():",search_d.group())
else:
    print("No match")



#检索和替换
#re.sub(pattern,replace_obj,string,count=0,flags=0)
"""参数说明：
pattern: 正则中的模式字符串
replace_obj:替换后的字符串
string:被查找的原始字符串
count:模式匹配后替换的最大次数，默认0意味着替换所有的匹配
flags:编译时用的匹配模式，数字形式"""

#上述参数中前三个是必选参数，后两个可选

phone="2020-09-01 # 这就是今天的日期" 

num=re.sub(r"#.*$","",phone)
print("今天的日期:",num)

num0=re.sub(r"\D","",phone)
print("今天的日期:",num0)

#replace_obj也可以是函数

def double(matched):
    value=int(matched.group("value"))
    return str(value*2)

s="A23g4HFD567"

print(re.sub("(?P<value>\d+)",double,s))

#re.compile(pattern,flags)
#用于编译正则表达式，生成一个正则表达式对象，供match和search使用
#flags具体参数为：
"""re.I:忽略小写
    re.L:表示特殊字符集\w,\W,\b,\B,\s,\S依赖于当前环境
    re.M:多行模式
    re.S:“.”并且包括换行符在内的任意字符
    re.U:表示特殊字符集\w,\W,\b,\B,\d,\D,\s,\S依赖于Unicode字符属性数据库
    re.X:为增加可读性，忽略空格和"#"后的注释 
"""

pattern=re.compile(r"\d+") #用于匹配至少一个数字
m=pattern.match("one12twothree34four")
print("m:",m)

m1=pattern.match("one12twothree34four",2,10)
print("m1:",m1)

m2=pattern.match("one12twothree34four",3,10)
print("m2:",m2)

print("m2.group():",m2.group())

print("m2.start():",m2.start())

print("m2.end():",m2.end())

#m1,m2为match对象，包含以下方法：
"""group()
   start():用于获取分组匹配的子串在整个字符串中的起始位置(子串第一个位置的索引，默认为0.
   end():用于获取分组匹配的子串在整个字符串中的结束位置，子串最后一个字符的索引+1
   span(): 返回获取分组匹配子串的(start,end)的元组
"""

pat=re.compile(r"([a-z]+) ([a-z]+)",re.I)

m3=pat.match("Hello World Wide Web")

print("m3:",m3)

print("m3.span():",m3.span())
print("m3.span(1):",m3.span(1))
print("m3.span(2):",m3.span(2))

print("m3.group():",m3.group(0))
print("m3.group(1):",m3.group(1))
print("m3.group(2):",m3.group(2))
print("m3.groups():",m3.groups())#等价于(m.group(1),m.group(2))

"""findall函数：在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，若没有找到匹配的，返回空列表。
findall是匹配所有，match和search是匹配一次

re.findall(string[,pos[,endpos]])
参数：string:待匹配的字符串
      pos:可选参数，指定字符串的起始位置，默认为0
      endpos:可选参数，指定字符的结束位置，默认为字符串长度"""

pattern=re.compile(r"\d+")#查找数字
res1=pattern.findall("nowcoder 123 google 456")
res2=pattern.findall("now88coder123google456",0,13)

print("res1:",res1)

print("res2:",res2)

#re.finditer()在字符串中找到正则表达式所匹配到的所有子串，将它们作为迭代器返回
"""re.finditer(pattern,string,flag=0)
参数：pattern:匹配的正则表达式
      string:待匹配的字符串
      flag :标志位，控制正则表达式的匹配方式"""

it=re.finditer(r"\d+","12a32bc43jf3")
for match in it:
    print(match.group())


#re.split()按照能够匹配的子串将字符串分割后返回列表
#re.split(pattern,string[,maxsplit,flags=0])
"""pattern:正则表达式
   string:待匹配的字符串
   maxsplit:可选参数。分割次数，默认为0，不限制次数
   flags:标志位"""

rs1=re.split("\W+","nowcoder,nowcoder,nowcoder.")
print("rs1:",rs1)
rs2=re.split("(\W+)"," nowcoder, nowcoder, nowcoder.")
print("rs2:",rs2)
rs3=re.split("\W+"," nowcoder, nowcoder, nowcoder.",1)
print("rs3:",rs3)
rs4=re.split("a*","hello world")
print("rs4:",rs4)

"""正则表达式对象：
1、re.RegexObject，re.compile()返回RegexObject对象
2、re.MatchObject,group()返回被re匹配的字符串(start(),end(),span())

"""







































