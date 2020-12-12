import os
import time
from mcstatus import MinecraftServer
#from ec2_instance_control import turn_instance_on as tio


def check_minecraft_server_status():
    server = MinecraftServer.lookup("3.129.206.49")
    try:
        status = server.status()
        message = f"The server has {status.players.online} players and replied in {status.latency} ms"
        mc_server_online = True

        return mc_server_online, message
    except Exception:
        message = 'The server is currently not on.'
        mc_server_online = False

        return mc_server_online, message


def turn_server_on(instance_status, instance_ip):
    if instance_status:
        if check_minecraft_server_status():
            print('minecraft server is online')
        else:
            print('minecraft server is offline... starting up server...')
            try:
                os.system(f"ssh -i 'minecraft_server_key.pem' ec2-user@{instance_ip}")
                os.system('bash /home/ec2-user/server/run_server.sh')
                status, message = check_minecraft_server_status()
                if status:
                    return status, message
                else:
                    return status, message
            except Exception as e:
                print(e)


def turn_server_off(instance_status, server_status):
    if server_status:
        pass
            
