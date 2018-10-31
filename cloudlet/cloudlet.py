import cloudletServer
import cloudletClient
import cloudletSettings
import sys

if len(sys.argv) != 2:
    print("Please provide the server IP as a command line argument")
    sys.exit()

cloudletSettings.init_settings(sys.argv[1])
cloudletClient.init_cloudlet()
cloudletServer.run(cloudletSettings.my_ip, cloudletSettings.my_port)
