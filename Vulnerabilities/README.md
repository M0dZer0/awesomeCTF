### Vulnerabilities

#### PHP

在安装好PHP的本地环境的PHP项目根目录（即本项目的PHP目录）运行

```shell
sudo php -S 0.0.0.0:80	or	php -S 0.0.0.0:8000
```

然后访问`127.0.0.1`或`http://localhost:8000/`等即可查看index.php，在`/`后面输入PHP文件名即可进行攻击测试。

##### webshell.php

