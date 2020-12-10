import os
import time
from mcstatus import MinecraftServer
#from ec2_instance_control import turn_instance_on as tio


def check_minecraft_server_status():
    server = MinecraftServer.lookup("3.129.206.49")
    try:
        status = server.status()
        print(f"The server has {status.players.online} players and replied in {status.latency} ms")
        mc_server_online = True
    except Exception:
        #print('The server is currently not on.')
        mc_server_online = False

    return mc_server_online


def turn_server_on(instance_status):
    if instance_status:
        if check_minecraft_server_status():
            print('minecraft server is online')
        else:
            print('minecraft server is offline... starting up server...')
            try:
                os.system('bash run_server.sh')
                check_minecraft_server_status()
            except Exception as e:
                print(e)
            
