USE crashcourse;

select prod_name
from products;#检索出的数据按照底层表中出现的顺序显示
/*
    关系数据库设计理论认为，如果不明确规定排序顺序，
则不应该假定检索出的数据的顺序有意义。
*/

#子句 由关键字和所提供的数据组成

select prod_name
from products
order by prod_name; #默认升序，字母表顺序a-z,或者是数值升序
#order by 也可以选择非检索的列排序数据

select prod_id,prod_price,prod_name
from products
order by prod_price,prod_name;#按多个列排序
/*先按price排序，且仅在price相同时，按prod_name排序，
 意味着当price中所有值都是唯一的时，不会按照name排序。
*/

select prod_id,prod_price,prod_name
from products
order by prod_price desc; #desc关键字降序排序

select prod_id,prod_price,prod_name
from products
order by prod_price desc,prod_name#desc只作用于位于其前面的列名，不指定desc时默认升序排序

#如果要对多个列降序排序，则需要在每个列后指定desc关键字

select prod_price
from products
order by prod_price desc
limit 1; #order by 和limit结合可以找出某列的最大或最小值，
	     # 且limit在必须order by之后


