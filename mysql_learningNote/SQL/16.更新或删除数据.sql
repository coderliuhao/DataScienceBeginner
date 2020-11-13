use crashcourse;

#更新和删除数据update子句
/*
update子句由三部分组成
1 要更新的表
2 列名和他们的新值
3 确定要更新行的过滤条件
*/

update customers
set cust_email = 'elmer@google.com'
where cust_id=10005;
#update子句选择需要更新的表
#set子句选择修改的列名和要更新的值
#where子句确定要更新的行
#update子句以where子句为结束


#更新多列
update customers
set cust_name='the fudds',
	cust_email='elmer@google.com'
where cust_id=10005;    
#修改多个列时，只需要在set子句后面增加要更新的列和值，逗号连接

#update中可以使用子查询，出现在set中可以用子句的返回值更新列的值
#出现在where子句中可以根据子查询的条件检索行进行列更新

#当使用update更新多行数据时，如果其中一行出错，则不能正常执行update
#如果不论是否发生错误也要执行update,需要在update后加ignore

update customers
set cust_email= Null
where cust_id = 10005;
#上面操作通过将列更新为Null来删除10005号客户的email值

#删除数据delete关键词
/*
1 从表中删除特定的行
2 从表中删除所有行
*/

delete from customers
where cust_id = 10006;
#delete from要求指定从中删除数据的表名
#where表名要删除的行，只删除客户10006，如果省略where子句，则删除所有客户

/*
tips:
1 删除整行用delete语句，删除整列用update语句
2 delete从表中删除行，甚至删除表中所有行，但是不能删除表本身
3 如果想要删除全部行，不必使用delete语句，
  替代方案是使用truncate table实现，因为它效率更高。

*/

/*
good habits

1 除非确定更新或者删除每一行，否则绝对不使用缺
  少where子句的updat和delete语句 
2 保证每个表都有主键，在where中通常指定主键值过滤行
3 在对update或delete使用where过滤条件之前，
  先用selet测试是否是正确的记录，以防where出错 
4 使用强制实施引用完整性的数据库
5 mysql没有撤销键，operate carefully

















