import requests
import json
import os
import shutil


serverConnection = "http://128.237.213.171:80" 
cloudletIP = "temp"
cloudletPort = "temp"

#set yourself up with the server
def registerPhone():
    global cloudletIP
    global cloudletPort
    # tell server that you would like to help find the kid
    serverResponse = requests.post(serverConnection, json.dumps({"requestType":"phoneJoinReq","id": "1"}))
    r = json.loads(serverResponse.text)
    
    # Parse the server response for the cloudlet's IP and Port
    cloudletIP = r["IP"]
    cloudletPort = r["port"]


def isAfterAmber(filePath, amberTime = 10):
    return true

x = input("would you like to send your photos? ")

# TODO: make this into a loop so you can continuously send more photos
if (x == "yes"): 
    registerPhone()

    cloudletConnection = "http://" + str(cloudletIP) + ":" + str(cloudletPort)

    # create new directory to hold cropped faces
    newpath = os.getcwd() + '/images/faces'
    print (newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # TODO: crop faces and put in new directory
    # src_dir = "your/source/dir"
    # dst_dir = "your/destination/dir"
    # for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
    #     if (isAfterAmber(jpgfile, amberTime)):
    #         shutil.copy(jpgfile, dst_dir)


    # zip new directory
    shutil.make_archive('output', 'zip', newpath)
    
    # send zipped directory file to cloudlet
    files = {'requestType': 'newPhotos' ,'zip': open('output.zip', 'rb')}
    cloudletResponse = requests.post(cloudletConnection, files=files)


    # TODO: delete directory and zipped file
    os.remove('output.zip')
    print("images sent")
