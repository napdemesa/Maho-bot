import os
import sys
import json
import boto3
#import paramiko
from botocore.exceptions import ClientError
#from mcstatus import MinecraftServer

#sys.path.insert(0, '/home/ec2-user/Maho-bot/mc_server')
#import turn_mc_server_on as mcs


def get_instance_id(path):
    ssm = boto3.client('ssm')
    args = {"Name": path, "WithDecryption": True}
    param = ssm.get_parameter(**args)

    return json.loads(param['Parameter']['Value'])


def check_instance_status():
    instance = get_instance_id('minecraft')
    instance_id = instance['INSTANCE_ID']
    ec2 = boto3.client('ec2')

    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    try:
        #print(response)
        if response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
            instance_online = True
            another_response = ec2.describe_instances(InstanceIds=[instance_id])

            return instance_online, 'Instance online', f"IP: {another_response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']}", 

    except Exception as e:
        instance_online = False
        return instance_online, 'Instance offline', 'IP: '


def turn_instance_on():
    instance = get_instance_id('minecraft')
    instance_id = instance['INSTANCE_ID']
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
        return True, response
    except ClientError as e:
        print(e)
        return False

    return


def turn_instance_off():
    instance = get_instance_id('minecraft')
    instance_id = instance['INSTANCE_ID']
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
        return True, response
    except ClientError as e:
        print(e)
        return False


#def main():
#    instance_id = get_instance_id('minecraft')
#    instance_status = check_instance_status(instance_id['INSTANCE_ID'])

    #mcs.turn_server_on(instance_status)

    #turn_instance_on(instance_id['INSTANCE_ID'])
    #turn_instance_off(instance_id['INSTANCE_ID'])

    #check_minecraft_server_status()


#if __name__ == "__main__":
#    main()