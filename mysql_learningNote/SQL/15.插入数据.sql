use crashcourse;

#插入数据语句insert
insert into customers
values( Null,
        'Pep E.LaPew',
        '100 Main Street',
        'Los Angles',
        'CA',
        '90046',
        'USA',
         NUll,
         Null);
#上面语句在customers表中插入了一个新的客户，包含对应列的信息，有些列为空值         
#插入语句一般不会产生输出。而且必须按照列的顺序填充信息。

#上面语句的更安全的写法
insert into customers(cust_name,
					  cust_address,
                      cust_city,
                      cust_state,
                      cust_zip,
                      cust_country,
                      cust_contact,
                      cust_email)
values('Pep E.LaPew',
        '100 Main Street',
        'Los Angles',
        'CA',
        '90046',
        'USA',
         NUll,
         Null);
/*         
1 上面语句将values值填充到表中的对应项
2 如果不需要为某列赋值，则不必在表中声明该列，
  作为省略的列处理:允许NUll,或者不给值时使用默认值。
3 表中声明需要插入值的列时不必严格按表中列的顺序列出，
  只需要将value与声明的列对应即可。
*/

insert into customers(cust_name,
                      cust_contact,
					  cust_email,
                      cust_address,
                      cust_city,
                      cust_state,
                      cust_zip,
                      cust_country)
values('Pep E.LaPew',
		NUll,
        NUll,
        '100 Main Street',
        'Los Angles',
        'CA',
        '90046',
        'USA'
        ) ;
        
        
#tips:向表中插入数据时，如果不声明列名，则需要按次序给出表中每列插入的值

#插入多行
#写法1
insert into customers(cust_name,
                      cust_address,
                      cust_city,
					  cust_state,
					  cust_zip,
                      cust_country)
values( 'Pep E.LaPew',
        '100 Main Street',
        'Los Angles',
        'CA',
        '90046',
        'USA'); 
insert into customers(cust_name,
                      cust_address,
                      cust_city,
					  cust_state,
					  cust_zip,
                      cust_country)
values('M.Martin',
       '42 Galaxy Way',
       'New York',
       'NY',
       '11213',
       'USA');     
       
#写法2
insert into customers(cust_name,
                      cust_address,
                      cust_city,
                      cust_state,
                      cust_zip,
                      cust_country)
values('M.Martin',
       '42 Galaxy Way',
       'New York',
       'NY',
       '11213',
       'USA'),
       ('M.Martin',
       '42 Galaxy Way',
       'New York',
       'NY',
       '11213',
       'USA');
       
#当单条insert有多组值插入时，每组值用一个括号即可。单条insert比多条提高mysql处理性能


#插入检索出的数据
/*
create table custnew(
     cust_id int unsigned auto_increment,
     cust_name varchar(11) not null,
     cust_address varchar(11) not null,
     cust_city varchar(11) not null,
     cust_state varchar(11) not null,
     cust_zip varchar(11) not null,
     cust_country varchar(11) not null,
     cust_contact varchar(11) not null,
     cust_email varchar(11) not null,
	 primary key (cust_id))
	 engine = InnoDB;
*/

insert into customers(cust_id,
                      cust_contact,
                      cust_email,
                      cust_name,
                      cust_address,
                      cust_city,
                      cust_state,
                      cust_zip,
                      cust_country)
select cust_id,
	   cust_contact,
		cust_email,
		cust_name,
		cust_address,
		cust_city,
		cust_state,
		cust_zip,
		cust_country
from custnew;

#使用insert select从custnew中对应的列数据导入customers
        


