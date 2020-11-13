use crashcourse;

#子查询：嵌套在其他查询中的查询

/*
考虑案例

1  检索包含物品TNT2的所有订单编号   prod_id==>order_num
2  检索具有前一步骤列出的订单编号的所有客户id order_num==>cust_id
3  检索前一步返回的所有客户ID的客户信息 cust_id==>cust_name,cust_contact

*/

/*
实现上面过程两种，一是使用多个select语句，每一步单独作为一个查询，
把前一步的返回结果用于本条select语句的where子句。

二是使用子查询，即直接在第一步的where子句中嵌套一个select语句

*/

#单步
#prod_id==>order_num
select order_num
from orderitems
where prod_id="TNT2";#返回结果order_num 200005,20007

#id order_num==>cust_id
select cust_id
from orders
where order_num in (20005,20007);#返回客户id 10001,1004

#cust_id==>cust_name,cust_contact
select cust_name,cust_contact
from customers
where cust_id in (10001,10004);


#子查询1 prod_id==>order_id=>cust_id
SELECT cust_id
from orders
where order_num in (select order_num
				    from orderitems
				    where prod_id="TNT2");
         #上述语句组合单步中的前两步，返回10001,10004

select cust_name,cust_contact
from customers
where cust_id in (10001,10004);

#子查询2  
select cust_name,cust_contact #order_num=>cust_id
from customers
where cust_id in (select cust_id #cust_id=>cust_name,cust_contact
                  from orders
				  where order_num in (select order_num ##prod_id=>order_num 
									  from orderitems
									  where prod_id ="TNT2"));
                 


#tips:单步实现过程就是按顺序一步一步进行，使用子查询时是自底向上的。
#避免多个子查询出现难以阅读，因此每一个子查询采用适当的缩进。
#where使用子查询时，应保证子查询的select列与当前where子句的列相同


#作为计算字段的子查询

/*
考虑案例
显示customers中每个客户的订单总数

1、从customers中提取客户列表
2、对于每个客户统计订单数目

*/

select count(*) as n_order
from orders
where cust_id=10004;#对某个特定用户的订单计数

#对每个客户统计订单数
select cust_name, (select count(*)
        from orders
        where orders.cust_id=customers.cust_id) as n_order
from customers
order by cust_name; 
/*
where使用完全限定名，比较orders表中的cust_id与当前正从customers表中检索的cust_id
n_order计算字段，由圆括号中的count(*)子查询建立，对每个检索出的客户执行一次。

通俗说，就是统计有订单的顾客的订单数目
*/

/*
select count(*)
from orders,customers
where orders.cust_id=customers.cust_id;
*/


#相关子查询：涉及外部查询的子查询
#用于两表中存在相同的列名

#上面案例，如果不使用完全限定名
select cust_name,(select count(*)
                  from orders
				  where cust_id=cust_id) as n_order
from customers
order by cust_name;    
#where cust_id=cust_id会让mysql认为仅在orders中的cust_id进行自身比较。              
#因为两个表中存在相同的列，造成歧义，返回错误的查询结果。


/*
子查询调试和查询调试时，首先建立并测试最内层的子查询，用子查询的结果
建立并测试外层查询，确认正常执行时嵌入子查询。
*/





