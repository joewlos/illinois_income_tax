# -*- coding: utf-8 -*-
'''
AMAZON DYNAMODB RESOURCE
'''
# Import required packages for Amazon DynamoDB
from boto3 import resource, session
import decimal
import json
from os import environ

# Check if we are on Heroku, and use config if not
if 'ON_HEROKU' not in environ:
	import sys
	sys.path.append('..')
	from config import Config

	# Set the resource using config
	dynamodb = resource(
		'dynamodb',
		config=session.Config(signature_version='s3v4'),
		region_name=Config.AWS_REGION_NAME,
		aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
		aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
	)

# Otherwise, set using environ
else:
	dynamodb = resource(
		'dynamodb',
		config=boto3.session.Config(signature_version='s3v4'),
		region_name=AWS_REGION_NAME,
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)

# Amazon's helper class for converting DynamoDB items to JSON
class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)