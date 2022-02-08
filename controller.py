#from numpy.lib.function_base import diff
import ec2_instance_manager
import boto3
import time
import main


def auto_scale_instances():
    client = main.get_sqs_resource()
    queue = client.get_queue_by_name(QueueName='request_queue_official')
    queue_length = int(queue.attributes['ApproximateNumberOfMessages'])

    print("Request queue length:", queue_length)

    if queue_length == 0:
        print("Queue is empty, shutting down all instances (downscaling)")
        return

    else:
        running_instances = ec2_instance_manager.get_running_instances()
        running_instances_size = len(running_instances)
        print("Running instances:", running_instances)
        if running_instances_size == 19:
            print("Im at max capacity")
            return


        # we need to scale up
        if running_instances_size < queue_length:
            stopped_instances = ec2_instance_manager.get_stopped_instances()
            num_of_available_instaces = len(stopped_instances)

            del_num = num_of_available_instaces - queue_length
            print("del num", del_num)
            if del_num > 0:
                temp_list = stopped_instances
                del temp_list[:del_num]
                ec2_instance_manager.bulk_start_instances(temp_list)
            if del_num < 0:
                ec2_instance_manager.bulk_start_instances(stopped_instances)


        else:
            return

while True:
    print("starting auto scaling")
    auto_scale_instances()
    time.sleep(30)
