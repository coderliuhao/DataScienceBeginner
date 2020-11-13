use crashcourse;

#聚集函数

/*
avg()  返回某列平均值
count()  返回某列的行数
max()  返回某列的最大值
min()  返回某列最小值
sum()  返回某列值之和
*/

select avg(prod_price) as avg_price
from products;

select avg(prod_price) as avg_price
from products
where vend_id=1003;#返回某供货商的产品价格的均值

#avg函数只能用来确定特定数值列的平均值，数值列名作为avg函数的参数
#avg()函数忽略值为Null的行


#count()函数确定表中行的计数或符合特定条件的行的数目
#count(*) 对表中行计数，不论列中是否含有空值
select count(*) as num_count
from customers;

#count(col) 对特定列具有值计数。忽略NUll空值
select count(cust_email) as num_cust
from customers;#返回cust_eamil中有值的行数


#max()函数要求指定列名，忽略列中为NULL值的行
select max(prod_price) as max_price
from products;#返回最贵的物品价格

/*
tips:max()一般用来找最大数值或者日期值。
mysql中还允许max()返回任意列的最大值,包括文本列的最大值。
用于文本数据时，如果数据按相应列排序，则max(）返回最后一行
*/

select min(prod_price) as min_price
from products;
/*
对应的min()函数，传入指定列名，可以是任意类型的列。
min()忽略列中为NULL的行
*/


#sum()函数 忽略为NULL值的行

select sum(quantity) as item_ordered
from orderitems
where order_num=20005;#返回指定订单号下的所有产品数量之和

select sum(quantity*item_price) as tot_price
from orderitems
where order_num=20005;#返回指定订单编号的总订单金额
#利用算术操作符，聚合函数可以执行多个列的计算


#distinct,返回某列全部的唯一值，可与其他聚合函数配合使用

select avg(distinct prod_price) as avg_price
from products
where vend_id=1003;
#返回1003号供应商只考虑不同价格的平均值

/*
如果指定列名，distinct只能用于count(),不能用于count(*),
不允许count(distinct)的写法，且distinct必须指定列名，
不能用于计算或表达式。
*/


#组合聚集函数

select count(*) as num_items,
	   max(prod_price) as max_price,
       min(prod_price) as min_price,
       avg(prod_price) as avg_price
from products;       
#组合count,max,min,avg四个聚合函数并重新指定别名


