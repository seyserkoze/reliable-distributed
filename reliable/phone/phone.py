import requests
import json
import os
import shutil


serverConnection = "http://128.237.213.171:80" 
# cloudletConnection = "http://192.168.26.1:420" 



def isAfterAmber(filePath, amberTime = 10):
    return true;

x = input("would you like to send your photos? ")


if (x == "yes"): 
    # tell server that you would like to help find the kid
    serverResponse = requests.post(serverConnection, json.dumps({"requestType":"phoneJoinReq","id": "1"}))
    r = json.loads(serverResponse.text)
    
    # Parse the server response for the cloudlet's IP and Port
    cloudletIP = r["IP"]
    cloudletPort = r["port"]

    cloudletConnection = "http://" + str(cloudletIP) + ":" + str(cloudletPort)

    # ping the cloudlet to tell it that the client would like to assist
    cloudletResponse = requests.post(cloudletConnection, json.dumps({"requestType":"phoneJoinReq","id": "1"}))


    # create new directory to hold cropped faces
    newpath = os.getcwd() + '/images/faces'
    print (newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # TODO: crop faces and put in new directory
    src_dir = "your/source/dir"
    dst_dir = "your/destination/dir"
    for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
        if (isAfterAmber(jpgfile, amberTime)):
            shutil.copy(jpgfile, dst_dir)


    # zip new directory
    shutil.make_archive('output', 'zip', newpath)
    
    # send zipped directory file to cloudlet
    files = {'file': open('output.zip', 'rb')}
    cloudletResponse = requests.post(cloudletConnection, files=files)


    # TODO: delete directory and zipped file



    
