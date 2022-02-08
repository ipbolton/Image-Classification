import boto3


def get_sqs_resource():
    resource = boto3.resource('sqs', region_name='us-east-1',
                            aws_access_key_id='AKIAQLAIBKNOGQAPMNXW',
                            aws_secret_access_key='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')
    return resource


def get_sqs_client():
    client = boto3.client('sqs', region_name='us-east-1',
                            aws_access_key_id='AKIAQLAIBKNOGQAPMNXW',
                            aws_secret_access_key='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')
    return client

def get_s3_client():
    s3 = boto3.client('s3', region_name='us-east-1',
                      aws_access_key_id='AKIAQLAIBKNOGQAPMNXW',
                      aws_secret_access_key='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')
    return s3

def get_ec2_client():
    ec2 = boto3.client('ec2', region_name='us-east-1',
                      aws_access_key_id='AKIAQLAIBKNOGQAPMNXW',
                      aws_secret_access_key='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')
    return ec2
