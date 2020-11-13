use crashcourse;

select count(*) as num_prods
from products
where vend_id=1003; #返回供应商1003提供的产品数目


select vend_id ,count(*) as num_prods
from products
group by vend_id; #按vend_id分组进行计算count(*)

/*
group by 指示mysql对每个组而不是整个结果集进行聚集 

1、group by子句可以包含任意数目的列，对分组进行嵌套
2、如果嵌套分组，数据将在最后规定的分组上汇总，
   意味着建立分组时指定的所有列都一起计算，不能从个别列访问数据。
3、group by子句列出的每个列都要是检索列或有效表达式，不能是聚集函数，
   如果在select中使用了表达式，则group by也要使用相同的表达式，不能是别名。 
4、除聚集函数外，select语句中的每个列必须在groupby子句中给出 。
5、分组列中有NULL值时，将NULL作为一个分组返回。列中有多个NULL值，则这些行分为一组。
6、group by出现在where语句之后，order语句之前。  

*/

select vend_id,count(*) as num_prods
from products
group by vend_id with rollup; #返回每个分组的值以及全部组的汇总


#过滤分组 having操作符

select cust_id,count(*) as n_order
from orders
group by cust_id
having count(*) >=2;#检索两个订单及以上的组

/*
having 支持where所有的操作符，句法相同，关键字差别。
having可以过滤分组，where是过滤特定行值。
差别：having是在分组之后进行过滤，而where是分组之前过滤。where排除的行不包括在分组中。

*/

select vend_id,count(*) as num_prods
from products
where prod_price>=10
group by vend_id
having count(*)>=2;
/*，
首先选出价格10以上的产品，按照供应商id分组，再返回2个以上产品的供应商
*/

#上述语句中没有where语句后
select vend_id,count(*) as num_prods
from products
group by vend_id
having count(*) >= 2;

/*
order by 和group by 的区别

1、order by 排序产生的输出 ；group by分组行，输出可能不是分组顺序\
2、order by对任意列都能使用(包括未选择的列)；
   group by只可能使用选择列或表达式，而且必须使用每个选择列表达式
3、order by不一定需要与聚集函数一起使用，
   group by如果与聚集函数一起使用列(表达式) ，则必须使用。
*/

select order_num,sum(item_price*quantity) as tot_price
from orderitems
group by order_num
having sum(item_price*quantity)>=50;
#having子句后不能跟计算字段的别名，必须使用表达式
#上面将返回订单总价大于等于50的订单编号和总订单价格
#返回结果的表中，是按订单编号顺序返回，订单总价乱序


select order_num,sum(item_price*quantity)  as tot_price
from orderitems
group by order_num
having sum(item_price*quantity)>=50
order by tot_price;
#最后一行order by 按订单总价排序
#将返回按订单总价顺序返回的分组结果

/*
子句排序
select     要返回的列或表达式     必须使用
from       从中检索数据的表       仅在从表中选择数据时使用
where      行级过滤             非必须 
group by   分组说明             仅在按组计算聚集时使用
having     组级过滤             非必须
order by   输出排序顺序          必须
limit      检索行数             非必须
*/











