import json
import boto3

from Maho_bot import Maho

def get_instance_id(path):
    ssm = boto3.client('ssm')
    args = {"Name": path, "WithDecryption": True}
    param = ssm.get_parameter(**args)

    return json.loads(param['Parameter']['Value'])

def main():
    creds = get_instance_id('minecraft')
    client = Maho()
    client.run(creds['maho_bot_token'])

if __name__ == "__main__":
    main()