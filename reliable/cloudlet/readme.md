# Cloudlet


### Prerequisites

requests library: http://docs.python-requests.org/en/master/
face matching api: https://github.com/ageitgey/face_recognition?fbclid=IwAR1561byVmHtARls6ZWRGg5QhxETWKO2VvuCjc1T7GP1MuJC1GTemd2jhTI

check this out later for multithreading: https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python

^be careful about deleting jobs while processing them tho if you do this

### Running the cloudlet

```
sudo python3 cloudlet.py arg1 arg2 arg3 arg4
```
arg1: IP address of the first server  
arg2: IP address of the second server  
arg3: The port this cloudlet will listen on  
arg4: The heartbeat interval between this cloudlet and the primary server  

Note that if you run multiple instances of cloudlet on a single machine you MUST run 
them in different directories and on different ports

### How to communicate with the cloudlet

#### Making requests to the cloudlet:

##### From the Server:

To send a create a new job: 

    key: requestType    value: newJob

    key: zip            value: (zipfile containing the job(name of zipfile MUST be "jobName.zip"))

To delete a job:

    key: requestType    value: deleteJob

    key: jobName        value: (name of the job to delete)

##### From the phone:

To submit unknown photos for processing:

    key: requestType    value: newPhotos

    key: zip            value: (zip file containing the photos to check, name can by anything)

To tell the cloudlet you're leaving:
    
    key: requestType    value: leave


#### Cloudlet Requests to server:

To initialize itself(everything here is a string):

    key: requestType    value: cloudJoinReq

    key: id             value: 1

    key: cloudIP        value: (ip address of the cloudlet ex. "128.237.185.97")

    key: cloudPort      value: (the port number this cloudlet will listen on)

To send found matches to the server:

    key: requestType    value: match

    key: zip            value: (zipfile containing the matches, name of the zipfile will be the name of the job)

To let the server know a phone left it:

    key: requestType    value: phoneLeaveReq

    key: cloudIP        value: (ip address of the cloudlet ex. "128.237.185.97")

    key: cloudPort      value: (the port number this cloudlet is listening on)
    
Heartbeat:

    key: requestType    value: heartbeat
