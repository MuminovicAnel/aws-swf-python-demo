import uuid
import boto3
from config import SWFConfig

swf = boto3.client('swf')
    
start_workflow = swf.start_workflow_execution(
	domain=SWFConfig.DOMAIN,
	workflowId=f'test-{uuid.uuid4()}',
	workflowType={
		"name": SWFConfig.WORKFLOW,# string
		"version": SWFConfig.WORKFLOW_VERSION # string
	},
	taskList={
			'name': SWFConfig.TASK_LIST_NAME
	},
	input='Upload'
)

print("Workflow requested: ", start_workflow)