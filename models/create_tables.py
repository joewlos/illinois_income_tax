# -*- coding: utf-8 -*-
'''
AMAZON DYNAMODB TABLES
Execute when creating the tables
'''
# Import required packages for Amazon DynamoDB
from resource import dynamodb

# Table for data describing a session with location as secondary index
sessions = dynamodb.create_table(
	TableName='ILTaxSessions',
	KeySchema=[
		{
			'AttributeName': 'session_id',
			'KeyType': 'HASH'
		},
		{
			'AttributeName': 'timestamp',
			'KeyType': 'RANGE'
		}		
	],
	GlobalSecondaryIndexes=[
		{
			'IndexName': 'ILTaxSessionsIndex',
			'KeySchema': [
				{
					'AttributeName': 'location',
					'KeyType': 'HASH'
				},
				{
					'AttributeName': 'type',
					'KeyType': 'RANGE'
				},				
			],
			'Projection': {
				'ProjectionType': 'ALL'
			},
			'ProvisionedThroughput': {
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}
		}
	],
	AttributeDefinitions=[
		{
			'AttributeName': 'session_id',
			'AttributeType': 'S'
		},
		{
			'AttributeName': 'timestamp',
			'AttributeType': 'S'
		},
		{
			'AttributeName': 'location',
			'AttributeType': 'S'
		},
		{
			'AttributeName': 'type',
			'AttributeType': 'S'
		}		
	],
	ProvisionedThroughput={
		'ReadCapacityUnits': 5,
		'WriteCapacityUnits': 5
	}
)