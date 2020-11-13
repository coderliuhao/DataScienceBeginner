use crashcourse;

#使用游标
/*
游标（cursor）是一个存储在MYSQL服务器上的数据库查询，它不是select语句，
而是被该语句检索出来的结果集。在存储了游标之后，应用程序可以根据需要
滚动或浏览其中的数据。

使用游标原因：在检索出来的行中前进或者后退一行或多行

mysql游标只能用于存储过程和函数

游标主要用于交互式应用，其中用户需要滚动屏幕上的数据，并对数据进行浏览或作出更改
*/

#使用游标的步骤
/*
1 在能够使用游标前，必须声明它。这一过程实际没有检索数据，
  只是定义要使用的select语句
2 一旦声明后，必须打开游标以供使用。这个过程用前面定义的select语句把数据实际检索出来 
3 对于填有数据的游标，会根据需要取出各行 
4 结束游标使用时，必须关闭游标
*/

#使用declare创建游标
#定义游标检索所有订单的select语句
delimiter //
create procedure processorders0()
begin 
declare ordernumbers cursor
for
select order_num from orders;

-- open cursor
open ordernumbers;

-- close cursor
close ordernumbers;
end //
delimiter ;
#declare声明游标名为ordernumbers
#cursor for为游标定义要使用的select语句 
#定义游标之后，使用open cursorname打开游标
#close cursorname语句可以关闭游标，如果不明确关闭，则执行到end语句时自动关闭
#存储过程处理完后，游标就会消失

#使用游标数据
#游标被打开后，使用fetch语句分别访问它的每一行
#fetch指定检索什么数据，检索出来的数据存储在哪里
#fetch向前移动游标中的内部行指针，使吓一跳fetch语句检索下一行（不重复读取同一行）

#案例1 从游标中检索第一行
drop procedure processorders;
delimiter //
create procedure processorders()
begin
    declare o int;
    declare ordernumbers cursor for
    select order_num from orders;
    
    open ordernumbers;
    
    fetch ordernumbers into o;
    
    close ordernumbers;
end//
delimiter ;  
#fetch检索order_num第一行保存到局部变量o中，对数据不作任何处理

#循环检索数据，从第一行到最后一行
drop procedure processorders0;
delimiter //
create procedure processorders0()
begin
    -- 定义局部变量
    declare done boolean default 0;
    declare o int;
    -- 声明游标
    declare ordernumbers cursor
    for
    select order_nums from orders;
    -- 定义continue handler
    declare continue handler for sqlstate '02000' set done =1;
    
    open ordernumbers;
    -- 循环所有行
    repeat
         -- get ordernumber
         fetch ordernumbers into o;
    -- 循环停止     
    until done end repeat; 
    -- 关闭游标
    close ordernumbers;
end //
delimiter ;
    
/*
1 声明局部变量done,用来描述游标结束的标志位
  声明局部变量o
2 声明游标来检索order_num列
3 continue handler语句，意为条件发生时继续执行的代码，
  当sqlstate=‘02000’，错误码02000表示未找到条件。
  未找到条件放在代码中即cursor未找到时，set语句把标志位done设置为1，即游标结束
4 打开游标
5 fetch操作在repeat 语句中，意味着会反复执行读取行的操作
6 until done end repeat.重复终止条件，直到done=1时停止重复
*/

#   tips:declare定义局部变量必须定义游标或句柄之前，
#   句柄即fetch操作必须在游标之后定义。


#完整示例
delimiter //
create procedure processororderr01()
begin
   -- 声明局部变量 
   declare done boolean default 0;
   declare o int;
   declare t decimal(8,2);
   
   -- 声明游标
   declare ordernumbers cursor
   for 
   select order_num from orders;
   
   declare continue handler for sqlstate '02000' set done=1;
   
   -- 创建表存放结果数据
   create table if not exists ordertotals
   (order_num int,total decimal(8,2));
   
   -- 打开游标
   open ordernumbers;
   
   REPEAT
      -- 句柄，获取order_num
       fetch ordernumbers into o;
       -- 调用之前创建的存储过程，计算含税的订单总计
       call ordertotal0(o,1,t);
       -- 把结果插入到存放结果的表
       insert into ordertotals(order_num,total)
       values(o,t);
       
	until done end repeat;
	close ordernumbers;
end //
delimiter ;      
/*
1 新增了局部变量t，存储每个订单合计
2 创建了用于存放结果的新表ordertotals,包含两列，订单编号和总计
3 repeat中重复读取行，然后调用之前计算带税合计的存储过程计算每个订单合计值，
  存储过程中是吧合计值存放在t中
4 把结果插入到新建的表中，保存每个订单的订单号和合计
*/

#上述过程创建并填充了新表
call processororderr01();
select *
from ordertotals;





  


