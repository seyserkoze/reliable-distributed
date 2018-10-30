# Cloudlet


### Prerequisites

requests library: http://docs.python-requests.org/en/master/
face matching api: https://github.com/ageitgey/face_recognition?fbclid=IwAR1561byVmHtARls6ZWRGg5QhxETWKO2VvuCjc1T7GP1MuJC1GTemd2jhTI
check this out later for multithreading: https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python
^be careful about deleting jobs while processing them tho if you do this

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

#### Cloudlet Requests to server:

To initialize itself(everything here is a string):
    key: requestType    value: cloudJoinReq
    key: id             value: 1
    key: cloudIP        value: (ip address of the cloudlet ex. "http://128.237.185.97")
    key: cloudPort      value: (the port number this cloudlet will listen on)

To send found matches to the server:
    key: requestType    value: match
    key: zip            value: (zipfile containing the matches, name of the zipfile will be the name of the job)
