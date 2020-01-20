#!/usr/bin/python

import uuid
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
from config import SWFConfig
import sys
import os

bucket = 'muminovic.actualit.info'

botoConfig = Config(connect_timeout=50, read_timeout=70)
swf = boto3.client('swf', config=botoConfig)
s3 = boto3.resource(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=SWFConfig.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=SWFConfig.AWS_SECRET_ACCESS_KEY
)
        
def uploadToS3(file, bucket, name):
    try:
        s3.meta.client.upload_file(file, bucket, name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
def listObjects(bucketName):
    return s3.meta.client.list_objects_v2(Bucket=bucketName)

def downloadFile(bucket, filename, localName):
    try:
        s3.meta.client.download_file(bucket, filename, localName)
        print("Successfuly downloaded")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
#hello = lambda x: print(x)
#captializeFirstLetter = lambda message: print(message.capitalize())

print('Listening for Worker Tasks')

activities = {
    "uploadCSVToS3Bucket": uploadToS3(sys.argv[1], bucket, sys.argv[2]),
    'listBuckets' : listObjects(bucket),
    'downloadFile': downloadFile(bucket, sys.argv[2], sys.argv[3])
}


while True:
    # Used by workers to get an ActivityTask from the specified activity taskList.
    task = swf.poll_for_activity_task(
        # The name of the SWFConfig.DOMAIN that contains the task lists being polled.
        domain=SWFConfig.DOMAIN,
        # Specifies the task list to poll for activity tasks.
        taskList={'name': SWFConfig.TASK_LIST_NAME},
        # Identity of the worker making the request
        identity=f'worker-{uuid.uuid4()}')

    if 'taskToken' not in task or not task['taskToken']:
        print('Poll timed out, no new task. Repoll')
    else:
        print('New task arrived')

        print('tasks :', task)

        activity_type_name = task['activityType']['name']
        input_param = task['input']

        if activity_type_name in activities:
            
            upload = uploadToS3(sys.argv[1], bucket, sys.argv[2])           
            print(upload)
            
            buckets = listObjects(bucket)
            print(buckets)
            
            download = downloadFile(bucket, sys.argv[2], sys.argv[3])

            swf.respond_activity_task_completed(
                taskToken=task['taskToken'],
                result=str(activities)
            )

            print('Task Done', activities)
        else:
            print(f'Activity type {activity_type_name} not found!')