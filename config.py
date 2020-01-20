import boto3
from botocore.exceptions import ClientError

class SWFConfig(object):
	WORKFLOW = "upload-to-s3-bucket"
	WORKFLOW_VERSION = "1"
	TASK_LIST_NAME = "swf-task-list"

	ACTIVITY_LIST = [
			'uploadCSVToS3Bucket',
			'listBuckets',
			'downloadFile'
	]
	AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
	DOMAIN = 'your_domain'
	AWS_ACCESS_KEY_ID = 'your_access_key_id'
