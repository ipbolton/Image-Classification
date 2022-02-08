import main
import time

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
            if instance_id == "i-05863669b7cca308b":
                instance_list.append(public_ip)
    return instance_list

ec2 = main.get_ec2_client()
response = ec2.start_instances(InstanceIds=["i-05863669b7cca308b"], DryRun=False)
print(response)
time.sleep(45)
temp = str(get_running_instances()[0])
hold = temp.replace(".", "-")
return_string = "http://ec2-" + hold + ".compute-1.amazonaws.com:3000"
print("IP of web server", return_string)
