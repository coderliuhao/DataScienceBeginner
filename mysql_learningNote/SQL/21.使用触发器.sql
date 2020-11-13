use crashcourse;

/*
触发器是mysql响应以下任意语句而自动执行的一条mysql语句，
或者begin和end之间的一组语句。

delete
insert
update
其他语句不支持触发器
*/

/*
创建触发器需要:
1 唯一的触发器名
2 触发器关联的表
3 触发器应该响应的活动(delete,insert,updatae)
4 触发器何时执行(处理之前或之后)

tips:1 触发器名必须在每个表中唯一，但不是在每个数据库唯一
     2 只有表支持触发器，视图不支持
     3 每个表每个事件每次只允许一个触发器，意味着每个表最多
	   6个触发器，分别是delete,update,insert操作的之前和之后
     4 单一触发器不能与多个事件或多个表关联
*/

#创建触发器
create trigger newproduct after insert on products
for each row select 'product added' into @q1;

/*
create trigger创建名为newproduct的触发器，
after insert关键词意味着触发器将在插入操作成功执行之后执行，
on意为在哪张表上创建触发器，for each row意味着代码对每个插入行执行，
执行的操作为对每个插入行显示一次product added
*/

#删除触发器
drop trigger newproduct;
#触发器不能更新和覆盖，修改一个触发器必须先删除再新建

#使用触发器

#1 insert触发器
/*
1 insert触发器代码内，可引用一个名为new的虚拟表，访问被插入的行
2 在before insert触发器中，new中的值也可以更新
3 对于auto_increment的列，new在insert执行之前包含0，在insert
  执行之后包含新的自动生成的值
*/

create trigger neworder after insert on orders
for each row select new.order_num into @val;
#new关键字创建虚拟表
/*
插入一个新订单到orders表中时，mysql生成一个新的订单号保存到order_num
中。触发器从new.order_num取得这个值并返回它，由于在插入新的新单之前order_num
还没生成，因此使用after insert触发器。对orders使用该触发器将总是返回新的订单号。

先将结果存放在变量中，再插入数据执行触发器之后，查看该变量里的值
*/
#测试触发器
insert into orders(order_date,cust_id)
values(now(),10001);
select @val;

#2 delete触发器
/*
1 delete触发器代码内，可引用old的虚拟表，访问被删除的行
2 old中的值都是只读，不可更新
*/
delimiter //
create trigger deleteorder before  delete on orders
for each row
begin
    insert into archives_orders(order_num,order_date,cust_id)
    values(old.order_num,old.order_date,old.cust_id);
end //
delimiter ;    
/*
1 任意订单被删除前执行此触发器
2 insert语句将old中的值保存到archives_orders的表中，archives表的列
  与orders相同
  
tips:触发器中使用的begin end语句并非必须，但是begin end语句使触发器能
     容纳更多的sql语句。这些语句都在begin end 语句之间
*/

#3 update触发器
/*
1 update触发器代码中 ，可以引用一个old的虚拟表访问update执行前的数据，
  也可以引用一个new的虚拟表访问update执行之后的值

2 before update触发器中，new中的值可能也被更新，允许更改将要用于update中的值
3 old中的值不能更新。
*/

create trigger updatevendor before update on vendors
for each row set new.vend_state = upper(new.vend_state);
#更新每一行时，new.vend_state的值都用upper(new.vend_id)替代

#MORE
/*
1 创建触发器可能需要一定的安全访问权限。触发器的执行是自动的，
  如果insert、update或delete语句能够执行，则相关触发器也能执行
2 应用触发器保持数据的一致性
3 使用触发器把更改记录到另一个表非常容易
4 触发器不支持call语句，意味着不能从触发器调用存储过程，所需的存储过程代码
  需要复制到触发器内。
*/
