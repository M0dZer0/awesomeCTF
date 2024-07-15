## NSSCTF的解题笔记

### WEB

#### Basic

##### 385

根据提示在burpsuite中将User-agent改为WLLM，再将X-Forward-For改为127.0.0.1，访问回显路径。

##### 386

PHP弱类型比较，见[WriteUp](./WEB/386.md)。

##### 427

PHP伪协议，见[WriteUp](./WEB/427.md)。

##### 441

PHP伪协议，见[WriteUp](./WEB/441.md)。

##### 2076

PHP弱类型的知识点，参考：https://www.nssctf.cn/note/set/3728。

##### 2638

先用万能密码绕过md5的密码匹配，后面就是基本的弱类型绕过。

##### 2640

使用php://filter协议就可以读取，参数设置为`php://filter/read=convert.base64-encode/resource=flag.php`。

##### 2821

和2640一样，参数设置为`?file=php://filter/resource=/flag`。

##### 2898

在控制台修改js代码运行我们想要的内容即可。如直接调用alert函数，或输入game  game.score=30000  game再执行任意操作。

##### 3053

考查几种查看源码的方式，可以在链接前加view-source:，可以禁用js，也可以使用curl而不用浏览器访问。

##### 3786

在game.js里有一段jsfuck编码，直接运行alert这段编码即可。

##### 3873

禁用javascript后进行命令拼接，对于前端验证也可以用bp抓包，参考：https://www.nssctf.cn/note/set/2160。

#### SQL injection

##### 1

有过滤的布尔盲注，见[WriteUp](./WEB/384.md)。

##### 19

sql语句拼接，参考：https://www.nssctf.cn/note/set/36。

##### 387

简单的SQL注入，见[WriteUp](./WEB/387.md)。

##### 428

简单的报错注入，用sqlmap自动解。

##### 442

对空格和一些关键词进行了过滤，参见：https://www.nssctf.cn/note/set/2862。

##### 713

万能密码和md5绕过方法，见[WriteUp](./WEB/713.md)。

#### RCE tricks

##### 383

使用hackbar直接提交system函数执行RCE。

##### 384

使用hackbar进行get和post方法传参，见[WriteUp](./WEB/384.md)。

##### 424

eval函数会执行传入的参数语句，见[WriteUp](./WEB/424.md)。

##### 425

用%09或${IFS}绕过空格过滤。

##### 438

过滤了一些关键词和无回显的命令执行，参见：https://www.nssctf.cn/note/set/2564。

##### 439

参数传递可以取反绕过，参见：https://www.nssctf.cn/note/set/6233。

##### 1096

对命令进行了过滤，那就用变量绕过，payload:`127.0.0.1;a=g;tac$IFS$1fla$a.php`。

##### 3409

对一些指令进行了过滤，别人的wp中有一些常见的绕过方法，我这里采用的`?rce=/bin/ca?$IFS????.php`。

##### 3864

使用hackbar进行GET和POST传参就可以了。

##### 3865

右边输入system函数会直接执行。

#### FILE search

##### 344

目录扫描找到phpinfo文件。

##### 382

使用F12查看源代码即可。

##### 1421

命令执行查看目录，发现一个txt文件，base64编码转图片。

#### FILE upload

##### 388

和423类似，只是flag在环境变量里(phpinfo.php)中,所以使用`<?php system(env); ?>`可以直接查看。

##### 423

基础的文件上传题，见[WriteUp](./WEB/423.md)。

##### 436

文件上传的基础题，见[WriteUp](./WEB/436.md)。

#### Unserialize

##### 426

dirsearch打开robots.txt查看隐藏的php文件，反序列化后输出。

##### 429

反序列化基础题，见[WriteUp](./WEB/429.md)。

##### 440

反序列化逻辑链的构造，注意结果需要url编码，参见：https://www.nssctf.cn/note/set/339。

##### 2602

简单的自定义反序列化，见[WriteUp](./WEB/2602.md)。

#### SSRF

##### 2011

SSRF,使用file协议读取本地文件，见[WriteUp](./WEB/2011.md)。

#### CRYPTO

##### 691

base64换表问题，将自定义的表丢到cyberchef即可解码。

##### 932

循环尝试base解码，POC见[WriteUp](./CRYPTO/932.md)。

##### 945

quipqiup解决不了，找到了一个新工具：https://www.guballa.de/vigenere-solver。

#### MISC

##### 433

很无聊，但知道了八卦和八进制的对应关系，以后遇到有记忆。

##### 450

很多加密套娃，这里学习到了一个新工具ciphey，用kali的apt或者Mac的brew安装即可。

##### 752

一道图片的base64编码题，利用[在线解码器](https://tool.jisuapi.com/base642pic.html)即可解决
