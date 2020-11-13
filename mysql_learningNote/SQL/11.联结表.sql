use crashcourse;

#使用联结表

/*
表中具有唯一标识的列叫做主键，通常是id、编号，名称之类的

如果表A中的某列在表B中做主键，那么这一列还可以叫表A的外键，定义了量表的关系。
*/

#创建联结
select vend_name,prod_name,prod_price
from vendors,products
where vendors.vend_id=products.vend_id
order by vend_name,prod_name;
#select中prod_name,prod_price来自products,vend_name来自vendors
#from 语句列出需要联结的两个表
#where子句通过匹配vend_id进行联结,由于列名一样，使用完全限定名。

#上述代码没有where子句
select vend_name,prod_name,prod_price
from vendors,products
order by vend_name,prod_name;
#返回84行数据，6个供应商，为每个供应商都匹配14个产品
#显然不是正确的，因为有的供应商匹配了不正确的产品，有些供应商赝本没有产品
#笛卡尔积：如果没有hwhere子句的联结条件，返回结果的行数是两个需要联结的表的行数乘积。
#因此要保证所有的联结都要有where子句

#内部联结

select vend_name,prod_name,prod_price
from vendors inner join products
on vendors.vend_id=products.vend_id;
#inner join创建内部联结与on子句配合使用，效果与from...where的等值联结一样

#联结多个表
select prod_name,vend_name,prod_price,quantity
from orderitems,products,vendors
where products.vend_id=vendors.vend_id
  and orderitems.prod_id=products.prod_id
  and order_num=20005;
/*
上方代码显示编号为20005订单中的物品。订单物品储存在orderitem表，
每个产品按产品ID存储，引用products的中产品。这些产品通过供应商ID
联结到vendors表中的相应的供应商，供应商ID储存在每个产品的记录中。
*/  

#子查询写法
select cust_name,cust_contact
from customers
where cust_id in (select cust_id
                  from orders
                  where order_num in (select order_num
                                      from orderitems
                                      where prod_id="TNT2"));

#联结表写法
select cust_name,cust_contact
from customers inner join orders inner join orderitems
on customers.cust_id=orders.cust_id
and orders.order_num=orderitems.order_num
and prod_id="TNT2";




