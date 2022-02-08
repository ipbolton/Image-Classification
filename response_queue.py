# This function gets the results from response queue
from typing import List, Any
import main


# This function gets the first result in the response queue:
def get_first_result(response):
    first_result = {}
    first_result['Message ID'] = response['Messages'][0]['MessageId']
    first_result['Message Body'] = response['Messages'][0]['Body']
    return first_result


# This function gets all the results in the response queue:
def get_all_results(response):
    all_results = {}

    messages_length = len(response['Messages'])

    for i in range(0, messages_length):
        all_results[f'Message {i} ID '] = response['Messages'][i]['MessageId']
        all_results[f'Message {i} Body'] = response['Messages'][i]['Body']

    return all_results


# This function converts the string image to it's original format
def convert_string_to_jpeg(converted_string):
    import base64

    image_data = base64.b64decode(converted_string)
    image_filename = 'test_0_converted.JPEG'
    with open(image_filename, 'wb') as f:
        f.write(image_data)

    return image_filename


# This function gets the number of messages currently in the queue
def get_res_queue_size():
    client = main.get_sqs_client()
    response = client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/023639184220/response_queue_official',
        AttributeNames=[
        ],
        MessageAttributeNames=[
            'string',
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=10,
        WaitTimeSeconds=10,
    )

    flag = False
    size = 0
    return_statement = ''
    try:
        # Parsing json to get size:
        size = len(response['Messages'])
    except:
        flag = True
        return_statement = "Currently the size of the response queue is 0."

    if flag == False:
        return size
    else:
        return return_statement


# This function deletes a result from the response Queue
def delete_response_message():
    # Retrieving all messages in queue:
    client = main.get_sqs_client()
    response = client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/023639184220/response_queue_official',
        AttributeNames=[
        ],
        MessageAttributeNames=[
            'string'
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=10,
        WaitTimeSeconds=10,
    )


    # Asking user which message they want to delete:
    message_index = input("Enter the index of the result you want to delete: ")
    message_index = int(message_index)

    try:
        message = response['Messages'][message_index]

        receipt_handle = message['ReceiptHandle']

        # Deleting message:
        client.delete_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/023639184220/request_queue_official',
            ReceiptHandle=receipt_handle
        )
        r = f' Deleted message at index: {message_index} '
        print(r)
    except:
        print("No results are currently in the request queue!")

    return ''


# This function deletes all the messages currently in the response queue
def delete_all_response_messages():
    # Retrieving all messages in queue:
    client = main.get_sqs_client()
    response = client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/023639184220/response_queue_official',
        AttributeNames=[
        ],
        MessageAttributeNames=[
            'string'
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=10,
        WaitTimeSeconds=10,
    )

    try:
        length_queue = len(response['Messages'])
        for i in range(0, length_queue):
            message = response['Messages'][i]
            receipt_handle = message['ReceiptHandle']

            # Deleting message:
            client.delete_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/023639184220/request_queue_official',
                ReceiptHandle=receipt_handle
            )

            print(f' Deleted result at index: {i} ')
    except:
        print("No results are currently in the request queue!")
    return ' '

    # This function sends an image to the Request Queue
def send_image_to_response_queue(my_string, my_attr):
    #import main
    resource = main.get_sqs_resource()

    # Sending image to request queue:
    queue = resource.get_queue_by_name(QueueName='response_queue_official')
    response = queue.send_message(MessageBody=str(my_string), MessageAttributes = {
        'image_name': {
            'StringValue': str(my_attr),
            'DataType': 'String'
        }
    })
    print("Image sent to response queue")
    return response
