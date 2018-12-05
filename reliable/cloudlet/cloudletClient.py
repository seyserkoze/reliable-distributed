import requests
import os
import shutil
import zipfile
import cloudletSettings as settings
import face_recognition
import sys
import time


def init_cloudlet():
    #setup known and unknown directories
    if os.path.exists(settings.known_dir):
        shutil.rmtree(settings.known_dir)
    if os.path.exists(settings.unknown_dir):
        shutil.rmtree(settings.unknown_dir)
    os.makedirs(settings.known_dir)
    os.makedirs(settings.unknown_dir)
    #register yourself with the server
    init_values = { 'requestType' : 'cloudJoinReq', 'id' : '1', 'cloudIP': settings.my_ip, 'cloudPort' : str(settings.my_port)}
    post_request(init_values)
    print("Cloudlet initialized")

def newJob(jobName):
    #assume the zip file is already there from the server
    #add the job to the list, extract the zip file and then delete it
    settings.jobs[jobName] = []
    zip_dir = os.path.join(settings.known_dir, jobName)
    zipped = os.path.join(zip_dir, jobName + ".zip")
    fp = zipfile.ZipFile(zipped, 'r')
    fp.extractall(zip_dir)
    fp.close()
    os.unlink(zipped)
    #get the face_encodings for each one
    for pic in get_photos(zip_dir):
        try:
            image = face_recognition.load_image_file(pic)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                settings.jobs[jobName].append(encodings[0])
        except:
            print("unable to get face encoding for " + pic)
    #delete the pictures once we get the encodings
    shutil.rmtree(zip_dir)

#recursively tries to find every photo in a directory, assuming there are only image files
def get_photos(path):
    result = []
    for r, d, files in os.walk(path):
        for f in files:
            if f[0] == ".":
                continue
            result.append(os.path.join(r, f))
    return result

def deleteJob(jobName):
    #delete that job from the known directories
    del settings.jobs[jobName]
    #delete that directory
    job_dir = os.path.join(settings.known_dir, jobName)
    return

#should probably do this in a new thread, since itll be slow af and itl happen alot
def processPhotos(newZip):
    zip_dir = os.path.join(settings.unknown_dir,newZip)
    fp = zipfile.ZipFile(zip_dir, 'r')
    #IF YOU DO MULTITHREAD NEED TO LOCK THE NEXT TWO LINES, ADD A MUTEX TO SETTINGS
    extractPath = os.path.join(settings.unknown_dir, str(settings.unique_id))
    settings.unique_id += 1
    fp.extractall(extractPath)
    fp.close()
    os.unlink(zip_dir)
    no_matches = True
    #iterate through each job
    #this needs to be done before the loop, otherwise get_photos will be returning zip files as well
    photos = get_photos(extractPath)
    for job, knowns in settings.jobs.items():
        match_found = False
        #get the face_encodings for each one
        for pic_path in photos:
            pic = pic_path.split("/")[-1]
            try:
                image = face_recognition.load_image_file(pic_path)
                #assume only one face per image since the phone will be cropping them
                unknown = face_recognition.face_encodings(image)[0]
            except:
                continue
            result = face_recognition.compare_faces(knowns, unknown)
            if True in result:
                print("match found for " + job + "! Picture: " + pic)
                match_found = True
                no_matches = False
                #move the picture over
                match_path = os.path.join(extractPath, job)
                if not os.path.exists(match_path):
                    os.makedirs(match_path)
                shutil.copy2(pic_path, os.path.join(match_path, pic))
        if match_found:
            #send it back to the server
            zipMatches = os.path.join(extractPath, job)
            shutil.make_archive(zipMatches, "zip", os.path.join(extractPath, job))
            reqBody = {"requestType" : "match", "zip" : open(zipMatches +".zip", "rb")}
            post_request(reqBody)
    if no_matches:
        print("No Matches found")
    shutil.rmtree(extractPath)
    return

#let the server know a phone left
def leave():
    body = {"requestType" : "phoneLeaveReq", 'cloudIP': settings.my_ip, 'cloudPort' : str(settings.my_port)}
    post_request(body)
    return

def getJobs():
    time.sleep(4) #give time for the server to initialize
    body = {"requestType" : "getJobs", "cloudIP" : settings.my_ip, "cloudPort": str(settings.my_port)}
    post_request(body)
    t = get_time()
    print(t + ": Receiving current jobs...")
    return

def heartbeat():
    body = {"requestType" : "heartbeat"}
    while(1):
        print(get_time() + ": sending heartbeat...", end="") #dont start a newline
        try:
            #try to make a request with a timeout of 1 second
            requests.post(settings.current_serv, files=body, timeout=3)
            print("server is alive")
        except:
            print("failed, switching server")
            settings.switch_server()
        time.sleep(settings.heartbeat_interval)

#helper for making requests, add a timeout to detect if a server is down
#switch to the other server if one is down
def post_request(body):
    while(1):
        try:
            #try to make a request with a timeout of 1 second
            requests.post(settings.current_serv, files=body, timeout=3)
            return
        except:
            new_num = (settings.server_num+1) % 2
            print(get_time() + ": Server " + str(settings.server_num) + " down, switching to server " + str(new_num))
            settings.switch_server()

def get_time():
    return time.asctime(time.localtime(time.time()))