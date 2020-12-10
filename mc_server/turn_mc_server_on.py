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
            os.system('java -Xmx1024M -Xms1024M -jar home/ec2-user/Maho-bot/mc_server/server.jar nogui')
            idx = 0
            animation = '.....'
            while not check_minecraft_server_status():
                print(animation[idx % len(animation)], end="\r")
                idx += 1
                time.sleep(0.1)
                #print('waiting for server to load...')
            check_minecraft_server_status()
