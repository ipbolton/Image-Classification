# Image-Classification
An application built to perform distributed bulk image classification using AWS services.

## Infrastructure
The application uses a NodeJS server as the front-end, where a user may specify a folder of images to be classified. These images are read in and passed into an SQS request queue. This queue uses a FIFO structure. Following this, The images are evenly distributed amongst a total of twenty (20) EC2 instances, as well as an S3 bucket for persistent storage. This action is performed using an algorithm in `controller.py`. The model has been pre-installed on each of these instances, reducing spin-up time. Upon classification of an image, the corresponding EC2 instance will pass the result to a response SQS Queue, which then displays the classification results to the end user. Upon completion of a classification task, the EC2 instance will spin-down if no images remain in the request queue.
