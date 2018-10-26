import requests
import json
import socket
import sys


#init
server_address = 'http://192.168.26.1:80/'  
my_ip = socket.gethostbyname(socket.gethostname())
port = 420

init_values = { 'requestType' : 'newPhotos', 'photos' : 'hello'}
init_data = json.dumps(init_values)
f = {'test' : open('test/dog.jpg', 'rb')}
r = requests.post(server_address, json=init_values, files=f)
if r.status_code != 200:
    print("Error: unable to initialize with server")
    sys.exit()
print("success")

while (1):
    continue