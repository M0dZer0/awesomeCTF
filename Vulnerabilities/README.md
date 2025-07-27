### Vulnerabilities

#### PHP

在安装好PHP的本地环境的PHP项目根目录（即本项目的PHP目录）运行

```shell
sudo php -S 0.0.0.0:80	or	php -S 0.0.0.0:8000
```

然后访问`127.0.0.1`或`http://localhost:8000/`等即可查看index.php，在`/`后面输入PHP文件名即可进行攻击测试。

##### webshell.php

用于测试一句话木马。

##### file_include.php

使用file传递参数可以进行文件包含，`file_exists($file)`只会检测本地文件，而`include($file);`也可以通过HTTP协议和FTP协议对远程文件进行包含，如`file=https://m0dzer0.github.io/phpinfo.php`用以执行攻击。

##### filter.php

当限制包含的文件后缀时，可以使用伪协议进行文件数据读取。13
