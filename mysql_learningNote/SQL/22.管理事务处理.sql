use crashcourse;

/*
1 事务处理是一种机制，用来管理必须成批执行的mysql操作，以保证数据库不包含
  不完整的操作结果。
2 利用事务处理可以保证一组操作不会中途停止，或者作为整体执行，或者完全不执行
3 如果没有错误发生，整组语句提交给数据表，如果发生错误，进行回退以恢复数据库到某个
  已知且安全的状态
  
事务处理的关键术语: 
1 事务(transaction)指一组SQL语句
2 回退(roolback)指撤销指定sql语句的过程
3 提交(commit)指将未存储的sql语句结果写入数据库表
4 保留点(savepoint)指事务处理中设置的临时占位符(placeholder),
  可以对它发布回退(注意这里的回退与回退整个事务不同)
*/

#控制事务处理(使用start transaction标识事务开始)

#使用rollback
-- 显示该表不为空
select * from ordertotals;
-- 开始事务处理
start transaction;
-- 删除这个表中所有行
delete from ordertotals;
-- 验证表为空
select * from ordertotals;
-- 使用回退，回退start transaction后的所有语句
rollback;
-- 验证回退的效果，即表不为空
select * from ordertotals;
#rollback只能在一个事务处理内使用
#事务处理用来管理insert,update,delete语句
#事务处理不能回退select语句
#不能回退create语句和drop语句，即使在事务处理中使用，也不会被撤销

#使用commit
start transaction;
delete from orderitems where order_num= 20010;
delete from orders where order_num = 20010;
commit;
/*
1 上面代码会删除两表中order_num为20010的订单信息，由于涉及两个表，使用事务处理块
保证订单不被部分删除
2 只有删除操作都不出错时，执行commit语句。其中一条delete出错都不会提交更改。


tips 当rollback和commit语句执行后，意味着事务处理被自动关闭
*/

/*
使用保留点
保留点是为了支持回退部分事务处理在事务处理块中合适位置放置的占位符，回退时可以回退到某个占位符

使用savepoint语句创建占位符
*/
savepoint delete1;
#每个保留点取唯一标识的名字，方便回退时告知mysql回退到何处
rollback delete1;#回退到刚才的保留点
/*
1 保留点越多越好，回退时更灵活
2 保留点在事务处理完成(执行一条rollback或commit语句)后自动释放，
  也可以用release savepoint明确释放保留点
*/
  
#更改默认提交行为:指示mysql不自动提交更改
set autocommit = 0;
#autocommit标志决定是否自动提交更改，不论是否有commit语句
#autocommit = 0意味着不自动提交

#autocommit标志是针对每个连接而不是服务器的













