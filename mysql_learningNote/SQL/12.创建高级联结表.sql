use crashcourse;

#使用表别名,缩短sql语句，便于复用同一表
select concat(rtrim(vend_name),"(",rtrim(vend_country), ")") as vend_NC
from vendors
order by vend_name;


select cust_name,cust_contact
from customers as c,orders as o,orderitems as oi
where c.cust_id = o.cust_id
and   o.order_num = oi.order_num
and   prod_id="TNT2";
#给三个表赋予别名，方便简写表名。且表表别名不返回客户机
#别名可以出现在select,from,order by子句以及语句的其他部分


#自联结：同一表中的联结
/*
 考虑案例:
 已知某物品id为DTNTR存在问题，必然来自某供应商，
现在要检查该供应商生产的其他产品是否有问题
 */

#方法1 子查询，先根据产品id找供应商，在按供应商检索其他产品
select prod_id,prod_name
from products
where vend_id in (select vend_id
                  from products
                  where prod_id ="DTNTR");

#方法2 联结表
select p2.prod_id,p2.prod_name
from products as p1,products as p2
where p1.vend_id = p2.vend_id #匹配两个表的vend_id
and p1.prod_id = "DTNTR";
#from给products赋予两次别名，第一次为p1,第二次为p2。
#select必须指定列的来源，因为完全相同的表具有重复列。
#当select选择了其中一个表(p2)的列，那么在条件过滤时，要使用另一表的列(p2)进行过滤。

#处理联结的效率高于处理子查询


#自然联结，每个列只返回一次
select c.*,o.order_num,o.order_date,oi.prod_id,oi.quantity,oi.item_price
from customers as c,orders as o,orderitems as oi
where c.cust_id = o.cust_id
and   o.order_num = oi.order_num
and   prod_id="FB";
#通配符*对c列使用，意味着选取c的全部列，后面都是明确列出的列，没有重复列被检测出



/*
外部联结：许多联结将一个表中的行与另一个表中的行相关联。但
有时候会需要包含没有关联行的那些行。
*/

select c.cust_id,o.order_num
from customers as c inner join orders as o
on c.cust_id = o.cust_id;
#以上为内部联结，检索所有客户和订单号


#外部联结
select c.cust_id,o.order_num
from customers as c left outer join orders as o
on c.cust_id = o.cust_id;
/*
  1、关键字outer join 指定联结类型为外部联结，结果中包含没有匹配的行
  2、指定了outer join时必须使用left或者right指定包含全部行的表，
  3、上面代码中left指的是outer join左边的customers表，意味着从customers
选择所有行。

*/
select c.cust_id,o.order_num
from customers as c right outer join orders as o
on c.cust_id = o.cust_id;
#从右边的orders表中选择所有行



#带聚集函数的联结

/*
考虑案例
检索所有客户及每个客户所下订单数
*/
select c.cust_name,c.cust_id,count(o.order_num) as n_order
from customers as c inner join orders as o
on c.cust_id = o.cust_id
group by c.cust_id;
/*
inner join将customers和orders联结，group by按客户分组数据，
调用count()对每个客户的订单计数，返回n_order
*/


select c.cust_name,c.cust_id,count(o.order_num) as n_order
from customers as c left outer join orders as o
on c.cust_id = o.cust_id
group by c.cust_id;
#外部联结，使用左边的customers表的全部行，返回没有下过订单的mouse house.

/*
tips: 一般使用内部联结，外部联结也有效
      保证使用正确的联结条件，否则返回不正确的数据
      总是提供联结条件，避免出现笛卡尔积
	  一个联结可以包含多个表，每个联结可以使用不同的联结类型。
*/

      