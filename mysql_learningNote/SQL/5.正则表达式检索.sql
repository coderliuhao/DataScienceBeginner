use crashcourse;

#基本字符匹配

select prod_name
from products
where prod_name REGEXP '1000'#与文字正文1000匹配的表达式
order by prod_name;

#regexp：正则表达式关键字，它告诉mysqlregexp后面跟的是正则表达式


select prod_name
from products
where prod_name regexp ".000" 
order by prod_name;

#上述正则表达式.000，“.”用来匹配任意一个字符，
# 所以结果中1000和2000都匹配且返回


#like与regexp的差别

select prod_name
from products
where prod_name like "1000"#注意此处没有使用通配符
order by prod_name;
#上面的语句不返回数据

select prod_name
from products
where prod_name regexp "1000"
order by prod_name;
#有返回数据

/*
like和regexp都可以用来匹配整个列。

区别：
like匹配整个列，在无通配符的条件下，被匹配的文本在列中出现时like不会找到它，
相应的行也不会返回。

regexp在列值内进行匹配，匹配的文本在列值中出现时，regexp会找到它，
并返回相应行。

tips 正则表达式regexp不区分大小写，大写和小写都匹配，
若要区分大小写，在正则表达式前使用binary关键字。
*/


#进行or匹配 “|”

select prod_name
from products
where prod_name regexp "1000|2000"
order by prod_name;
#正则表达式1000|2000，"|"为正则表达式的or操作符，即匹配其中之一
#因此结果中1000和2000都返回

#tips:多个or时可以增加“|”符号来增加条件 举例：1000|2000|3000


select prod_name
from products
where prod_name regexp "[123] Ton";
#正则表达式[123] Ton,[123]定义一组字符，用于匹配1或2或3
#[^123]将匹配除这些字符之外的任何东西

#等价
select prod_name
from products
where prod_name regexp "[1|2|3] Ton";


#匹配范围
select prod_name
from products
where prod_name regexp "[1-5] ton";
#表达式[1-5]为一个集合，用来定义一个范围，上述语句将返回包含"1-5之间的数字 Ton"

#同理[a-z]能匹配任何的字母字符，[A-Z]能匹配所有大写字母字符



#匹配特殊字符
select vend_name
from vendors
where vend_name regexp "."#"."匹配任意字符。返回所有行
order by vend_name;

select vend_name
from vendors
where vend_name regexp "\\.";#p匹配带"."的行
#表达式”\\.“,匹配特殊字符时必须用\\作为前导,\\是mysql的转义字符
#\\-为查找”-“，\\.为查找"."，匹配反斜杠"\"时，使用”\\\“


/*
\\f  换页
\\n  换行
\\r  回车
\\t  制表
\\v  纵向制表

*/

#匹配字符类
/*
[:alnum:] 任意字母和数字，同([a-zA-Z0-9)
[:alpha:] 任意字符，同（[a-zA-Z]）
[:blank:] 空格和制表，同([\\t])
[:cntrl:] ASCII控制字符
[:digit:] 任意数字，同([0-9])
[:graph:] 与[:print:]相同，不包含空格
[:lower:] 任意小写字母，同([a-z])
[:print:] 任意可打印字符
[:punct:] 既不在[:alnum:]也不在[:cntrl:]中的字符
[:space:] 包括空格在内的任意空白字符，同([\\f,\\n,\\r,\\t,\\v])
[:upper:] 任意大写字母，同([A-Z])
[:xdigit:] 任意十六进制数字，同([a-fA-F0-9])
*/

#匹配多个实例

/*
元字符      说明
*          0个或多个匹配
+          1个或多个匹配({1,})
?          0个或1个被匹配({0,1})
{n}        指定数目的匹配
{n,}       不少于指定数目的匹配
{n,m}      匹配数目的范围
*/

select prod_name
from products
where prod_name regexp "\\([0-9] sticks?\\)"
order by prod_name;
/*
表达式解读:
1、\\转义后面括号里的反斜杠字符
2、[0-9]匹配任意数字
3、sticks?,s后的?使s可选，?匹配0次或一次它前面的字符s,
  因此可以匹配stick和sticks。
*/

#匹配连在一起的4个数字
select prod_name
from products
where prod_name regexp "[[:digit:]]{4}"#匹配任意数字4次
order by prod_name;

#等价表达式
select prod_name
from products
where prod_name regexp "[0-9]{4}"
order by prod_name;

#定位符
/*
元字符       
  ^      匹配文本开始 
  $      文本的结尾
[[:<:]]  词的开始
[[:>:]]  词的结尾
*/

#匹配名字以数字(包括小数点)开头的产品
select prod_name
from products
where prod_name regexp "^[0-9\\.]"
order by prod_name;
#因为^匹配字符串的开始，因此^[0-9\\.]只在"."或任意数字为字符串首字符时匹配


