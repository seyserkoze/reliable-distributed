import requests
import os, os.path
import glob
import json
import sys

def main():
  argList = sys.argv
  alternateServerIP = argList[1]
  alternateServerPort = argList[2]
  currentServerStatus = argList[3]

  print("Initialized a " + currentServerStatus + " server")


  if currentServerStatus ==  'S':
    files = {'requestType': 'getState'}
    r = requests.post('http://'+alternateServerIP+":"+alternateServerPort, files=files)
    print("GOT STATE FROM PRIMARY - STATE INITIALIZED")
    with open("cloudletStore.json", "w") as f:
      currentJson = r.json()
      json.dump(currentJson, f)


  currLength = len([name for name in os.listdir('../reliable/reliablemedia/lookup/') if os.path.isfile(name)])
  currResLength = len([name for name in os.listdir('../reliable/reliablemedia/lookup/') if os.path.isfile(name)])

  flag = 0
  if((os.path.exists('cloudletStore.json'))):
    stamp = os.stat('cloudletStore.json').st_mtime
    flag = 1
  while(1):
    if(currentServerStatus == 'S'):
      try:
        files = {'requestType': 'heartbeat'}
        r = requests.post('http://'+alternateServerIP+":"+alternateServerPort, files=files, timeout=1)
      except:
        currentServerStatus = 'P'

    elif(currentServerStatus == 'P'):
      if((os.path.exists('cloudletStore.json'))):
        if(flag == 0 or os.stat("cloudletStore.json").st_mtime > stamp):
          try:
            files = {'requestType': 'heartbeat'}
            r = requests.post('http://'+alternateServerIP+":"+alternateServerPort, files=files, timeout=1)
            print("SENDING UPDATE STATE REQUEST TO SECONDARY")
            files = {'requestType': 'updateState', 'zip':open('cloudletStore.json','rb')}
            r = requests.post('http://'+alternateServerIP+":"+alternateServerPort, files=files)
          except:
            pass

        stamp = os.stat("cloudletStore.json").st_mtime
        flag = 1

      tempVar = len(os.listdir('../reliable/reliablemedia/lookup/'))
      if(currLength < tempVar):
        print('hello')
        list_of_files = glob.glob('../reliable/reliablemedia/lookup/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
        with open("cloudletStore.json", "r") as f:
          data = json.load(f)

        for key,val in data.items():
          files = {'requestType': 'newJob', 'zip':open(latest_file,'rb')}
          r = requests.post("http://"+key, files=files)
        currLength = tempVar

    '''elif(currResLength = len([name for name in os.listdir('./results/') if os.path.isfile(name)])):
       list_of_files = glob.glob('./results/*')
       latest_file = max(list_of_files, key=os.path.getctime)

print latest_file
'''
main()
