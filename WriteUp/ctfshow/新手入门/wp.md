## 菜狗入门题writeup

[TOC]

##### 一、杂项签到

使用010 editor查找ASCII的ctf字段，找到flag。

##### 二、损坏的压缩包

使用010 editor查看文件类型，将文件格式改为png。

##### 三、谜之栅栏

使用010 editor的compare files功能找到不同字段。

##### 四、你会数数吗

使用010 editor的histogram功能对可见字符数进行排序。

<img src="./src/4.1.png" alt="4.1" style="zoom:50%;" />

##### 五、你会异或吗

使用010 editor的hex operations功能进行0x50异或得到正常图片。

##### 六、flag一分为二

额Mac上不好操作直接找了[wp](https://blog.csdn.net/m0_68012373/article/details/128960816)。

##### 七、我是谁

一道网页交互和图像处理的题目，看[脚本](./src/whoami.py)。

##### 八、you and me

盲水印的题目，直接用GitHub开源的BlindWaterMark-master。

##### 九、我吐了你随意

unicode零宽字符的题目，用[网站工具](http://330k.github.io/misc_tools/unicode_steganography.html)解码。

##### 十、web签到

按源代码要求用hackbar提交内容执行打印flag操作。注意使用cookie传参的时候对CTFshow-QQ群:=post_var进行url编码。

<img src="./src/web1.png" alt="image-20240117204139359" style="zoom:50%;" />