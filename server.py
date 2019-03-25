# -*- coding: utf-8 -*-
'''
INITIALIZE FLASK
'''
# Import required packages for Flask and functions
from decimal import Decimal
from flask import (
	Flask, 
	jsonify,
	request, 
	send_from_directory
)
import geoip2.database
import os

# Import the model functions
from models.inserts import *
from models.queries import *

# Initialize the Flask app with server name
app = Flask(__name__, static_folder='static')


'''
STATIC ROUTES
'''
# Static route for custom stylesheet, used by Dash apps
@app.route('/stylesheet.css', methods=['GET'])
def stylesheet():
	doc_path = os.path.join(app.static_folder, 'css')
	return send_from_directory(doc_path, 'stylesheet.css')

# Serve robots.txt for page scraping
@app.route('/robots.txt', methods=['GET'])
def robots():
	robots_path = os.path.join(app.static_folder, 'robots')
	return send_from_directory(robots_path, 'robots.txt')


'''
AMAZON DYNAMODB KVS
'''
# Triggered by changes to the tax revenue graph or submit button
def send_kvs_data(data):

	# Edit the session for location
	ip = data.pop('request_ip')
	city, state = find_ip_loc(ip)
	data['location'] = '{0}, {1}'.format(city, state)
	
	# Convert the tax and income data to decimal for dynamodb
	data['tax_rates'] = {k:Decimal(str(v)) for k,v in data['tax_rates'].items()}
	data['income'] = Decimal(str(data['income']))

	# Put the data to kvs
	put_session(data)

	# Return nothing to Dash
	return

# Get kvs data from a user's submit for the results page
def get_session_kvs_data(session_id):
	data = get_specific_submit_item(session_id)[0]
	tax_rates = {k:float(v) for k,v in data['tax_rates'].items()}
	return tax_rates, data['location']

# Get all submitted values and average the tax rates
def get_all_submit_kvs_data(location=None):
	data, count = get_all_submit_items()
	return data, count


'''
GEOLOCATION FROM IP
'''
# Use GeoIP2 to find the location for the IP
def find_ip_loc(ip):
	db_name = 'GeoLite2-City.mmdb'
	path = os.path.join(app.static_folder, 'data', db_name)
	reader = geoip2.database.Reader(path)

	# Return early if we are on local for testing
	if ip == '127.0.0.1':
		return 'Local', 'HOST'

	# Try using the city version
	resp = reader.city(ip)
	city = resp.city.name

	# If not in US, get country, otherwise, use state
	if resp.country.iso_code != 'US':
		country = resp.country.iso_code
		return city, country
	else:
		state = resp.subdivisions.most_specific.iso_code
		return city, state