### NSSCTF的解题笔记

#### WEB

##### 344

目录扫描找到phpinfo文件。

##### 382

使用F12查看源代码即可。

##### 383

使用hackbar直接提交system函数执行RCE。

##### 384

使用hackbar进行get和post方法传参，见[WriteUp](./WEB/384.md)。

##### 385

根据提示在burpsuite中将User-agent改为WLLM，再将X-Forward-For改为127.0.0.1，访问回显路径。

##### 386

PHP弱类型比较，见[WriteUp](./WEB/386.md)。

##### 387

简单的SQL注入，见[WriteUp](./WEB/387.md)。

##### 388

和423类似，只是flag在环境变量里(phpinfo.php)中,所以使用`<?php system(env); ?>`可以直接查看。

##### 423

基础的文件上传题，见[WriteUp](./WEB/423.md)。

##### 424

eval函数会执行传入的参数语句，见[WriteUp](./WEB/424.md)。

##### 425

用%09或${IFS}绕过空格过滤。

##### 426

dirsearch打开robots.txt查看隐藏的php文件，反序列化后输出。

##### 427

PHP伪协议，见[WriteUp](./WEB/427.md)。

##### 429

反序列化基础题，见[WriteUp](./WEB/429.md)。

##### 436

文件上传的基础题，见[WriteUp](./WEB/436.md)。

##### 439

参数传递可以取反绕过，参见：https://www.nssctf.cn/note/set/6233。

##### 441

PHP伪协议，见[WriteUp](./WEB/441.md)。

##### 713

万能密码和md5绕过方法，见[WriteUp](./WEB/713.md)。

##### 1096

对命令进行了过滤，那就用变量绕过，payload:`127.0.0.1;a=g;tac$IFS$1fla$a.php`。

##### 2011

SSRF,使用file协议读取本地文件，见[WriteUp](./WEB/2011.md)。

##### 3864

使用hackbar进行GET和POST传参就可以了。

##### 3865

右边输入system函数会直接执行。

##### 3873

禁用javascript后进行命令拼接，对于前端验证也可以用bp抓包，参考：https://www.nssctf.cn/note/set/2160。

#### CRYPTO

#### MISC
