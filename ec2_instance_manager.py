import boto3
import main


def create_key_pair():
    print("Creating key pair")
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    key_pair = ec2_client.create_key_pair(KeyName="my_ec2_key")
    private_key = key_pair["KeyMaterial"]
    private_key_file=open("my_ec2_key","w")
    private_key_file.write(private_key)
    private_key_file.close
    print("Finished creating key pair")

def get_public_ip(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))

def create_instance():
    print("Creating new instance")
    ec2_client = main.get_ec2_client()
    instances = ec2_client.run_instances(
        ImageId="ami-0f1955d89b939abdf",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="my_ec2_key"
    )
    print("Done creating instance")
    print("Instance id:", instances["Instances"][0]["InstanceId"])

def bulk_create_instances(num):
    print("Starting bulk create of", num, "instances")
    for i in range(num):
        create_instance()

def start_instance(instance_id):
    print('Starting instance with ID:',instance_id)
    ec2 = main.get_ec2_client()
    response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
    print(response)
    #update_instance_state(instanceid,1) # setting value for this instance as one in s3 bucket.

def bulk_start_instances(instance_ids):
    print("Starting these instances", instance_ids)
    for i in instance_ids:
        start_instance(i)

def stop_instance(instance_id):
    print("Stopping instance:", instance_id)
    ec2_client = main.get_ec2_client()
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    print(response)

def bulk_stop_instances(instance_ids):
    instance_ids.remove("i-0c6fe4c893fc48b1d")
    instance_ids.remove("i-0371c9aaf4fa78271")
    #i-0885788ef6811d11e
    print("Stopping these instances", instance_ids)
    for i in instance_ids:
        stop_instance(i)

def get_running_instances():
    instance_list = []
    ec2_client = main.get_ec2_client()
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running", "pending"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            if instance_id != "i-05863669b7cca308b":
                instance_list.append(instance_id)
    return instance_list

def get_stopped_instances():
    instance_list = []
    ec2_client = main.get_ec2_client()
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["stopped"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            if instance_id != "i-0c6fe4c893fc48b1d":
                instance_list.append(instance_id)
    return instance_list

def get_all_instances():
    instance_list = []
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running", "stopped"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            if instance_id != "i-0c6fe4c893fc48b1d":
                instance_list.append(instance_id)
    return instance_list

def get_stopped_instances():
    instance_list = []
    ec2_client = main.get_ec2_client()
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["stopped"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            instance_list.append(instance_id)
    print("Here are your instances:", instance_list)
    return instance_list

def terminate_instance(instance_id):
    print("Terminating instance:", instance_id)
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)

def stop_and_terminate(instance_id):
    stop_instance(instance_id)
    terminate_instance(instance_id)

def bulk_stop_and_terminate(instance_ids):
    instance_ids.remove("i-0c6fe4c893fc48b1d")
    instance_ids.remove("i-0885788ef6811d11e")
    print("Deleting these instances", instance_ids)
    for i in instance_ids:
        stop_instance(i)
        terminate_instance(i)
