### 第1章 Web类赛题

#### 1.SQL注入漏洞

##### 关键词绕过

- 编码绕过：URL编码、ASCII编码

- 字母大小写绕过

- 在关键词内添加无效字符：SE%00LECT、Sel%0bECT

- 内联注释绕过：/*! code */

- 利用被删除的关键词绕过：双写绕过等

- 等价函数与命令绕过

  - ```php
    && => and    || => or
    ```

  - ```php
    %20 %09 %0a %0b %0c %0d %a0 /**/ 制表符 ()	反引号 => 空格
    ```

  - ```php
    and 1 like 1 => and 1=1    and 2>1 => and 1=1				and 2<1 => and 1=2
    ```

  - ```php
    sleep() => benchmark()    concat_ws => group_concat    @@user => user()
    ```

- 宽字节绕过、溢出绕过等

##### 截断绕过

URL中的%00在ASCII码中表示0，而ASCII码中的0表示字符串的结束。所以当URL中出现%00时服务器会认为URL已经结束，不会再去检测后面的内容，而这将引发绕过验证。当一些参数被WAF检测到时，如SELECT被过滤，先尝试关键词绕过的方法无果后可以考虑使用添加无效字符的方法绕过"SEL%00ECT"。如果手工注入不方便，可以使用sqlmap中的template脚本，其中的InsertNullCharInSQLKeywords.py可以指定需要添加空字符的关键词。

##### 二次注入