## aws-swf-boto3-demo

Amazon Simple Workflow Service Demo Application in python with boto3



#### Requirements

- [python](https://www.python.org/downloads/)

- An active [AWS account](http://aws.amazon.com/) with [Access Keys](http://docs.amazonwebservices.com/AWSSecurityCredentials/1.0/AboutAWSCredentials.html#AccessKeys)

- [Boto3 SWF documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#id44)



#### How it works

Go to config.py and add your infos

```
WORKFLOW = "upload-to-s3-bucket"
WORKFLOW_VERSION = "0.3"
TASK_LIST_NAME = "swf-task-list"

ACTIVITY_LIST = [
    {'name': 'uploadToS3', 'version': '0.3'},
	{'name': 'listBuckets', 'version': '0.3'},
	{'name': 'downloadFileFromS3', 'version': '0.3'},
]

DOMAIN = 'upload-file-S3-v2'
AWS_SECRET_ACCESS_KEY = ''
AWS_ACCESS_KEY_ID = ''
```

Register the workflow

```python
python register.py
```

Run the decider

```python
python decider.py
```

Run the worker, he uses 3 arguments (string)

```python
python worker.py target_bucket filename filename_key path_downloaded_file
```

start the workflow execution

```python
python start_workflow.py
```


