use crashcourse;

#创建和操纵表
/*
使用create table创建表，必须给出的信息:
1 新表的名字，在create table后给出
2 表列的名字和定义，逗号分隔

举例
create table customers
(cust_id int not null auto_increment,
 cust_name char(50) not null,
 cust_address char(50)  null,
 cust_city char(50)  null,
 cust_state char(5)  null,
 cust_zip char(10)  null,
 cust_country char(50)  null,
 primary key (cust_id))
 engine = InnoDB;
 
表中列的定义在圆括号中，每列定义以列名、数据类型。主键在创建表时用
primary key关键字指定

  auto_increment:本列每当增加一行时自动增量，每次执行一个Insert语句时
mysql自动对该列增量，给该列赋予下一个可用的值。

每个表只允许一个auto_increment列，且必须被索引

insert语句指定一个插入的值，如果该值唯一，则会被用来替代自动生成的值，
且后续的增量都在插入值上进行。

使用select last_insert_id()语句返回最后一个auto_increment值

*/

#举例
/*
create table orders
(order_num int not_null
 order_date datetime not null
 cust_id int not null
  primary key (order_num)
)engine=InnoDB;

创建表时，定义了3个not null的列，意味着不允许该列有NULL值，
将会阻止插入没有值的列，如果试图插入没有值的列，会报错。插入失败。

*/


#举例
/*
create table vendors
(vend_id int not null auto_increment,
 vend_name char(50) not null.
 vend_address char(50) null,
 vend_city char(50)  null,
 vend_state char(5)  null,
 vend_zip char(10)  null,
 vend_country char(50)  null,
 primary key (vend_id))
)engine = InnoDB;


上面例子中，vend_id,和vend_name指定not null,因此是必需的
其余的列定义为null,意为允许出现Null值，null为默认设置，如果不指定not null
默认定义为null.

tips：NULL值是没有值，不是空串。not null中允许有空串"",空串不是无值

*/

#表中每个行必须具有唯一的主键，主键使用单个列，则该列的值必须唯一
#主键使用多个列，则列的组合值必须唯一，且主键不允许有null值


#创建表时指定默认值
/*
create table orderitems
(order_num int not null,
 order_item int not null,
 prod_id char(10) not null,
 quantity int not null default 1.\,
 primary key (order_num,order_item)
)engine=InooDB;

default关键字指示mysql在未给出该列的值的情况下使用 1
mysql不允许函数作为默认值，只支持常量
尽可能使用默认值而不是null值


engine语句省略时使用默认引擎MyISAM,支持全文本搜索
常用的引擎：
InooDB：一个可靠的事务处理引擎，不支持全文本搜索
MEMORY：功能上等同于MyISAM，数据存储在内存中，速度快
MyISAM:性能很高，支持全文本搜索，不支持事务处理
tips:外键不能跨引擎，使用一个引擎的表不能引用使用不同引擎的表的外键
*/

#更新表alter table语句
#alter table后给出要更新的表名
#所做更改的列

alter  table vendors
add vend_phone char(20);
#上面语句给vendors表通过add关键字增加一个vend_phone的列，明确数据类型

alter table vendors
drop column vend_phone;
#上面语句通过drop columns删除刚刚增加的列

#alter定义外键
/*
alter table  orderitems
add constraint fk_oreritems_orders
foreign key (order_num) references orders(order_num);

alter table orderitems
add constraint fk_orderitems_products 
foreign key (prod_id) references products(prod_id);

alter table orders
add constraint fk_orders_customers
foreign key (cust_id) references customers(cust_id);

alter table products
add constraint fk_products_vendors 
foreign key (vend_id) references vendors(vend_id);

tips:alter table要慎重
*/

#删除表
drop table productnotes1;

#重命名表
/*
rename table b_customers to customers,
             b_vendors to vendors;
             
rename table后跟待修改的表名配合to关键字后跟替换的表名             
*/






