import socket
import os
import _thread

def init_settings(add1, add2, port):
    global jobs
    global servers
    global current_serv
    global my_ip
    global my_port
    global known_dir
    global unknown_dir
    global unique_id
    global server_num
    global lock
    jobs = {}
    servers = ['http://' + add1 + ":80", 'http://' + add2 + ":80"]
    server_num = 0
    current_serv = servers[server_num]
    my_ip = socket.gethostbyname(socket.gethostname())
    my_port = int(port)
    known_dir = os.path.join(os.getcwd(), "__known")
    unknown_dir = os.path.join(os.getcwd(), "__unknown")
    unique_id = 0
    lock = _thead.allocate_lock()


def switch_server():
    global server_num
    global servers
    global current_serv
    global lock
    lock.acquire()
    server_num = (server_num + 1) % 2 #switch between 0 and 1
    current_serv = servers[server_num]
    lock.release()
    return