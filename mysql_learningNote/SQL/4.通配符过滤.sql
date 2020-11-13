use crashcourse;

select prod_id,prod_name
from products
where prod_name like "jet%";#找出所有以jet为开头的产品

/*
like操作符 指示mysql后跟的搜索模式利用通配符匹配而不是直接相等匹配进行比较。
严格意义上 like是谓词。

%通配符：表示任何字符出现任意次数，包括0次。它告诉mysql接受jet之后的任意字符
在使用通配符匹配时，待匹配的字符区分大小写，即小写字符不能匹配大写的值。
*/

select prod_id,prod_name
from products
where prod_name like "%anvil%";#使用两个%位于模式的两端

#  两端带%通配符的模式，表示匹配任何位置包含中间文本的值

select prod_name
from products
where prod_name like "s%e";#匹配以s开头，以e结尾的产品名字


select prod_name
from products
where prod_name like "%";#返回全部行

#说明 %也能匹配0个字符，意味着返回全部的行，但是不能匹配带null的行

/*匹配模式中的尾空格会影响通配符匹配，
"%anvil"将不会匹配到尾部带空格的保存词,有效的解决办法是在搜索模式后加一个%.
*/

#下划线通配符"_":用途与"%"一样，但下划线只匹配单个字符而非多个

select prod_name,prod_id
from products
where prod_name like "_ ton anvil";

#结果显示"_"只匹配了单个数字，.5的名称没有匹配


select prod_name
from products
where prod_name like "% ton anvil";
#除了"_"匹配到的，它将匹配 .5 ton anvil这条记录















