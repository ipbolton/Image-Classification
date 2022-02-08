import image_classification
#import request_queue
import response_queue
import ec2_instance_manager
import convert_image
import requests
import main


response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = response.text
print("Started instance (worker):", instance_id)
client = main.get_sqs_resource()
queue = client.get_queue_by_name(QueueName='request_queue_official')

queue_size = int(queue.attributes['ApproximateNumberOfMessages'])

while queue_size > 0:
    for msg in queue.receive_messages(MaxNumberOfMessages=10, MessageAttributeNames=['image_name']):
        print("Queue size:", queue_size)


        print("Getting string image from request queue")
        request_string = msg.body
        image_filename = convert_image.convert_image_to_jpeg(request_string, str(msg.message_attributes.get('image_name').get('StringValue')))
        print("Finished converting image")

        classification_result = image_classification.image_classification(image_filename)

        return_string = image_filename + ", " + classification_result

        # Send classified image to response queue
        response_queue.send_image_to_response_queue(return_string, str(msg.message_attributes.get('image_name').get('StringValue')))

        # Send result to S3
        print("Result sent to S3")
        convert_image.send_result_S3(return_string)

        print("Removing image from request queue")
        msg.delete()

        # Get queue size
    queue_size = int(queue.attributes['ApproximateNumberOfMessages'])

ec2_instance_manager.stop_instance(instance_id)
