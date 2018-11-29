import requests
import json
import os
import shutil

serv1 = "http://128.237.124.45:80"
serv2 = "http://128.237.124.45:72"

fileList = []

#set yourself up with the server
def registerPhone():
    global cloudlet
    # tell server that you would like to help find the kid
    registerBody = {"requestType":"phoneJoinReq","id": "1"}
    serverResponse = None
    try:
        serverResponse = requests.post(serv1, files=registerBody, timeout=1)
    except:
        try:
            print("First server down(" + serv1 + "), trying second server(" + serv2 + ")")
            serverResponse = requests.post(serv2, files=registerBody, timeout=1)
        except:
            print("Both servers unavailable, aborting...")
            sys.exit()
    print (serverResponse.text)
    r = json.loads(serverResponse.text)
    
    # Parse the server response for the cloudlet's IP and Port
    cloudletIP = r["IP"]
    cloudletPort = r["port"]
    cloudlet = "http://" + str(cloudletIP) + ":" + str(cloudletPort)
    return cloudlet


cloudlet = registerPhone()

while(1):
    # create temp directory to copy images to
    tempdir = os.getcwd() + '/__tEmPoRArY_NANI'
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    #TODO: GUI to get file names and copy them to the tempdir

    # zip new directory and remove the temp folder
    shutil.make_archive('output', 'zip', tempdir)
    shutil.rmtree(tempdir)

    # send zipped directory file to cloudlet
    files = {'requestType': 'newPhotos' ,'zip': open('output.zip', 'rb')}
    requests.post(cloudlet, files=files, timeout=5)

    #delete zip file
    os.remove('output.zip')
    print("images sent")

#we're done, phone leave
try:
    requests.post(cloudlet, files={'requestType': 'leave'}, timeout =1)
except:
    pass
