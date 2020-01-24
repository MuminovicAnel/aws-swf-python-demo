#!/usr/bin/python

import uuid
import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
from config import SWFConfig
import sys

botoConfig = Config(connect_timeout=50, read_timeout=70)
swf = boto3.client('swf', config=botoConfig)
s3 = boto3.resource(
    's3',
    # Hard coded strings as credentials, not recommended.
    #aws_access_key_id=SWFConfig.AWS_ACCESS_KEY_ID,
    #aws_secret_access_key=SWFConfig.AWS_SECRET_ACCESS_KEY,
    #region_name=SWFConfig.REGION_NAME
)
        
def uploadToS3FromLocal(file, bucket, name):
    try:
        return s3.meta.client.upload_file(file, bucket, name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
def listObjects(bucketName):
    try:
        return s3.meta.client.list_objects_v2(Bucket=bucketName)
        print("Successfuly listed buckets")
        return True
    except Exception as e:
        print('Error in listing buckets: ', e.response.get('Error', {}).get('Code'))
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def downloadFileFromS3(bucket, filename, localName):
    try:
        return s3.meta.client.download_file(bucket, filename, localName)
        print("Successfuly downloaded")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

print('Listening for Worker Tasks')

activities = {
    "uploadToS3": "copyToBucket",
    "listBuckets" : "listObjects",
    "downloadFileFromS3": 'downloadFileFromS3'
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

            upload = uploadToS3FromLocal(sys.argv[2], sys.argv[1], sys.argv[3]) 
            print(upload)          
            
            buckets = listObjects(sys.argv[1])
            for bucket in buckets['Contents']:
                print(bucket)
            
            download = downloadFileFromS3(sys.argv[1], sys.argv[3], sys.argv[4])
            print(download)
            
            """ copy_source = {'Bucket': sys.argv[1], 'Key': sys.argv[2]}
            copy = copyFromSourceToTargetBucket(copy_source, sys.argv[3], sys.argv[4])           
            print(copy) """

            swf.respond_activity_task_completed(
                taskToken=task['taskToken'],
                result=str(activities)
            )

            print('Task Done', activities)

            exit()
        else:
            print(f'Activity type {activity_type_name} not found!')