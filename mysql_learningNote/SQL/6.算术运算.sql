use crashcourse;

#字段 基本与列的意思相同

#mysql通常用Concat()函数实现字段拼接

select Concat(vend_name,"(",vend_country, ")")
from vendors
order by vend_name;
/*
Concat()拼接串，每个串之间用“，”分隔，上述连接以下4个元素

存储在vend_name中的名字
包含一个空格和一个左圆括号的串
存储在vend_country中的国家
包含右边括号的串
*/

#去掉数据左右的空格

select concat(RTrim(vend_name)," (",Rtrim(vend_country), ")")
from vendors
order by vend_name;

#rtrim()：去掉值右边的空格，ltrim()去掉左边的空格
#trim()去掉值两边的空格


#使用别名
select concat(rtrim(vend_name)," (",rtrim(vend_country),")") as vend_title
from vendors
order by vend_name;

/*
关键字as :一个字段或值的替换名，alias.
指示mysql传建一个包含vend_title的计算字段
*/


#执行算术计算

select prod_id,quantity,item_price
from orderitems
where order_num=20005;

select prod_id,
       quantity,
	   item_price,
       quantity*item_price as expand_items
from orderitems
where order_num=20005;       
# 通过quantity和item_price的乘积可以得到计算字段总expand_price
#四种算术操作符 + - * /加减乘除

select trim(" abc ");