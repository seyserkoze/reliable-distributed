import requests
import json
import socket
import sys
import os

#init
server_address = 'http://10.0.0.246:80/'  
filename = os.path.join(os.getcwd(),"test", "obama.zip")
r = {'requestType' : 'newPhotos', 'zip' : open(filename, 'rb')}
f = {'requestType' : 'newJob', 'zip' : open(filename, "rb")}
d = {'requestType' : 'deleteJob', 'jobName' : 'zipme'}
r = requests.post(server_address, files=f)
if r.status_code != 200:
    print("Error: unable to initialize with server")
    sys.exit()
print("sent")