import cloudletServer
import cloudletClient
import cloudletSettings
import sys
import threading

if len(sys.argv) != 5:
    print("Please provide the following command line arguments:")
    print("arg1: ip of primary server")
    print("arg2: ip of secondary server")
    print("arg3: the port this cloudlet will listen on")
    print("arg4: the heartbeat interval")
    sys.exit()

cloudletSettings.init_settings(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
print("Connecting to servers: " + cloudletSettings.servers[0] + " and " + cloudletSettings.servers[1])
cloudletClient.init_cloudlet()
#heartbeats
heartbeat = threading.Thread(target=cloudletClient.heartbeat)
heartbeat.start()
#setup jobs
jobs = threading.Thread(target=cloudletClient.getJobs)
jobs.start()
cloudletServer.run(cloudletSettings.my_ip, cloudletSettings.my_port)
