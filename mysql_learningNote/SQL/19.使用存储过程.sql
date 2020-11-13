use crashcourse;

/*
存储过程： 为以后的使用而保存的一条或多条mysql语句的集合，
		 可视为批文件，但作用不仅限于批处理。

使用存储过程原因 
1 通过把处理封装在容易使用的单元中，简化复杂的操作 
2 由于不要求反复建立一系列处理步骤，保证数据完整性 
3 简化对变动的管理 
4 提高性能，使用存储过程比使用sql语句快 
5 存储过程可以使用那些只能用在单个请求中的mysql元素和特性来编写更强更灵活的代码 

缺陷
1、存储过程编写比sql语句复杂 
2、没有创建存储过程的安全访问权限  
*/

#创建存储过程
delimiter //
create procedure productprice()
begin
    select avg(prod_price) as avg_price
    from products;
end //
delimiter ;  
/*
1  使用delimiter指定//作为新的分隔符
2  关键词create procedure创建存储过程，存储过程可能带有参数因此
   在存储过程后加圆括号  
3  begin和end 语句用来限定存储过程体。过程体本身仅是一个简单的select语句

4  过程体中的select语句以;为select语句的结束符，
   并非整个创建存储过程的结束符。
5  end语句标志着创建过程的结束，需要使用前面定义的//结束符 
6  为方便后续使用，使用delimiter语句将结束符重新恢复为 ; 结束符  
*/

#使用存储过程
call productprice();
#call语句调用创建的存储过程函数，需要带括号

#删除存储过程
drop procedure productprice;
#drop procedure procedurename 注意这里不需要带括号

#使用参数
delimiter //
create procedure productprice(
    out p1 decimal(8,2),
    out p2 decimal(8,2),
    out p3 decimal(8,2)
)
begin
    select min(prod_price)
    into p1
    from products;
    select max(prod_price)
    into p2
    from products;
    select avg(prod_price)
    into p3
    from products;
end //
delimiter ;  
/*
创建带参数的productprice存储过程
参数分别为p1,p2,p3,关键字out指出相应参数从存储过程传出一个值
每个参数必须具有指定的类型，decimal为十进制，(8,2)为存储8位数包含两位小数  
过程体中，关键字into意为将值保存到相应的变量    
*/

#调用上面的存储过程 
call productprice(
     @pricelow,
     @pricehigh,
     @priceavg); 
#变量名必须以@开始     

#检索平均价格
select @priceavg;
#检索最小最大和平均
select @pricelow,@pricehigh,@priceavg;


#创建ordertotal存储过程，接受订单号返回订单合计
delimiter //
create procedure ordertotal(
	in onumber int,
    out ototal decimal(8,2)
)
begin 
    select sum(item_price*quantity)
    from orderitems
    where order_num = onumber
    into ototal;
end //
delimiter ;    
#创建存储过程语句中，参数onumber前面的关键字in,意为该参数要存入存储过程
#ototal参数前的out关键词，意为要从存储过程返回合计
#where子句选择需要计算合计的行
#into将合计保存到ototal变量

#调用上面存储过程
call ordertotal(20005,@tot);
#这里必须传递两个参数，订单号和包含计算合计值的变量名

#显示合计
select @tot; #与call中传递的参数名一致才可以显示

#检索订单号20009的订单合计
call ordertotal(20009,@tot);
select @tot;

#业务场景：获得与以前一样的订单合计，需要对合计附加营业税，只针对某些顾客
/*
上面场景分成以下几步
1 获得合计，与以前一样
2 把营业税有条件添加到合计
3 返回合计（带或不带税）
*/
#上面业务的存储过程为
delimiter //
create procedure ordertotal0(
     in onumber int,
     in taxable boolean,
     out otot decimal(8,2)
) comment 'obtain order total,optionally add tax'
begin 
    -- declare variable total and taxrate
    declare total decimal(8,2);
    declare taxrate int default 6;
    -- get order total
    select sum(item_price*quantity)
    from orderitems
    where order_num = onumber
    into total;
    -- is taxable
    if taxable then
        -- yes,add tax rate to total
        select total+(total/100 * taxrate) into total;
    end if;
    -- save to out variable
    select total into otot;
end //
delimiter ;    
/*
1 创建ordertotal存储过程，指定两个传入存储过程的参数,
  整型onumber(订单编号)，布尔型taxable（是否带税）
2 comment关键字，如果给出则会在show procedure status中显示
3 过程体中，使用 --加空格添加注释。declare语句定义了两个局部变量，
  total十进制的两位小数，税率taxrate整型，取百分号前面的数字，默认值为6

4 select语句中将计算的合计值存放在局部变量total中，进行是否含税的判断，
  if taxable 意为条件为真，即含税状况，then select语句计算含税时合计值的计算公式，
  并将结果保存到total，end if语句标志if语句的结束
5 最后再将局部变量的结果total保存到定义的全局变量otot中。 
*/
#使用上述存储过程
call ordertotal0(20005,0,@tot);
select @tot;#taxable为0意味着条件为假，即不含税时

call ordertotal0(20005,1,@tot);
select @tot;

/*
if语句条件为真使用then子句进行真条件下的操作，如果存在不为真
时的其他操作，可以使用else子句，注意else子句不跟then关键字，
而是直接给出操作的语句。

如果if语句为假还需进行进一步条件判断的话，使用elseif子句，如果elseif
子句为真仍使用then子句。
*/

#检查存储过程
show create procedure ordertotal0;

show procedure status;#列出全部的存储过程列表
show procedure status like 'ordertotal0';