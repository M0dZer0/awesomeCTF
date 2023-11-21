# WEB

[TOC]



## SQL注入

### UNION注入

由于PHP代码的一些限制，页面可能只会显示一行记录，所以我们需要将想要的结果显示在第一行，此时有多种方法，如可以在末尾添加`limit 1,1`参数，作用是取查询结果第一条记录后的1条记录，或者指定id=-1或一个很大的值使得第一行记录无法被查询到。

<!--union联合查询是将查询结果和主查询结果组合，需要保证列数相同，我们常用order by判断列数并用union select 1，2，3...依据回显数字判断注入语句应该写在哪一列都是依照这个原理-->



## XSS

## 文件上传

## WEB技巧

### PHP弱类型(MD5绕过)

参考：https://www.bilibili.com/video/BV1mb411R7LR?p=3&vd_source=babc412cd285c7f3e7b58102a5465f0f

### 命令执行漏洞

用分号执行命令拼接

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
