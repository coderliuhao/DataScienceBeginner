use crashcourse;

#视图：视图是虚拟的表，只包含使用时动态检索数据的查询

/*
视图常见应用
1 重用sql语句
2 简化sql操作
3 使用表的部分而不是全部表内容
4 保护数据。可以给用户授权表的特定部分的访问权限
  而不是整个表的访问权限 
5 更改数据格式和表示
*/
/*
视图规则和限制
1 视图必须唯一命名
2 对于可创建的视图数目没有限制
3 为创建视图需要有足够的访问权限
4 视图可以嵌套，可以利用其他视图中检索数据的查询来和构造视图
5 order by可以用在视图中，如果从该视图中检索数据select中也有order by,
  那么该视图中的order by 会被覆盖
6 视图不能索引，也不能有关联的触发器或默认值
7 视图可以和表一起使用
*/

/*
使用视图
1 视图用create view语句创建
2 使用show create view viewnames语句查看创建视图的语句
3 使用drop删除视图，drop view viewname
4 更新视图时可以先drop在create,也可以直接用create or replace view
  如果要更新的视图不存在，create or replace view会新建一个视图，如果存在，
  该语句会替换原视图

/*
考虑案例,获得产品TNT2订单的顾客信息
*/

#联结表写法

select cust_name,cust_contact
from customers,orders,orderitems
where customers.cust_id = orders.cust_id
and   orderitems.order_num = orders.order_num
and   prod_id = "TNT2";

#创建视图写法

create view productcustomers as
select cust_name,cust_contact,prod_id
from customers,orderitems,orders
where customers.cust_id = orders.cust_id
and   orderitems.order_num = orders.order_num;
#create view.... as ...语句创建一个联结三个表的视图，返回已订购任意产品的所有客户列表
#从productcustomers这个视图中检索订购产品id为‘TNT2’的客户
select cust_name,cust_contact
from productcustomers
where prod_id = 'TNT2';

#上面两种方法返回相同的结果，创建视图方法，可以继续用来查询订购别的产品的顾客信息

   
#视图重新格式化检索出的数据

#考虑在单个组合计算中返回供应商名称和国家

#拼接写法
select concat(rtrim(vend_name),"(",rtrim(vend_country),")") as vend_title
from vendors
order by vend_name;

#视图写法
create view vend_name_country as 
select concat(rtrim(vend_name),"(",rtrim(vend_country),")")
from vendors
order by vend_name;
select *
from vend_name_country;

#视图过滤不想要的数据
create view customer_emails as 
select cust_id,cust_name,cust_email
from customers
where customers.cust_email is not null;

select *
from customer_emails;

/*
tips:如果创建视图时使用了where子句，且在使用视图时也使用了where子句
     则两组where子句将自动组合。
*/


#视图与计算字段
#案例：检索某特定订单的产品，计算每种物品的总价

#常规写法
select prod_id,quantity,item_price,(quantity*item_price) as total_price
from orderitems
where order_num =20005;

#视图写法
create view total_price as 
select order_num,prod_id,quantity,item_price,
	   (quantity*item_price) as tot
from orderitems;       
#创建视图时，注意选择where子句中的条件所在的列，
#才能在使用视图时使用该列的条件过滤数据
select *
from total_price
where order_num = 20005;

#更新视图
/*
如果视图定义中有以下操作，则不能更新视图
1 group by分组
2 联结
3 子查询
4 并
5 聚集函数
6 distinct
7 导出计算列

tips:视图通常用于检索数据，而不用于更新


