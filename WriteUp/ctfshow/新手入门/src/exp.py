import requests
import json
import base64
import random
url='http://0ea674d0-0052-4266-9701-cc5fbd9ea496.challenge.ctf.show/'


s=requests.session()
username=str(random.randint(1,100000))
print(username)
r=s.get(url+'?username='+username)
responses=[]

for i in range(10):
        r=s.get(url+'find_dragonball')
        responses.append(json.loads(r.text))

for item in responses:
        data=json.dumps({'player_id':item['player_id'],'dragonball':item['dragonball'],'round_no':item['round_no'],'time':item['time']})
        miwen=base64.b64decode(item['address'])
        round_no=item['round_no']
        if round_no in [str(i) for i in range(1,8)]:
                fake_address=miwen[:64]+miwen[80:]
                fake_address=base64.b64encode(fake_address).decode()
                r=s.get(url+'get_dragonball',params={"address":fake_address})

r=s.get(url+'flag')
print(r.text)