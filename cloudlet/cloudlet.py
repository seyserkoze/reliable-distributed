import cloudletServer
import cloudletClient
import cloudletSettings

cloudletSettings.init_settings()
cloudletClient.init_cloudlet()
cloudletServer.run(cloudletSettings.my_ip, cloudletSettings.my_port)
