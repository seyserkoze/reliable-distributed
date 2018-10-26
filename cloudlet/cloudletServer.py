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
    # filename = form['zip'].filename
    # data = form['zip'].file.read()
    # print(data)
    # f = open("/tmp/%s"%filename, "wb")
    # f.write(data)
    # f.close()
    reqType = form['requestType'].value
    #only decode if it isn't already in string form
    try:
      reqType = reqType.decode('utf-8')
    except AttributeError:
      pass
    if reqType == "newPhotos":
      print("newPhotos, put it in the unknown dir")
    if reqType == "newJob":
      print("newJob, put it in the known dir")
    return


def run(ip, port):
  print('cloudlet server starting...')

  #ip and port of server
  print("ip address: " + ip + " port: " + str(port))
  server_address = (ip, port)
  httpd = HTTPServer(server_address, CloudletHTTPRequestHandler)
  print('cloudlet server running...')
  httpd.serve_forever()