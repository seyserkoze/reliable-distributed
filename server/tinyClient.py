import requests
import os, os.path
import glob
import json

def main():
  currLength = len([name for name in os.listdir('./temp/') if os.path.isfile(name)])
  currResLength = len([name for name in os.listdir('./temp/') if os.path.isfile(name)])
  print(currLength)
  while(1):
    tempVar = len(os.listdir('./temp/'))
    if(currLength < tempVar):
      print('hello')
      list_of_files = glob.glob('./temp/*')
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
