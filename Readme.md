## aws-swf-boto3-demo

Amazon Simple Workflow Service Demo Application in python with boto3



#### Requirements

- [python](https://www.python.org/downloads/)

- An active [AWS account](http://aws.amazon.com/) with [Access Keys](http://docs.amazonwebservices.com/AWSSecurityCredentials/1.0/AboutAWSCredentials.html#AccessKeys)

- [Boto3 SWF documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#id44)



#### How it works

Go to config.py and add your infos

```
DOMAIN = 'your_domain'
AWS_ACCESS_KEY_ID = 'your_access_key_id'

AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
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
python worker.py file_to_upload_to_s3 new_name_to_s3 name_downloaded_file
```

start the workflow execution

```python
python start_workflow.py
```


