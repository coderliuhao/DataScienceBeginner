use crashcourse;
#处于打开和使用状态的文件备份
/*
1 命令行实用程序mysqldump转储所有数据库内容到某个外部文件，在进行常规备份前这个实用程序应正常运行，
  以便能正确的备份转储文件
2 命令行实用程序mysqlcopy从一个数据库复制所有数据 
3 使用mysql的 backup table或select into outfile转储所有的数据到某个外部文件，这两个语句
  都接受将要创建的系统文件名，此系统文件必须不存在，否则会出错。数据可以使用
  restore table语句复原

tips 为保证所有数据被写到磁盘上，可能需要在进行备份前使用flush tables语句  
*/

analyze table orders;
#analyze table语句用来检查表键是否正确

check table orders,orderitems;
/*
1 check table支持在许多问题上对表进行检查，在MYISAM表上还对索引检查
2 check table支持一系列用于MyISAM的方式
3 changed检查最后一次检查以来改动过的表
4 extend执行最彻底的检查
5 fast只检查未正常关闭的表
6 medium检查所有被删除的链接并进行键检查
7 quick只进行快速扫描

tips 如果MyISAM表访问产生不正确和不一样的结果，需要用repair table
     语句来修复响应的表
	
     如果从一个表中删除大量数据，应使用optimize table来收回所用空间，优化表的性能
*/

/*
排除系统启动问题时，首先应该尽量用手动启动服务器。
mysql服务器自身通过在命令行上执行musqld启动，几个mysqld选项
1 --help 显示帮助
2 --safe-mode 装载减去某些最佳配置的服务器
3 --verbose 显示全文本消息
4 --versiion显示版本信息后退出
*/

/*
几种日志文件：
1 错误日志 包含自动关闭和启动问题以及任意关键错误的细节，通常命名为
  hostname.err,位于data目录中。名称可以用 --log-error命令行选项更改
2 查询日志 记录所有的mysql活动，日志通常命名为hostname.log位于data目录中
  可用--log命令行选项更改
3 二进制日志 记录更新过数据的的所有语句，通常命名为hostname-bin位于data怒目录内
  可用 --log-bin命令行选项进行更改
4 缓慢查询日志 记录执行缓慢的任何查询，通常命名为hostname-slow.log,
  位于data目录内，可用--log-slow-queries命令行选项更改
  
tips 使用日志时，可用flush logs语句刷新和重新开始所有日志文件  
*/


  