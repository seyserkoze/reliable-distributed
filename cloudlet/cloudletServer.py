from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from io import BytesIO
import json
import ast

#Create custom HTTPRequestHandler class
class CloudletHTTPRequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
    print("post received")
    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    self.send_response(200)
    self.end_headers()
    tempBody = self.rfile.read(content_length) # <--- Gets the data itself
    body = json.loads(tempBody)
    if(body['requestType'] == 'newJob'):
       response = {'IP':'128.9.20,1', 'port':'80'}
       response = json.dumps(response)
       self.wfile.write(response.encode('utf-8'))
    elif(body['requestType'] == 'newPhotos'):
       #fill this in
       print("newPhotos request")
       photo = body['photos']
       print(photo)
       #f = body['test']
       #print(f)
    return


def run(ip, port):
  print('cloudlet server starting...')

  #ip and port of server
  print("ip address: " + ip + " port: " + str(port))
  server_address = (ip, port)
  httpd = HTTPServer(server_address, CloudletHTTPRequestHandler)
  print('cloudlet server running...')
  httpd.serve_forever()