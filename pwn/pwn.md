# PWN

[TOC]

## Pwntools Usage

## ROP gadget

在栈缓冲区溢出的基础上，利用程序中已有的小片段(gadgets) 来改变某些寄存器或者变量的值，从而控制程序的执行流程。所谓gadgets 就是以ret 结尾的指令序列，通过这些指令序列，我们可以修改某些内存或者寄存器的值。
