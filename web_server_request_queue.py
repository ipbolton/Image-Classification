# Make modifications to the request queue here:
import main
import sys
import base64

images_path = "/home/ubuntu/upload_images/"
firstarg=sys.argv[1]

def uploadPicture(picPath, bucketName, s3Name):
    client = main.get_s3_client()
    client.upload_file(picPath, bucketName, s3Name)
    print("Success uploading", picPath, " to S3")

# This function converts a jpeg image to a string
def convert_image_to_string(file):

    with open(file, "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())

    with open('encode.bin', "wb") as file:
        file.write(converted_string)

    return converted_string


# This function sends an image to the Request Queue
def send_image_to_request_queue(file):
    #import main
    resource = main.get_sqs_resource()

    converted_string = convert_image_to_string(file)

    # Sending image to request queue:
    queue = resource.get_queue_by_name(QueueName='request_queue_official')
    response = queue.send_message(MessageBody=str(converted_string),MessageAttributes = {
        'image_name': {
            "StringValue": firstarg,
            "DataType": "String"

        }
    })
    print("Image:", file, "sent to queue as string")
    return response



send_image_to_request_queue(images_path + firstarg)
uploadPicture(images_path + firstarg, 'cse-546-picture-files', firstarg)
