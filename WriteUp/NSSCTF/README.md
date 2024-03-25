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

