import sys
import requests
import os
import argparse
import time

parser = argparse.ArgumentParser(description='Upload images')
parser.add_argument('--num_request', type=int, help='one image per request')
parser.add_argument('--url', type=str, help='URL of your backend server, e.g. http://3.86.108.221/xxxx.php')
parser.add_argument('--image_folder', type=str, help='the path of the folder where images are saved on your local machine')
args = parser.parse_args()

def send_one_request(url, image_path):
    # Define http payload, "myfile" is the key of the http payload
    file = {"myfile": open(image_path,'rb')}
    r = requests.post(url, files=file)
    # Print error message if failed
    if r.status_code != 200:
        print('sendErr: '+r.url)
    else :
        print(r.text)

def send_response_queue_request(url, num):
    r = requests.post(url + '/response_queue', data = {'num': num})
    if r.status_code != 200:
        print("Error")
        print(r.request)

def get_results(url):
    print("get request python")
    r = requests.get(url)
    print(r.content.decode())
    return r.content.decode()


num_request = args.num_request
url = args.url
image_folder = args.image_folder
# Iterate through all the images in your local folder
for i, name in enumerate(os.listdir(image_folder)):
    if i == num_request:
        break
    image_path = image_folder + name
    send_one_request(url, image_path)
    time.sleep(0.5)

send_response_queue_request(url, num_request)

while True:
    r = requests.get(url)
    if "Error" in r.content.decode():
        time.sleep(5)

    elif "(" in r.content.decode():
        broken_string = r.content.decode().split('\n')
        length = len(broken_string)

        if num_request == 1:

            print(r.content.decode())
            new_r = requests.get(url + "/kill")
            sys.exit(0)
        if length - 1 == num_request:


            print(r.content.decode())
            new_r = requests.get(url + "/kill")
            sys.exit(0)
    else:
        time.sleep(5)
