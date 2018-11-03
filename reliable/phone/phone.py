import requests
import json
import os
import shutil


serverConnection = "http://128.237.213.171:80" 
# cloudletConnection = "http://192.168.26.1:420" 


def isAfterAmber(filePath):
    fileName = os.path.basename(file_path)
    if (filePath)

amberTime = 
x = input("would you like to send your photos? ")


if (x == "yes"): 
# tell server that you would like to help find the kidi
    # cloudletResponse = requests.post(cloudletConnection, json.dumps({"requestType":"phoneJoinReq","id": "1"}))
    serverResponse = requests.post(serverConnection, json.dumps({"requestType":"phoneJoinReq","id": "1"}))
    print(serverResponse.text)
    print(type(serverResponse.text))
    # print(cloudLetResponse)

    r = json.loads(serverResponse.text)
    cloudletIP = r["IP"]
    cloudletPort = r["port"]

    cloudletConnection = "http://" + str(cloudletIP) + ":" + str(cloudletPort)

    print(cloudletConnection)

    cloudletResponse = requests.post(cloudletConnection, json.dumps({"requestType":"phoneJoinReq","id": "1"}))
    print(cloudletResponse.text)

else: 

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

    # delete directory and zipped file



    
