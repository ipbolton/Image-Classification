import boto3
import main

# This function converts a jpeg image to a string
def convert_image_to_string(file):
    import base64

    with open(file, "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())

    with open('encode.bin', "wb") as file:
        file.write(converted_string)

    return converted_string


# This function converts the string image to it's original format
def convert_image_to_jpeg(converted_string, name):
    import base64

    image_data = base64.b64decode(converted_string)
    image_filename = name
    with open(image_filename, 'wb') as f:
        f.write(image_data)

    return image_filename



# This function sends the result to the output bucket in S3 to be stored
def send_result_S3(result):
    # Putting results into a text file:
    write_file = result + ".txt"
    f = open(write_file, "w+")
    f.write(result)

    # Sending text file to S3:
    s3 = main.get_s3_client()

    with open(write_file, 'rb') as f:
        s3.upload_fileobj(f, 'output-bucket-cse-546', write_file)
    return
