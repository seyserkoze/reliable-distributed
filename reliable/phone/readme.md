# Phone


### Prerequisites

requests library: http://docs.python-requests.org/en/master/
geocoder: 

### Phone Commmunication

#### Initialization with the Server:

To initialize itself(everything here is a string):

    key: requestType    value: phoneJoinReq

    key: id             value: 1

##### To the Cloudlet

To submit unknown photos for processing:

    key: requestType    value: newPhotos

    key: zip            value: (zip file containing the photos to check, name can by anything)

To tell the cloudlet you're leaving:
    
    key: requestType    value: leave

##TODO:  
GUI  
parse location from image metadata
get location for images without location metadata
