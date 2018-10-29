import cloudletServer
import cloudletClient
import cloudletSettings

cloudletSettings.init_settings()
cloudletClient.init_cloudlet()
cloudletServer.run(settings.my_ip, settings.my_port)
