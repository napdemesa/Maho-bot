import os
import json

import boto3
from botocore.exceptions import ClientError
from mcstatus import MinecraftServer


def get_instance_id(path):
    ssm = boto3.client('ssm')
    args = {"Name": path, "WithDecryption": True}
    param = ssm.get_parameter(**args)

    return json.loads(param['Parameter']['Value'])


def check_instance_status(instance_id):
    ec2 = boto3.client('ec2')

    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    try:
        if response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
            instance_online = True
            print('server online')
    except Exception:
        instance_online = False
        print('server offline')

    return instance_online


def turn_instance_on(instance_id):
    ec2 = boto3.client('ec2')

    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

    return


def turn_instance_off(instance_id):
    ec2 = boto3.client('ec2')
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

    return


def check_minecraft_server_status():
    server = MinecraftServer.lookup("3.21.241.184")
    try:
        status = server.status()
        print(f"The server has {status.players.online} players and replied in {status.latency} ms")
        mc_server_online = True
    except Exception:
        print('The server is currently not on.')
        mc_server_online = False

    return mc_server_online


def main():
    instance_id = get_instance_id('minecraft')
    instance_status = check_instance_status(instance_id['INSTANCE_ID'])
    if instance_status:
        if check_minecraft_server_status():
            print('minecraft server is online')
        else:
            print('minecraft server is offline... starting up server...')
            os.system('java -Xmx1024M -Xms1024M -jar server.jar nogui')
            while not check_minecraft_server_status():
                print('waiting for server to load...')
            check_minecraft_server_status()

    turn_instance_on(instance_id['INSTANCE_ID'])
    turn_instance_off(instance_id['INSTANCE_ID'])

    #check_minecraft_server_status()


if __name__ == "__main__":
    main()