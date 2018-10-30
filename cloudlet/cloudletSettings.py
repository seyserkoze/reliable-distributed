import socket
import os

def init_settings():
    global jobs
    global serv_ip
    global serv_port
    global my_ip
    global my_port
    global known_dir
    global unknown_dir
    global unique_id
    jobs = {}
    serv_ip = 'http://128.237.185.97' 
    serv_port = 80 
    my_ip = socket.gethostbyname(socket.gethostname())
    my_port = 80
    known_dir = os.path.join(os.getcwd(), "__known")
    unknown_dir = os.path.join(os.getcwd(), "__unkown")
    unique_id = 0
    