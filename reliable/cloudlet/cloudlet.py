import cloudletServer
import cloudletClient
import cloudletSettings
import sys
import _thread

if len(sys.argv) != 5:
    print("Please provide the following command line arguments:")
    print("arg1: ip of server 1")
    print("arg2: ip of server 2")
    print("arg3: the port this cloudlet will listen on")
    print("arg4: the heartbeat interval")
    sys.exit()

heartbeat_interval = int(sys.argv[4])
cloudletSettings.init_settings(sys.argv[1], sys.argv[2], sys.argv[3])
print("Connecting to servers: " + cloudletSettings.servers[0] + " and " + cloudletSettings.servers[1])
cloudletClient.init_cloudlet()
#heartbeats
_thread.start_new_thread(cloudletClient.heartbeat(), (heartbeat_interval, ))
cloudletServer.run(cloudletSettings.my_ip, cloudletSettings.my_port)
