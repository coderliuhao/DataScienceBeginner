use crashcourse;

/*
全文本搜索
在使用全文本搜索时， MySQL不需要分别查看每个行，不需要分别分析和处理
每个词。 MySQL创建指定列中各词的一个索引，搜索可以针对这些词进行。
*/

#创建表时启用全文本搜索。

create table productnotes1
(
note_id    int          not null auto_increment,
prod_id    char(10)     not null,
note_date  datetime     not null,
note_text  text         null,
primary key(note_id),
fulltext(note_text) #fulltext将索引note_text单列
)
engine=MyISAM;

select note_text
from productnotes
where match(note_text) against("rabbit");
#match指定被搜索的列，against指定使用的搜索表达式
#返回包含rabbit的行
/*
match()中传递的列，必须是fulltext定义过的MyISAM类型，
如果指定多列则必须按照定义时的顺序列出。搜索不区分大小写。
*/

#上面语句的like实现
select note_text
from productnotes
where note_text like "%rabbit%";

/*
like在匹配时，返回的行并非总是有序的。而全局文本搜索会按照匹配的良好程度
排序返回。从返回的结果来看，一条记录中的rabbit出现在第3个词，另一条记录中的rabbit
出现在第20词，所以认为排名第三的rabbit比第20的rabbit的行等级高，因此
具有较高等级的行先返回。
*/

select note_text,match(note_text) against("rabbit") as rank
from productnotes;
#上面语句中，将match() against() 创建计算字段rank
#由于没有where子句过滤，上面语句将返回note_text的所有行
#返回的rank值越大，意味着rabbit在行中越靠前。
#如果同时全文本搜索多个词，那么匹配词越多的行比匹配词少的等级高



#使用查询扩展：除了找到包含某单词的行外，还要找到可能与搜索有关的其他行

/*
查询扩展过程：
1 先基本全文本搜索，找出与搜索条件匹配的所有行
2 mysql检查这些匹配的行并选择所有有用的词
3 mysql再次全局搜索，使用开始的搜索条件与所有有用的词。
*/


#step1 简单全文本搜索
select note_text
from productnotes
where match(note_text) against("anvils");
#返回一行包含anvils的数据

#step2,3
select note_text
from productnotes
where match(note_text) against("anvils" with query expansion);
#按等级返回7行数据，第二行包含第一行的两个词customer和recommend
#with query expansion 查询扩展操作符
#表中行越多，查询扩展的结果就越好


#布尔文本搜索：全文本搜索的布尔方式
/*
将返回以下内容
1 要匹配的词
2 要排斥的词
3 排列提示
4 表达式分组
5 其他
*/
#tips:布尔方式即使没有全文本搜索定义时也能使用

select note_text
from productnotes
where match(note_text) against("heavy" in boolean mode);
#in boolean mode布尔模式的全文本搜索，查找"heavy"且没有指定任何布尔操作符 

#匹配包含heavy且不包含任意以rope开始的词所在的行
select note_text
from productnotes
where match(note_text) against("heavy -rope*" in boolean mode);
#against中的 -rope*意为排除以rope为开头(包括ropes）的词所在的行

/*
全文本布尔操作符
+   必须存在
-   排除，必须不出现
>   包含且增加等级值
<   包含且减少等级值
()  把词组成子表达式
~   取消一个词的排序值
*   词尾通配符
""  定义一个短语(用于对匹配的短语进行操作)
*/

select note_text
from productnotes
where match(note_text) against('+rabbit + bait' in boolean mode);
#将搜索包含rabbit和bait的行

select note_text
from productnotes
where match(note_text)against('rabbit bait' in boolean mode);
#没指定任何操作符，将搜索包含rabbit或者bait的行

select note_text
from productnotes
where match(note_text)against('"rabbit bait"' in boolean mode);
#将搜索包含rabbit bait短语的行

select note_text
from productnotes
where match(note_text)against('>rabbit <carrot' in boolean mode);
#匹配rabbit和carrot增加rabbit的等级，降低carrot的等级

select note_text
from productnotes
where match(note_text)against('+safe +(<combination)' in boolean mode)
#搜索包含safe和combination的词，降低combiantion的等级

/*
全文本搜索说明:
1 索引全文本数据时，短词(3个或3个以下的词)被忽略且从索引中排除
2 mysql中的内建非用词列表，这些词在索引全文本时总被忽略，必要时可以覆盖
3 许多词出现频率很高，意味着返回太多结果，所以搜索它们意义不大。如果一个词出现频率
  超过50%以上的行中，将它作为非用词忽略，50%规则不用于in boolean mode
4 表中行数小于3行，全文本搜索不返回结果(50%原则)
5 忽略词中的d单引号。don't索引为dont
6 不具有词分隔符的语言不能恰当返回全文本搜索结果  
7 仅在MyISAM数据库引擎中支持全文本搜素
*/


