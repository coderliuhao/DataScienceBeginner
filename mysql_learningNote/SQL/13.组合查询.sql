use crashcourse;

#组合查询
#1 在单个查询中从不同表返回类似结构的数据
#2 对单个表执行多个查询，按单个查询返回数据

/*
考虑案例
需要价格小于等于5的所有物品的一个列表;而且包括供应商1001和1002生产的所有物品。
*/

#多条select组合实现
select prod_id,vend_id,prod_price
from products
where prod_price<=5;
#上述语句找到价格小于5 的所有产品 返回4条数据
select vend_id,prod_id,prod_price
from products
where vend_id in (1002,1001);
#上述语句找到供应商1002,1001的所有产品  返回5条数据
#总行数9

#组合上面两个语句
select vend_id,prod_id,prod_price
from products
where prod_price<=5
union
select vend_id,prod_id,prod_price
from products
where vend_id in (1001,1002);
#返回的结果既包含价格小于等于5的产品，也包含仅由1001,1002生产的所有物品
#返回结果8行，因为有一条1002供货商的产品价格小于5是重复数据，在union时被去除。

#等价的where子句写法
select vend_id,prod_id,prod_price
from products
where prod_price<=5 or vend_id in (1001,1002);
#多个where条件返回的结果与union结果相同，说明union可以由多个where条件完成相同的工作。

/*
union规则：
1  union由两个及以上的select语句组成，语句之间用关键字union分割
2  union中每个查询必须包含相同的列，表达式或聚集函数
3  列数据类型必须兼容
*/

#union有自动去除重复行的作用，如果需要保留重复行的结果时：

select vend_id,prod_id,prod_price
from products
where prod_price <=5
union all
select vend_id,prod_price,prod_id
from products
where vend_id in (1001,1002);
#使用union all关键字可以完全保留两部分的返回结果 包含9条数据。
#where子句无法完成union all的工作


#组合查询结果排序

select vend_id,prod_id,prod_price
from products
where prod_price <=5
union
select vend_id,prod_id,prod_price
from products
where vend_id in (1001,1002)
order by vend_id,prod_price;
#order by对所有的select语句返回的结果排序

#tips:使用unioin组合查询时，可以应用于不同的表








