# -*- coding: utf-8 -*-
'''
INITIALIZE DASH APP
'''
# Import graphing packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from textwrap import dedent

# Import packages for data retrieval, post, and cleaning
import os
import pandas as pd
import re
import sys

# Import styles that apply to all Dash apps
from styling import (
	external_stylesheets,
	colors, green, red, font,
	credits
)

# Import from app file in parent directory
sys.path.append('..')
from server import (
	app as server,
	get_session_kvs_data,
	get_all_submit_kvs_data
)

# Initialize the dash app with Flask app as server on index
dash_app_results = dash.Dash(
	__name__, 
	external_stylesheets=external_stylesheets, 
	server=server,
	url_base_pathname='/results/'
)


'''
DATA FROM CSV
'''
# Open the data from csv and get the x-axis values
csv_path = os.path.join(server.static_folder, 'data', 'agi_data.csv')
df = pd.read_csv(csv_path, index_col=0)
x = df.index.tolist()  # x-axis on most graphs


'''
TAX RATE BAR CHART
'''
# Function for returning bar graph of rates
def tax_rate_bar(tax_rates, title):
	tax_data = [{
		'x': [re.sub(',00[0|1]', 'k', k) for k in x],
		'y': [round(tax_rates[v] * 100.0, 2) for v in x],
		'type': 'bar',
		'marker': {
			'color': colors
		}
	}]

	# Return the data for the figure
	return go.Figure(
		data=tax_data,
		layout=go.Layout(
			title=title,
			titlefont={'family': font},
			yaxis={
				'title':'Tax Rate for Bracket',
				'titlefont': {'family': font},
				'ticksuffix': '%'
			},
			xaxis={
				'title':'Income Bracket',
				'titlefont': {'family': font}
			},
			showlegend=False
		)
	)

# Standard chart for IL flat tax
def IL_standard():
	tax_rates = {k:0.0495 for k in x}
	title = 'Current Illinois Flat Tax<br>at 4.95% for All Brackets'
	return tax_rate_bar(tax_rates, title)

# Get the average of all submitted values for the graph
def avg_submitted():
	data, count = get_all_submit_kvs_data()

	# Average the keys
	k = data[0]['tax_rates'].keys()
	avgs = {}
	for x in k:
		values = [v['tax_rates'][x] for v in data]
		avgs[x] = float(sum(values)) / count

	# Return the tax rate bar
	title = 'Average IL Tax Rates<br>Selected by {} Other Users'.format(count)
	return tax_rate_bar(avgs, title)

'''
LAYOUT
'''
# Provide the layout of the app in a function with session_id as param
def serve_layout():
	return html.Div(children=[

		# Represents the URL bar, doesn't render anything
		dcc.Location(id='url', refresh=False),

		# Title for introductory section
		html.Div(children=[
			html.Div(children=[
				html.H3('HOW DID USERS CHANGE ILLINOIS\' INCOME TAX?')
			], className='col-md-12 text-center')
		], className='row', style={'padding-top': '2.5%', 'padding-bottom': '2.5%'}),

		# Information for user
		html.Div(children=[
			html.Div(children=[
				html.H5(dcc.Markdown(dedent('*THANK YOU FOR TESTING THIS SITE!*'))),
				html.P(dcc.Markdown(dedent(
					'''
					The site is currently collecting the following information from users:
					* 1. Generalized Location
					* 2. All Slider Movements
					* 3. All Income Entries
					* 4. Any State Dropdown Selections
					* 5. Timestamp for Each Action
					'''
				))),
				html.P(dcc.Markdown(dedent(
					'''
					If you have any ideas for how to interactively display that information,
					let Joe know. He's still working on that part. 
					'''
				)))
			], className='col-md-12 text-justify')
		], className='row'),

		# Show current tax system, user tax system, average tax system
		html.Div(children=[
			dcc.Graph(figure=IL_standard(), id='current-tax-rates', className='col-md-4'),
			dcc.Graph(id='session-tax-rates', className='col-md-4'),
			dcc.Graph(figure=avg_submitted(), id='average-tax-rates', className='col-md-4')
		], className='row', style={'height': '300px'}),

		# In markdown italics, tell the user where this information came from
		html.Div(children=[
			html.Div(children=[
				dcc.Markdown(dedent(credits))
			], className='col-md-12 text-center')
		], className='row', style={'padding-top': '3.75%'})

	# Close out the container with 100% of the frame width
	], style={'width': '100%', 'padding-left': '2.5%', 'padding-right': '2.5%'})

# Serve the layout with different title
dash_app_results.layout = serve_layout
dash_app_results.title = 'IL Income Tax Results'


'''
SERVE LAYOUT WITH DATA
'''
# Get the data for the session from the url
@dash_app_results.callback(
	dash.dependencies.Output('session-tax-rates', 'figure'),
	[dash.dependencies.Input('url', 'pathname')]
)

# Serve the page with the session id
def layout_callback(*values):
	if not values[0]:
		return  # Empty return if there's a problem with url

	# Split the url
	url = values[0].split('/')
	if len(url) == 3:
		session_id = url[-1]
	
	# If there is no session_id, fail the callback
	else:
		return 'An Error Occurred | No session data provided'

	# Get the data from the session for the graph
	tax_rates, location = get_session_kvs_data(session_id)
	title = 'Tax Rates Submitted<br>by User in {}'.format(location)

	# Return the graph of the user's tax rates
	return tax_rate_bar(tax_rates, title)