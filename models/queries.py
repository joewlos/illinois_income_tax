# -*- coding: utf-8 -*-
'''
AMAZON DYNAMODB QUERIES
'''
# Import required packages for Amazon DynamoDB
from boto3.dynamodb.conditions import Attr, Key
from resource import dynamodb

# Sessions tables includes edits to taxes with location as secondary index
sessions = dynamodb.Table('ILTaxSessions')

# Get submitted items from the table using secondary index
def get_all_submit_items():
	response = sessions.scan(IndexName='ILTaxSessionsIndex')
	return response['Items'], response['Count']

# Get specific submit item
def get_specific_submit_item(session_id):
	response = sessions.query(
		KeyConditionExpression=Key('session_id').eq(session_id),
		FilterExpression=Attr('type').contains('submit')
	)
	return response['Items']