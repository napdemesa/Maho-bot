import os
import time
import sys
import paramiko
from mcstatus import MinecraftServer
#from ec2_instance_control import turn_instance_on as tio
sys.path.insert(0, '/home/ec2-user/Maho-bot/ec2_instance_control')
import turn_instance_on as ec2


def check_minecraft_server_status(instance_ip):
    try:
        server = MinecraftServer.lookup(instance_ip)
        status = server.status()
        message = f"The server has {status.players.online} players and replied in {status.latency} ms"
        mc_server_online = True

        return mc_server_online, message
    except Exception:
        message = 'The server is currently not on.'
        mc_server_online = False

        return mc_server_online, message


def turn_server_on(instance_status, instance_ip):
    timeout = 30

    if instance_status:
        print(instance_ip)
        #instance_status, instance_message, instance_ip = ec2.check_instance_status()
        status, message = check_minecraft_server_status(instance_ip)
        if status:
            print('minecraft server is online')
            return status, message
        else:
            print('minecraft server is offline... starting up server...')
            try:
                print(instance_ip)
                key = paramiko.RSAKey.from_private_key_file('/home/ec2-user/Maho-bot/maho_bot/mc_server.pem')
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print('key works')
                ssh.connect(hostname=instance_ip, username="ec2-user", pkey=key)
                print('connected to instance')
                #stdin, stdout, stderr = 
                #stdin, stdout, stderr = ssh.exec_command('yes')
                #print(stdout.read())

                stdin, stdout, stderr = ssh.exec_command('nohup bash /home/ec2-user/server/run_server.sh &')
                print('executed')
                #stdout.channel.recv_exit_status()
                while True:
                    line = stdout.readline()
                    if line:
                        break
                    if not line:
                        break
                    print(line, end='')

                print(':eyes:')
                ssh.close()

                while True:
                    status, message = check_minecraft_server_status(instance_ip)
                    if status:
                        break
                print(message)
                if status:
                    return status, message
                else:
                    return status, message
            except Exception as e:
                print(e)


def turn_server_off(instance_status, server_status):
    if server_status:
        pass
            
