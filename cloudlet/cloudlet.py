import requests
import json
import socket
import sys
import cloudletServer

#init
server_address = 'http://128.237.213.171:80/'  
my_ip = socket.gethostbyname(socket.gethostname())
port = 80

init_values = { 'requestType' : 'cloudJoinReq', 'id' : '1', 'cloudIP': my_ip, 'cloudPort' : str(port)}
init_data = json.dumps(init_values)
r = requests.post(server_address, data=init_data)
if r.status_code != 200:
    print("Error: unable to initialize with server")
    sys.exit()
print("success")

cloudletServer.run(my_ip, port)
