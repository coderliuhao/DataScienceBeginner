USE crashcourse;
SELECT prod_name,prod_id,prod_price #取多列
FROM products;

select *  #取所有列，包括为止列名
from products;

select vend_id  
from products;

select distinct vend_id #distinct关键字指示mysql返回不同值
from products;          

select distinct vend_id,prod_price #distinct应用于所有列
from products; #两列数据每一行都不同

select prod_name
from products
limit 5;  #limit关键字，返回不多于几行数据

select prod_name
from products
limit 5,5; #第一个数5为起始行，第二个数5为检索的行数。即返回从5行开始的5行
           #5,6,7,8,9行，末端行索引为5+5-1
select prod_name
from products
limit 1,10; #末端的行索引为1+10-1

select prod_name
from products
limit 1; #仅有一个值的limit总是从第一行开始


select prod_name
from products
limit 10,5;#行数不够时mysql将返回它能返回的那么多行


select products.prod_name #同时使用表名和列名完全限定列
from products;

select product.prod_name
from crashcourse.products; #表名也可以完全限定











