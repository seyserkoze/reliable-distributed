from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from io import BytesIO
import json
import ast
import cgi
import cloudletClient
import cloudletSettings as settings

#Create custom HTTPRequestHandler class
class CloudletHTTPRequestHandler(BaseHTTPRequestHandler):

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

    if reqType == "newPhotos":
      print("New photo set received for processing")
      filename = form['zip'].filename
      data = form['zip'].file.read()
      fp = open(os.path.join(settings.unknown_dir, filename), "wb")
      fp.write(data)
      fp.close()
      #call the client to search against it
      cloudletClient.processPhotos(filename)

    elif reqType == "newJob":
      #make a directory with the job name and register it
      filename = form['zip'].filename
      jobName = filename[:-4]
      print("New Job received: " + jobName)
      data = form['zip'].file.read()
      jobPath = os.path.join(settings.known_dir, jobName)
      os.makedirs(jobPath)
      fp = open(os.path.join(jobPath, filename), "wb")
      fp.write(data)
      fp.close()
      #call the client to unzip it and add the job
      cloudletClient.newJob(jobName)

    elif reqType == "deleteJob":
      jobName = self.getKeyValue(form, "jobName")
      print ("Deleting Job: " +  jobName + "...")
      cloudletClient.deleteJob(jobName)

    elif reqType == "leave":
      cloudletClient.leave()

    return

  #gets the value from the form and decodes it to a string if necessary
  def getKeyValue(self, form, key):
    value = form[key].value
    #only decode if it isn't already in string form
    try:
      value = value.decode('utf-8')
    except AttributeError:
      pass
    return value


def run(ip, port):
  print('Cloudlet server starting...')

  #ip and port of server
  print("Cloudlet IP address: " + ip + " port: " + str(port))
  server_address = (ip, port)
  httpd = HTTPServer(server_address, CloudletHTTPRequestHandler)
  print('Cloudlet server running...')
  httpd.serve_forever()