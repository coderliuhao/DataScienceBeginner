use crashcourse;

#文本处理函数
select vend_name,Upper(vend_name) as vend_name_upcase
from vendors
order by vend_name;
#upper()函数将文本转换成大写形式，返回原值以及大写变换后的值
/*
left() 返回串左边的字符
right() 返回串右边的字符
length() 返回串的长度
locate() 找到串的一个子串
lower() 将串转为小写
upper() 将串转为大写
ltrim() 删除串左边的空格
rtrim() 删除串右边的空格
soundex() 返回串的SOUNDEX值 :
   soundex是一个将任何文本串转换为描述其语音表示的字母数字模式的算法
substring() 返回字符串的字符 
*/

#soundex example
select cust_name,cust_contact
from customers
where cust_contact="Y.Lie"; 
#上面语句没有返回值


select cust_name,cust_contact
from customers
where soundex(cust_contact)=Soundex("Y.Lie");   
#返回发音相似的Y.Lee


#日期处理函数
/*
AddDate()  增加一个日期(天，周等)
AddTime()  增加一个时间(时，分等)
CurDate()  返回当前日期
CurTime()  返回当前时间

Date()     返回日期时间的日日期部分
Time()     返回日期时间的时间部分
Year()     返回日期的年份部分
Month()    返回日期的月份部分
Day()      返回日期的天数部分
Hour()     返回时间的小时部分
Minute()   返回时间的分钟部分
Second()   返回时间的秒数部分

Date_Format() 返回一个格式化的日期或时间串 
DateDiff() 计算两个日期之差 
Date_Add() 高度灵活的日期计算函数
DayofWeek() 对一个日期返回是星期几 
Now()       返回当前的日期和时间
*/

select cust_id,order_num
from orders
where order_date="2005-09-01";
#为解决上述检索方式，可能不能检索到含有日期和时间的值，使用date()函数
#更好写法
select cust_id,order_num
from orders
where date(order_date)="2005-09-01";
#同理如果检索时间时，为避免出现日期时间不能检索到的问题，使用time()函数


select cust_id,order_num
from orders
where date(order_date) between "2005-09-01" and "2005-09-30";
#beetween来检索一个日期范围

#s等价写法
select cust_id,order_num
from orders
where year(order_date)=2005 and Month(order_date)=9:
#分别使用year()函数和month()函数检索相应的年份和月份


#数值处理函数
/*
abs()   求绝对值
cos()   求余弦 
sin()   求正弦
tan()   求正切
mod()   求余数
pi()    圆周率
rand()  返回随机数
sqrt()  返回平方根 
exp()   返回指数值
*/
