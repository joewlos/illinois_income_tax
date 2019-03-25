# -*- coding: utf-8 -*-
'''
AMAZON DYNAMODB QUERIES
'''
# Import required packages for Amazon DynamoDB
import json
from resource import dynamodb, DecimalEncoder

# Sessions tables includes edits to taxes with location as secondary index
sessions = dynamodb.Table('ILTaxSessions')

# Add the edits or final submission to the kvs table
def put_session(data):
	response = sessions.put_item(Item=data)
	return json.dumps(response, indent=4, cls=DecimalEncoder)