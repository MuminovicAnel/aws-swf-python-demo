import boto3
from botocore.exceptions import ClientError

swf = boto3.client('swf')

class SWFConfig(object):
	WORKFLOW = "upload-to-s3-bucket"
	WORKFLOW_VERSION = "0.4"
	TASK_LIST_NAME = "swf-task-list"

	ACTIVITY_LIST = [
			{'name': 'uploadToS3', 'version': '0.4'},
			{'name': 'listBuckets', 'version': '0.4'},
			{'name': 'downloadFileFromS3', 'version': '0.4'},
	]

	DOMAIN = 'upload-file-S3-v2'
