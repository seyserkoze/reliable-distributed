import requests
import json
import os
import shutil
import sys
from tkinter import filedialog
import tkinter
#import exifread
#Add this to readme dependables if we do it: exifread: https://pypi.org/project/ExifRead/ (pip3 install exifread)

serv1 = "http://128.237.124.45:80"
serv2 = "http://128.237.124.45:72"

#set yourself up with the server
def registerPhone():
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

#copies all files in 'files' to the directory 'tempdir'
#TODO: add the location stuff to this function
def copyFiles(files, tempdir):
    # lat1 = "Latitude"
    # lat2 = "EXIF Latitude"
    # long1 = "Longitude"
    # long2 = "EXIF Longitude"
    location = "Pittsburgh, PA"
    count = 0
    for f in files:
        file_ending = f.split(".")[-1]
        name = location + str(count) + file_ending
        new_name = os.path.join(tempdir, name)
        shutil.copy(f, new_name)
        count += 1
        # fp = open(f, 'rb')
        # tags = exifread.process_file(fp)
        # fp.close()
        # keys = tags.keys()
        # lat = ""
        # lon = ""
        # #latitude
        # if (lat1 in keys):
        #     lat = keys[lat1]
        # elif (lat2 in keys):
        #     lat = keys[lat2]
        # #longitude
        # if (long1 in keys):
        #     lon = keys[long1]
        # elif (long2 in keys):
        #     lon = keys[long2]
        # location = #https://stackoverflow.com/questions/20169467/how-to-convert-from-longitude-and-latitude-to-country-or-city
        # shutil.copy2(f, os.path.join(tempdir, location))




######################START##################################
cloudlet = registerPhone()
root = tkinter.Tk()
my_gui = PhoneGUI(root)
root.mainloop()

while(1):
    # create temp directory to copy images to
    tempdir = os.getcwd() + '/__tEmPoRArY_NANI'
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    #TODO: GUI to get file names and copy them to the tempdir


    copyFiles(fileList)
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
