import requests
import os
import shutil
import zipfile
import cloudletSettings as settings
import face_recognition


def init_cloudlet():
    #setup known and unknown directories
    if os.path.exists(settings.known_dir):
        shutil.rmtree(settings.known_dir)
    if os.path.exists(settings.unknown_dir):
        shutil.rmtree(settings.unknown_dir)
    os.makedirs(settings.known_dir)
    os.makedirs(settings.unknown_dir)
    #register yourself with the server
    serv_addr = settings.serv_ip + str(settings.serv_port)
    init_values = { 'requestType' : 'cloudJoinReq', 'id' : '1', 'cloudIP': settings.my_ip, 'cloudPort' : str(settings.my_port)}
    r = requests.post(serv_addr, files=init_values)
    if r.status_code != 200:
        print("Error: unable to initialize with server")
        sys.exit()
    print("Cloudlet initialized")

def newJob(jobName):
    #assume the zip file is already there from the server
    #add the job to the list, extract the zip file and then delete it
    settings.jobs[jobName] = []
    zip_dir = os.path.join(settings.known_dir, jobName + ".zip")
    fp = zipfile.ZipFile(zip_dir, 'r')
    fp.extractall(settings.known_dir)
    fp.close()
    os.unlink(zip_dir)
    print(os.listdir(zip_dir[:-4]))
    #get the face_encodings for each one
    for pic in os.listdir(zip_dir[:-4]):
        pic_path = os.path.join(zip_dir[:-4], pic)
        if pic[0] == ".":
            continue
        image = face_recognition.load_image_file(pic_path)
        encoding = face_recognition.face_encodings(image)[0]
        settings.jobs[jobName].append(encoding)
    #delete the pictures once we get the encodings
    shutil.rmtree(zip_dir[:-4])


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
    fp.extractall(extractPath)
    settings.unique_id += 1
    fp.close()
    os.unlink(zip_dir)
    match_found = False
    job = "blah"
    knowns = []
    #get the face_encodings for each one
    for pic in os.listdir(os.path.join(extractPath, newZip[:-4])):
        if pic[0] == ".":
            continue
        pic_path = os.path.join(extractPath, newZip[:-4], pic)
        image = face_recognition.load_image_file(pic_path)
        unknown = face_recognition.face_encodings(image)[0]
        if not match_found:
            for k, v in settings.jobs.items():
                result = face_recognition.compare_faces(v, unknown)
                if result[0]:
                    print("match found! Picture: " + pic)
                    match_found = True
                    #move the picture over
                    match_path = os.path.join(extractPath, k)
                    if not os.path.exists(match_path):
                        os.makedirs(match_path)
                    shutil.move(pic_path, os.path.join(match_path, pic))
                    job = k
                    knowns = v
                    break
        #once a match is found only check against that one job
        else:
            result = face_recognition.compare_faces(knowns, unknown)
            if result[0]:
                print("match found! Picture: " + pic)
                match_found = True
                #move the picture over
                match_path = os.path.join(extractPath, job)
                if not os.path.exists(match_path):
                    os.makedirs(match_path)
                shutil.move(pic_path, os.path.join(match_path, pic))
    if match_found:
        #send it back to the server
        zipMatches = os.path.join(extractPath, job)
        shutil.make_archive(zipMatches, "zip", os.path.join(extractPath, job))
        reqBody = {"requestType" : "match", "zip" : open(zipMatches, "rb")}
        r = requests.post(settings.serv_ip + ":" + settings.serv_port, files=reqBody)
        if r.status_code != 200:
            print("Unable to send matches to the server")
    else:
        print("No Matches found")
    shutil.rmtree(extractPath)
    return