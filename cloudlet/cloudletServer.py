from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from io import BytesIO
import json
import ast
import cgi

#Create custom HTTPRequestHandler class
class CloudletHTTPRequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
    print("post received")
    self.send_response(200)
    self.end_headers()
    form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
    filename = form['zip'].filename
    data = form['zip'].file.read()
    f = open(os.path.join(os.getcwd(), "tmp", filename), "wb")
    f.write(data)
    f.close()
    reqType = self.getKeyValue(form, "requestType")
    if reqType == "newPhotos":
      print("newPhotos, put it in the unknown dir")
      #create a directory with a unique name to search against known dirs
    if reqType == "newJob":
      jobName = self.getKeyValue(form, "jobName")
      print("New Job received: %s", jobName)
      #make a directory with the job name and register it
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
  print('cloudlet server starting...')

  #ip and port of server
  print("ip address: " + ip + " port: " + str(port))
  server_address = (ip, port)
  httpd = HTTPServer(server_address, CloudletHTTPRequestHandler)
  print('cloudlet server running...')
  httpd.serve_forever()