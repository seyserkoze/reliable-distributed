import requests
import json


r = requests.post('http://128.237.213.171:80/', data=json.dumps({'requestType':'phoneJoinReq', 'id':'1'}))
print(r.text)


