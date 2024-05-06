import urllib.parse
test ="""GET /xxx.php HTTP/1.1
Host: 127.0.0.1:80
"""
#注意后面一定要有回车，回车结尾表示http请求结束
tmp = urllib.parse.quote(test)
new = tmp.replace('%0A','%0D%0A')
result = 'mybox://127.0.0.1:80/'+'_'+new
print(urllib.parse.quote(result))
