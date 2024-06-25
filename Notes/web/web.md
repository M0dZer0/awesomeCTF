# WEB

[TOC]



## SQL注入

### UNION注入

由于PHP代码的一些限制，页面可能只会显示一行记录，所以我们需要将想要的结果显示在第一行，此时有多种方法，如可以在末尾添加`limit 1,1`参数，作用是取查询结果第一条记录后的1条记录，或者指定id=-1或一个很大的值使得第一行记录无法被查询到。

<!--union联合查询是将查询结果和主查询结果组合，需要保证列数相同，我们常用order by判断列数并用union select 1，2，3...依据回显数字判断注入语句应该写在哪一列都是依照这个原理-->

### 字符型注入

在MYSQL（PHP）中，等号两边如果类型不一致，则会发生强制转换，如

```mysql
'1' ==> 1		'1a' ==> 1		'a' ==> 0
```

因此我们可以输入`?id=1a`判断是否为字符型注入

在输入URL时，我们要熟悉一些字符编码

```php
' ==> %27
# ==> %23
空格 ==> %20
```

### 布尔盲注

substring()、mid()、substr()、trim()等用法参考：

https://www.bilibili.com/video/BV1mb411R7LR?p=14&vd_source=babc412cd285c7f3e7b58102a5465f0f

### 堆叠注入

当目标开启多语句执行时，可以采用多语句执行的方式修改数据库的任意结构和数据，我们可以在闭合单引号后执行任意SQL语句。

### 防御和注入方法

SELECT、GROUP BY、ORDER BY、LIMIT、INSERT、UPDATE、DELETE注入参见<u>从0到1CTFer成长之路</u>

1. 字符替代
   - 只过滤空格
     - 可以用%0a、%09、%a0和/**/组合、括号等代替
   - 过滤某些关键词
     - 如将SELECT替换为空，我们可以使用嵌套如SESELECTLECT的形式绕过
     - 如果只过滤SELECT，可以考虑大小写混写的方式绕过
   - 正则匹配
     - 如关键词\bselect\b可以用形如/* !50000select */的方式绕过
2. 逃逸引号

## 任意文件读取漏洞

## XSS

## 文件上传

## WEB技巧

### burpsuite使用方法

#### GET和POST方法传参

参考：https://www.cnblogs.com/Clannad21/p/16410229.html

### PHP弱类型(MD5绕过)

参考：https://www.bilibili.com/video/BV1mb411R7LR?p=3&vd_source=babc412cd285c7f3e7b58102a5465f0f

在PHP5中，intval函数存在问题

```php
intval('2e4') ==> 2		intval('2e4' + 1)==> 20001
```

参考：https://www.cnblogs.com/dre0m1/p/16062369.html

参考：https://blog.csdn.net/Xxy605/article/details/109427287

参考：https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value

### 命令执行漏洞

用分号执行命令拼接

PHP绕过字符匹配：http://www.360doc.com/content/23/1011/08/1099749859_1099749859.shtml

### PHPbypass绕过

参考：https://www.bilibili.com/video/BV1mb411R7LR?p=8&vd_source=babc412cd285c7f3e7b58102a5465f0f

### Git信息泄露

攻击者可以通过开发者遗忘的.git文件夹获取开发人员提交过的所有源代码，进而可能导致服务器被攻击。

1. 常规git泄露

​	使用[scrabble](https://github.com/denny0223/scrabble)工具直接获取源代码

2. git回滚

​	git记录了每次提交的修改，所以当存在git信息泄露时flag文件可能在修改中被删除或者覆盖了，但我们可以利用`git reset`恢		复之前的版本，我们可以先利用scrabble工具获取源代码，再通过`git reset --hard HEAD^`跳到上一版本。更简单的方法是		通过`git log -stat`查看每个commit修改了哪些文件，再用`git diff HEAD commit-id`查看当前版本与id对应版本的变化。

3. git分支

​	使用[GitHacker](https://github.com/WangYihang/GitHacker)查找分支，执行`git reflog`命令可以看到checkout的记录，自动化工具可以恢复其他分支的信息。
