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

额Mac上不好操作直接找了[wp](https://blog.csdn.net/m0_68012373/article/details/128960816)

##### 七、我是谁

一道网页交互和图像处理的题目，看[脚本](./src/whoami.py)