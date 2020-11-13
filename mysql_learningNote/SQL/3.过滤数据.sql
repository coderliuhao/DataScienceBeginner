USE crashcourse;

select prod_name,prod_price
from products
where prod_price=2.50;#只返回prod_price=2.50的行

#如果同时使用where和order by则应该让order by子句在where之后

/*操作符
= 等于，！=不等于，<>不等于，<小于  >大于，>=大于等于  <=小于等于
between 介于指定两个值之间
*/

select prod_name,prod_price
from products
where prod_name="fuses";#值的名称也不区分大小写

select prod_name,prod_price
from products
where prod_price<10;

select prod_name,prod_price
from products
where prod_price<=10;


select vend_id,prod_name
from products
where vend_id <> 1003;#返回不是由1003供应商制造的所有产品

#tips 值为字符串类型时需要用引号限定，数值列进行比较的值不用引号

#等价的！=

select vend_id,prod_name
from products
where vend_id != 1003;


select prod_name,prod_price
from products
where prod_price between 5 and 10;#左右均为闭区间，即包括5和 10

select prod_name
from products
where prod_price is null;#返回空的prod_price字段，不同于0，空字符串，空格

select cust_id
from customers
where cust_email is null;#cust_email有空值，返回为空值的cust_id


#组合where语句

#用操作符连接或改变where子句中的子句的关键字，逻辑操作符

select prod_id,prod_price,prod_name
from products
where vend_id=1003 and prod_price<=10;#and连接，意味着返回同时满足所有给定条件的行
#检索由1003号供应商制造的且价格小于10的产品名称和价格


select prod_name,prod_price
from products
where vend_id=1002 or vend_id=1003; 
#返回任一个由指定供应商制造的所有产品名称和价格

#将上述where子句中的or换成and

select prod_name,prod_price
from products
where vend_id=1002 and vend_id=1003;#没有数据返回

#or用来检索满足任一给定条件的行

#如果要检索价格大于等于10，且由 1002或1003制造的产品的名称

select prod_name,prod_price
from products
where vend_id=1002 or vend_id=1003 and prod_price>=10;
#上述where解读为:1003制造商生产的价格大于10的产品或者由1002生产的任何产品
#由于and优先级高于or，因此上述where语句并不能按预期检索


select prod_name,prod_price
from products
where (vend_id=1002 or vend_id=1003) and prod_price>=10;
#在前面的条件加括号提升运算的优先级，首先计算括号里的语句在执行and运算
#上述语句符合预期，圆括号明确的分组操作符，消除因运算优先级引发的歧义


select prod_name,prod_price
from products
where vend_id in (1002,1003)#in操作符指定条件范围，检索由1002和1003制造的所有产品
order by prod_name;         #条件清单必须在圆括号中

#上面等价操作
select prod_name,prod_price
from products
where vend_id=1002 or vend_id=1003
order by prod_name;


#not操作符 否定出现在它之后的任何条件

select prod_name,prod_price
from products
where vend_id not in (1002,1003)#列出除1002,1003以外供应商制造的产品
order by prod_name;











