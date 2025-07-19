### 第1章 Web安全基础知识

#### HTTP

HTTP的常用请求方法有：

| 请求方法 | 功能                                                         |
| -------- | ------------------------------------------------------------ |
| GET      | 通常用于直接获取服务器上的资源                               |
| POST     | 一般用于向服务器发送数据，常用于更新资源信息                 |
| PUT      | 一般用于新增一个数据记录                                     |
| PATCH    | 一般用于修改一个数据记录                                     |
| DELETE   | 一般用于删除一个数据记录                                     |
| HEAD     | 一般用于判断一个资源是否存在                                 |
| OPTIONS  | 一般用于获取一个资源自身所具备的约束，如应该采用怎样的HTTP方法及自定义的请求头 |

HTTP的常见状态码：

| 状态码                    | 含义                                                         |
| ------------------------- | ------------------------------------------------------------ |
| 101 Switching Protocols   | 切换协议，通常见于HTTP切换为Websocket协议                    |
| 200 OK                    | 请求成功                                                     |
| 201 Created               | 资源创建成果，通常用于回应动词PUT                            |
| 204 No Content            | 用于不回显任何内容的情况，如网络联通性检测                   |
| 301 Moved Permanently     | 永久跳转，浏览器以后访问到这个地址都会直接跳转到Location头所指向的新地址 |
| 302 Found                 | 临时跳转，会跳转到Location头所指向的地址                     |
| 404 Not Found             | 所请求资源不存在                                             |
| 405 Method not allowed    | 方法不被允许                                                 |
| 500 Internal Server Error | 服务器内部错误                                               |
| 502 Bad Gateway           | 网关在转发内容时出错，通常是转发的下一站—后端不可达或返回了一些奇怪的信息 |
| 504 Gateway Time-out      | 网关在转发内容时出错，通常是转发的下一站—后端不可达          |

### 第2章 Web安全入门—PHP相关知识

#### 弱类型特性

PHP是弱类型语言（还有javascript），如果是运算操作，PHP会把所有数据都转换成整型，如果是拼接操作，则会全部转换成str

```shell
php > var_dump(1 + '1');
int(2)
php > var_dump('1' + 1);
int(2)
php > $num1 = 'test';
php > $num2 = 1;
php > var_dump($num1.$num2);
string(5) "test1"
```

#### 变量覆盖漏洞

##### PHP语法导致的变量覆盖

```php
<?php
  $a = "want_to_be_a_cat";
  $b = "miaow";
  $test = $a;
  $$test = $b;	// 取变量$test的值作为新变量名
  var_dump($want_to_be_a_cat);	// 输出miaow
```

##### PHP函数导致的变量覆盖

```php
<?php
  $a = "want_a_cat";
  $b = "miao";
  extract([$a => $b]);
  var_dump($want_a_cat);	// 输出miao
	//
	将关联数组 [$a => $b] 解包为变量和值。
	等同于 extract(["want_a_cat" => "miao"])。
	它会创建一个新的变量 $want_a_cat，并将值 "miao" 赋给它。
  //
  //parse_str("want_a_cat = miao");	// 只在PHP5.2中出现 创建一个变量 $want_a_cat，并赋值为 "miao"。
  //var_dump($want_a_cat);
  //mb_parse_str("want_a_cat = miao");	// 只在PHP5.2中出现与parse_str()类似，但它支持多字节字符串（如 UTF-8 编码）。
	//var_dump($want_a_cat);
```

##### PHP配置项导致变量覆盖（register_globals: php.ini中的一个配置项，配置为true之后传入GET/POST参数都会被赋成变量）

```php
<?php
  var_dump($want_to_be_a_cat);	// 传入want_to_be_a_cat = miao，输出miao
```

#### 文件包含漏洞

在PHP中，文件包含语法主要有`include` `include_once` `require` `require_once`

```php
<?php
  include 'b.php';
	include_once 'b.php';	// 整个程序中只会包含一次
	include('b.php');	// 遇到错误程序会继续执行
	include_once('b.php');
	require 'b.php';
	require_once 'b.php';
	require('b.php');	// 遇到错误程序会报错退出
	require_once('b.php');
```

PHP的文件包含会先读去文件，如果内容是PHP代码，那就直接解析成PHP代码包含进来，如果不是PHP代码则会原样输出，这样可能造成任意攻击代码执行和任意文件读取漏洞。

##### PHP本地文件包含漏洞

```php
<?php
	include($_GET['file']);
	// 没输入路径的时候，默认和当前php同一路径
	include('var/www/html/'.$_GET['file']);
```

利用这个漏洞执行webshell，有几种常见方法：

1. Web的文件上传功能，在图片中插入我们的PHP代码，然后包含该图片即可；
2. 利用中间件日志文件来助攻，一般中间件默认都会开启日志记录，当请求`http://127.0.0.1:8080/1.php ? file=<? php phpinfo(); ?>`这个地址时，这个请求就会被中间件保存在自己的日志中，再通过包含日志文件，如`/var/log/apache2/access.log`，从而解析日志中存在的恶意代码；
3. 通过SSH日志文件包含：尝试通过命令`ssh '<? php phpinfo();?>'@HOST`去连接目标机器，我们的代码就会被当成用户名存放在`/var/log/auth.log`中，然后文件包含即可。

##### PHP远程文件包含漏洞

远程文件包含先根据输入的URL访问到远程资源，然后再把内容返回。进行包含时，远程文件包含需要PHP配置项中`allow_url_include = On`，否则无法利用，配置项通常在`php.ini`文件中，运行`php --ini`命令即可加载文件路径。常见的路径有

```
/opt/homebrew/etc/php/8.1/php.ini
/usr/local/etc/php/8.1/php.ini
/etc/php/8.1/apache2/php.ini
```

远程文件包含一般有HTTP、FTP协议等，对于以下PHP代码，我们只需要对file传递一个URL即可解析远程文件。注意的是，`file_exists($file)`函数只对本地文件包含生效（php 8.3）。但这个配置项通常设置为Off，漏洞已经不常见了。

```php
<?php
highlight_file(__FILE__);
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    include($file);
    if (file_exists($file)) {
        include($file);
    } else {
        echo "File does not exist.";
    }
} else {
    echo "No file specified.";
}
?>
```

