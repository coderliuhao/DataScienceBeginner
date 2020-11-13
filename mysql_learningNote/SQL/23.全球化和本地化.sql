use crashcourse;

#字符集:字母和符号的集合
#编码：某个字符集成员的内部表示
#校对：规定字符如何比较的指令

#使用字符集和校对顺序

show collation;
#可显示所有的校对以及适用的字符集

show VARIABLES LIKE 'character%';
SHOW VARIABLES LIKE 'collation%';
#上面代码可确定所用字符集和校对

#给表指定字符集和校对
CREATE TABLE mytable
(col1 INT,
 col2 VARCHAR(10))
DEFAULT CHARACTER SET hebrew
COLLATE hebrew_general_ci；
/*
1 如果指定CHARACTER SET和COLLATE,则使用这些值
2 如果指指定CHARACTER SET,则使用此字符集及其默认校对
3 如果既不指定CHARACTER SET 也不指定COLLATE，使用数据库默认  
*/

#为每个列设置字符集和校对 
CREATE TABLE mytable1
(col1  int,
 col2 VARCHAR(10),
 col3 VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_general_ci
)DEFAULT CHARACTER SET hebrew
COLLATE hebrew_general_ci;
#这里只对col3指定字符集和校对

select * FROM customers
order by lastname,firstname COLLATE latin1_general_cs;
#select语句使用collate指定一个备用的校对顺序
#可用来进行区分大小写搜索
#collate还可以在group by、having、聚集函数、别名等中使用

#tips 使用cast函数和convert函数可以使串在字符集之间校对






    