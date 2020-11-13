/*
1 mysql安全服务基础：用户不能对过多的数据具有过多的访问权
2 访问控制：给用户提供他们所需的访问权，且仅提供他们所需的访问权，管理访问控制需要创建和管理用户账号
3 现实世界或者日常工作中绝不能使用root
4 访问控制有助于避免在不合适的数据库操作或其他一些用户错误，通过保证用户不能执行
  他们不应该执行的语句
  
*/
#管理用户 
use mysql;
select user from user; 

create user liuhao IDENTIFIED BY '@Liuhao123';
#创建新用户liuhao,密码为@Liuhao123
use mysql;
select user from user; 
#测试是否创建成功
rename USER liuhao to LIUHAO;
#重命名用户名
use mysql;
select user from user; 

drop user LIUHAO;
#删除用户
USE mysql;
SELECT USER FROM user;

show grants for liuhao;
#usage表示根本没有权限
#结果表示在任意数据库和任意表上对任何东西没有权限
/*
1 用户定义为user@host,mysql的权限用用户名和主机名结合定义。如果不指定主机名
  则使用默认的主机名%
2 设置权限使用grant语句时给出以下信息
  要授予的权限
  被授予访问权限的数据库或表
  用户名
*/

grant select on crashcourse.* to liuhao;  
#grant语句允许用户在crashcourse数据库的所有表上使用select,由于只 授予select访问权限，
#用户liuhao对crashcourse数据库中的所有数据只有只读访问权限 

show grants for liuhao; 
#结果中将出现上面的只读权限

revoke select on crashcourse.* from liuhao;  
#revoke是 grant的逆操作，用来撤销权限，需要提供的信息与grant语句相同
show grants for liuhao;  

/*
grant和revoke可在几个层次上控制访问权限
1 整个服务器，使用grant all 和revoke all
2 整个数据库，使用on database.*
3 特定表，使用on database.table
4 特定的列
5 特定的存储过程

tips：可通过列出各权限并用逗号分隔，将多条grant语句串在一起
     grant select,insert on crashcourse.* to liuhao
*/

#更改口令（密码）
SET PASSWORD FOR  liuhao  = Password('Liuhao123@');
#指定用户更改密码
SET PASSWORD = Password(new_password)
#上面语句将更新当前用户密码
  
  