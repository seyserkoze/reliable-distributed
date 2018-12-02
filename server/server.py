from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from io import BytesIO
import json
import ast
import socket
import cgi
import sys
import requests

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
    self.send_response(200)
    self.end_headers()
    form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
          'CONTENT_TYPE':self.headers['Content-Type'],
          })

    reqType = self.getKeyValue(form, "requestType")

    if(reqType == 'phoneJoinReq'):
      print("PHONE JOIN REQUEST RECEIVED")
      response = simpleLB()
      response = json.dumps(response)
      print("PHONE WAS ASSIGINED TO CLOUDLET: ",response)
      self.wfile.write(response.encode('utf-8'))
    elif(reqType == 'cloudJoinReq'):
      print("CLOUDLET JOIN REQUEST RECEIVED")
      cloudletIP = self.getKeyValue(form,"cloudIP")
      cloudletPort = self.getKeyValue(form,"cloudPort")

      addToCurrentCloudlets(cloudletIP, cloudletPort)

      print("CLOUDLET STATE WAS UPDATED")
    elif(reqType == "match"):
      filename = form['zip'].filename
      data = form['zip'].file.read()
      fp = open(os.path.join('./results/', filename), "wb")
      fp.write(data)
      fp.close()
    elif(reqType == "getState"):
      print("RECEIVED GET STATE REQUEST FROM SECONDARY")
      with open('cloudletStore.json', "r") as f:
        data = json.load(f)
        curr = json.dumps(data)
        self.wfile.write(curr.encode('utf-8'))
    elif(reqType == "updateState"):
      print("RECEIVED UPDATE STATE REQUEST FROM PRIMARY")
      print("")
      data = form['zip'].file.read()
      fp = open('cloudletStore.json', "wb")
      fp.write(data)
      fp.close()
      print("STATE WAS UPDATED TO MATCH PRIMARY")
    elif(reqType == 'phoneLeaveReq'):
      cloudletIP = self.getKeyValue(form,"cloudIP")
      cloudletPort = self.getKeyValue(form,"cloudPort")
      leaveCloudlet(cloudletIP, cloudletPort)

    elif(reqType == 'getJobs'):
      check = 0
      for fileVal in os.listdir("../reliable/reliablemedia/lookup/"):
        if(fileVal.endswith('.zip')):
          files = {'requestType': 'newJob', 'zip':open(fileVal,'rb')}
          r = requests.post("http://"+cloudletIP+":"+cloudletPort, files=files)
          check = 1
      if(check): print("ALL JOBS SENT TO NEW CLOUDLET")
    return


  def getKeyValue(self,form, key):
    value = form[key].value

    try:
      value = value.decode('utf-8')
    except AttributeError:
      pass
    return value

def leaveCloudlet(cloudletIP, cloudletPort):
  with open('cloudletStore.json', 'r') as f:
    data = json.load(f)
  fullAddress = cloudletIP + ":" + cloudletPort
  data[fullAddress] -= 1

  with open('cloudletStore.json','w') as f:
    json.dump(data,f)

def addToCurrentCloudlets(cloudletIP, cloudletPort):
  print("HERE")
  flag = 0
  if(not(os.path.exists('cloudletStore.json'))):
    with open('cloudletStore.json', "w") as f:
      data = {}
      data[str(cloudletIP) + ":" + str(cloudletPort)] = 0
      json.dump(data,f)
  else:
    with open('cloudletStore.json','r') as f:
      data = json.load(f)

    data[str(cloudletIP) + ":" + str(cloudletPort)] = 0

    with open('cloudletStore.json','w') as f:
      json.dump(data, f)


def simpleLB():
  if(not(os.path.exists('cloudletStore.json'))):
    return {'IP':'-1', 'port':'-1'}
  else:
    with open('cloudletStore.json', 'r') as f:
      data = json.load(f)
    minVal = -1
    parse = ""
    for key,val in data.items():
      if(minVal == -1 or val < minVal):
        minVal = val
        parse = key
    data[parse] += 1

    with open('cloudletStore.json','w') as f:
      json.dump(data,f)

    cloudletIP = "0"
    cloudletPort = "0"
    if(parse != ""):
      currIndex = parse.find(":")
      cloudletIP = parse[:currIndex]
      cloudletPort = parse[currIndex+1:]
    return {'IP':cloudletIP, 'port':cloudletPort}


def run():
  print('http server is starting...')
  argList = sys.argv
  print(str(argList))
  serverPort = argList[2]
  serverIP = argList[1]
  #ip and port of servr
  #by default http server port is 80
  server_address = (serverIP, int(serverPort))

  with open('cloudletStore.json','w') as f:
    data = {}
    json.dump(data, f)
  httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()





if __name__ == '__main__':
  run()
