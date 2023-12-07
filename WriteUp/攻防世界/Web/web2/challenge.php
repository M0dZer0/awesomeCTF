<?php 
$miwen="a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws"; 

function encode($str){ 
    // 反转字符串
    $_o=strrev($str); 
    // echo $_o; 
         
    for($_0=0;$_0<strlen($_o);$_0++){ 
        // 截取字符
        $_c=substr($_o,$_0,1); 
        $__=ord($_c)+1; 
        $_c=chr($__); 
        $_=$_.$_c;    
    }  
    // 每个字母向后移动13个位置，即是加密算法，也是解密算法
    return str_rot13(strrev(base64_encode($_))); 
} 

highlight_file(__FILE__); 
/* 
   逆向加密算法，解密$miwen就是flag 
*/ 
?>