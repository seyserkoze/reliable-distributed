import requests
import json
import socket
import sys
import os

#init
server_address = 'http://128.237.128.85:80/'  
filename = os.path.join(os.getcwd(),"test", "zipme.zip")
#f = {'requestType' : 'newPhotos', 'zip' : ('blah.txt', 'foo\n')}
f = {'requestType' : 'newPhotos', 'zip' : open(filename, "rb")}
r = requests.post(server_address, files=f)
if r.status_code != 200:
    print("Error: unable to initialize with server")
    sys.exit()
print("sent")