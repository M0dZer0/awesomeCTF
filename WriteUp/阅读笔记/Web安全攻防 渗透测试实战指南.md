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

```html
index.php?id=-15 /*!UNION*/ /*!SELECT*/ 1,2,3
```

