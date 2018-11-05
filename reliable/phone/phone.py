import requests
import json
import os
import shutil
import glob
import faceCropping

serverConnection = "http://128.237.178.179:80"
# 128.237.178.179
cloudletIP = "temp"
cloudletPort = "temp"

amberTime = 10
#set yourself up with the server
def registerPhone():
    global cloudletIP
    global cloudletPort
    # tell server that you would like to help find the kid
    serverResponse = requests.post(serverConnection, files={"requestType":"phoneJoinReq","id": "1"})
    print (serverResponse.text)
    r = json.loads(serverResponse.text)
    
    # Parse the server response for the cloudlet's IP and Port
    cloudletIP = r["IP"]
    cloudletPort = r["port"]



def isAfterAmber(filePath, amberTime = 10):
    return True

x = input("would you like to send your photos? ")

# TODO: make this into a loop so you can continuously send more photos
if (x == "yes"): 
    registerPhone()

    cloudletConnection = "http://" + str(cloudletIP) + ":" + str(cloudletPort)

    # create new directory to hold cropped faces
    # changed it to the unknown folder for now for the demo
    newpath = os.getcwd() + '/unknown'
    print (newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # TODO: crop faces and put in new directory
    # src_dir = os.getcwd() + '/images'
    #dst_dir = os.getcwd() + '/images/faces'
    #for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
    #    fname, ext = os.path.splitext(jpgfile)
    #    if (isAfterAmber(fname, amberTime)):
    #        facecrop(jpgfile)
    #        shutil.copy(fname+"_cropped_"+ext, dst_dir)

    # zip new directory
    shutil.make_archive('output', 'zip', newpath)
    
    # send zipped directory file to cloudlet

    files = {'requestType': 'newPhotos' ,'zip': open('output.zip', 'rb')}
    cloudletResponse = requests.post(cloudletConnection, files=files)


    # TODO: delete directory and zipped file
    os.remove('output.zip')
    print("images sent")
