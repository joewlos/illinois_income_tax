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
from datetime import datetime
from flask import request
import os
import pandas as pd
import re
import sys
import uuid

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
	send_kvs_data
)

# Initialize the dash app with Flask app as server on index
dash_app_input = dash.Dash(
	__name__, 
	external_stylesheets=external_stylesheets, 
	server=server,
	url_base_pathname='/'
)


'''
DATA FROM CSV
'''
# Open the data from csv and get the x-axis values
csv_path = os.path.join(server.static_folder, 'data', 'agi_data.csv')
df = pd.read_csv(csv_path, index_col=0)
x = df.index.tolist()  # x-axis on most graphs


'''
SLIDERS
'''
# Dictionary for dropdown menu in sliders
tax_dict = [
	{	'label': 'Illinois Flat Tax',
		'value': 'IL_2017',
		'rates': [0.0495] * 5
	},
	{	'label': 'Indiana Flat Tax', 
		'value': 'IN_2018',
		'rates': [0.0323] * 5
	},
	{	'label': 'Louisiana Progressive Tax',
		'value': 'LA_2018',
		'rates': [0.02, 0.04, 0.06, 0.06, 0.06]
	},
	{	'label': 'Maine Progressive Tax',
		'value': 'ME_2018',
		'rates': [0.058, 0.0675, 0.0715, 0.0715, 0.0715]
	},
	{	'label': 'Massachusetts Flat Tax', 
		'value': 'MA_2018',
		'rates': [0.051] * 5
	},
	{	'label': 'Michigan Flat Tax', 
		'value': 'MI_2018',
		'rates': [0.0425] * 5
	},
	{	'label': 'New Jersey Progressive Tax',
		'value': 'NJ_2018',
		'rates': [0.014, 0.0175, 0.0553, 0.0637, 0.0897]
	},
	{	'label': 'Utah Flat Tax', 
		'value': 'UT_2018',
		'rates': [0.05] * 5
	},
	{	'label': 'Vermont Progressive Tax',
		'value': 'VT_2018',
		'rates': [0.035, 0.066, 0.066, 0.076, 0.0875]
	},
	{	'label': 'Wisconsin Progressive Tax',
		'value': 'WI_2018',
		'rates': [0.04, 0.0627, 0.0627, 0.0627, 0.0765]
	}
]

# Dropdown edits the values of the sliders
def create_dropdown(default='IL_2017'):

	# Dropdown default value is IL 2017
	drop = dcc.Dropdown(
		id='slider-dropdown',
		options=[{k:v for k,v in d.items() if k != 'rates'} for d in tax_dict],
		value=default
	)

	# Return the dropdown
	return drop

# Iterate across all income bands to create the sliders
def create_sliders(values=[0.0495] * 5, default='IL_2017'):
	
	# First slider is a dropdown for viewing different tax rates
	sliders = [
		html.H5("Customize Illinois' Rates"),
		html.H6("Apply Another State's Tax System to Illinois",
			style={'margin-top': '30px'}),
		create_dropdown(default=default)
	]
	
	# Iterate across each band
	for i, band in enumerate(x):
		size = '30px'
		sliders += [
			html.Div(children=[

				# Label and text input
				html.Div(children=[
					html.Div(
						children=[html.Label('{} Tax Rate'.format(band))], 
						className='col-md-8'
					),
					html.Div(
						children=[
							dcc.Input(
								id='input-text-{}'.format(i), 
								min=0,
								max=100,
								value=round(values[i] * 100.0, 2),  # 2 decimal places
								type='number'
							)
						],
						id='input-section-{}'.format(i),
						className='col-md-2'
					),
					html.Div(
						children=['%'],
						className='col-md-1'
					)
				], className='row'),

				# The slider bar
				html.Div(children=[
					dcc.Slider(
						id='slider-{}'.format(i),
						min=0,
						max=1,
						marks={m / 100.0: '{}%'.format(m) for m in range(0, 101, 10)},
						value=round(values[i], 4),  # Percentage, so 4 decimal places
						step=0.0005
					)
				], id='slider-section-{}'.format(i))

			# Apply margin to slider
			], style={'margin-top': size})
		]
	return sliders


'''
FLAT AND PROGRESSIVE EXAMPLE BARS
'''
# IL Brackets used for tax calc and graph calc
brackets = [
	[0, 25000],
	[25000, 50000],
	[50000, 100000],
	[100000, 500000],
	[500000, 1000000000000]  # Trillion is the max input
]

# Fed brackets and rates used in the progressive example graph
fed_brackets = [
	[0, 9525],
	[9526, 38700],
	[38700, 82500],
	[82500, 157500]
]
fed_rates = [0.1, 0.12, 0.22, 0.24]

# Show a single bar demonstrating how a tax is applied to an income
def example_bar_graphs(
		values,
		brackets=brackets,
		x=x,
		title='Income Tax Rates<br>for ${:,.0f}',
		colors=colors
	):
	agi = values[0]
	taxes = values[1:]

	# Put the income into its brackets
	income_brackets = []
	for i, b in enumerate(brackets):
		if b[0] < agi:

			# Calculate how much tax will be paid
			amt = min(b[1], agi) - b[0]
			tax = amt * taxes[i]

			# Hoverinfo depends on whether x is supplied
			if x:
				name = re.sub(',00[0|1]', 'k', x[i])
				hoverinfo = 'name'
			else:
				name = None
				hoverinfo = 'none'

			# Add the trace for the bar chart
			trace = go.Bar(
				x=[amt],
				y=[agi],
				name=name,
				text='{:,.2f}%'.format(taxes[i] * 100.0),
				textposition='auto',
				hoverinfo=hoverinfo,
				orientation='h',
				hoverlabel={
					'bgcolor': colors[i],
					'font': {'family': font}
				},
				marker={'color': colors[i]}
			)
			income_brackets.append(trace)

	# Return the figure to the graph
	return go.Figure(
		data=income_brackets,
		layout=go.Layout(
			barmode='stack',
			title={
				'text': title.format(agi),
				'yanchor': 'top',
				'xanchor': 'center',
				'y': 0.7,
				'x': 0.5
			},
			titlefont={'family': font},
			showlegend=False,
			height=220,
			margin={
				'l': 50,
				'r': 50,
				'pad': 0
			},
			yaxis={
				'showgrid': False,
				'zeroline': False,
				'showline': False,
				'ticks': '',
				'showticklabels': False
			},
			xaxis={
				'showgrid': False,
				'zeroline': False,
				'showline': False,
				'ticks': '',
				'showticklabels': True,
				'tickprefix': '$',
				'range': [0, agi]
			}
		)
	)


'''
INFORMATION SECTION
'''
# Information about using the app with example graphs
def create_info():

	# Remove indents when using markdown
	header1 = dcc.Markdown(dedent('*FLAT VS. PROGRESSIVE INCOME TAX*'))
	text1 = dcc.Markdown(dedent('''
	Illinois is one of only eight states using a **flat** income tax system.
	In other words, Illinois taxes every individual's income at the same rate,
	regardless of how high or low the individual's income is.
	Most other states and the federal government use a **progressive** income tax system.
	In progressive systems, the government divides an individual's income into brackets,
	and tax rates rise in higher brackets.
	'''))
	text2 = dcc.Markdown(dedent('''
	For example, the lowest federal income bracket ends at $9,525.
	The federal government taxes every dollar earned up to $9,525 at 10%,
	while every dollar earned above $9,525 is taxed at 12%.
	In Illinois' flat system, there are no brackets.
	The tax rate never changes, across every level of income.
	Whether you're a billionaire or living below the poverty line,
	your effective tax rate in Illinois–before exemptions and credits–is
	always **4.95%** for every dollar you earn. 
	'''))
	text3 = dcc.Markdown(dedent('''
	The bars above show how progressive federal income tax brackets
	and Illinois' flat tax are applied to an annual income of $100,000.
	The progressive tax rates rise in each income bracket, 
	with the individual owing more taxes on the portions of income
	in higher brackets. The Illinois tax rate remains flat.
	'''))
	text4 = dcc.Markdown(dedent('''
	Illinois' governor and legislature are considering
	a [constitutional amendment](https://chicago.suntimes.com/opinion/j-b-pritzker-progressive-income-tax-fair-illinois-budget/)
	to change the state's flat income tax to a progressive system.
	If the amendment is passed, Illinois' citizens would vote to
	approve or disapprove the change to the state constitution in a referendum in 2020.
	'''))
	header2 = dcc.Markdown(dedent('*SEE THE EFFECTS OF DIFFERENT RATES*'))
	text5 = dcc.Markdown(dedent('''
	Use the sliders on the right to **customize Illinois' tax rates** for different income brackets,
	or use the dropdown menu to apply rates used in other states to Illinois.
	Enter your income below to view how different rates would change your own tax bill. 
	When you are happy with your customizations,
	click "View Results" to see how your tax rates line up with those of other users.
	'''))

	# Use greyscale for the example colors
	greys = [
		'#222222',
		'#444444',
		'#666666',
		'#777777'
	]

	# Arrange the instructions with the examples
	p = [
		html.H5(header1),
		html.P(text1),
		html.P(text2),
		html.Div(children=[
			html.Div(children=[
				dcc.Graph(id='graph-progressive-example', 
					config={
						'displayModeBar': False
					},
					figure=example_bar_graphs(
						[100000] + fed_rates,
						brackets=fed_brackets,
						title='Federal Progressive Tax Rates<br>for an ${:,.0f} Income',
						x=None,
						colors=greys
				))
			], className='col-md-6'),
			html.Div(children=[
				dcc.Graph(id='graph-flat-example', 
					config={
						'displayModeBar': False
					},
					figure=example_bar_graphs(
						[100000] + [0.0495],
						brackets=[[0, 100000]],  # Single bracket
						title='IL Flat Tax Rate<br>for an ${:,.0f} Income',
						x=None,
						colors=greys
				))
			], className='col-md-6')
		], className='row', style={'margin-top': '-.5%'}),  # Adjust for large graph size
		html.P(text3),
		html.P(text4),
		html.H5(header2, style={'padding-top': '2.5%'}),
		html.P(text5, style={'padding-bottom': '-.5%'})
	]

	# Return the text
	return p


'''
LAYOUT
'''
# Provide the layout of the app in a function with session_id
def serve_layout():
	session_id = str(uuid.uuid4())
	return html.Div(children=[

		# Title for introductory section
		html.Div(children=[
			html.Div(children=[
				html.H3('HOW WOULD YOU CHANGE ILLINOIS\' INCOME TAX?')
			], className='col-md-12 text-center')
		], className='row', style={'padding-top': '2.5%', 'padding-bottom': '2.5%'}),

		# Explanatory text
		html.Div(children=[
			html.Div(children=create_info(), 
				className='col-md-12 text-justify')
		], className='row'),
		
		# New row for seeing seeing tax on AGI
		html.Div(children=[

			# User input for the AGI using median wage as starting point
			html.Div(children=[
				html.H5('Income ($)'),
				dcc.Input(
					id='input-agi-calc', 
					min=0,
					max=1000000000000,  # Trillion limit seems reasonable
					value=60000,  # Approximate IL median wage
					type='number',
					className='personal-bar'
				)
			], className='col-md-2 text-center'),

			# New rows to keep spacing between titles and data
			html.Div(children=[
			
				# Title row
				html.Div(children=[
					html.Div(children=[
						html.H5('Est 2019 Tax Bill')
					], className='col-md-4 text-center'),
					html.Div(children=[
						html.H5('Customized Bill')
					], className='col-md-4 text-center'),
					html.Div(children=[
						html.H5('Difference')
					], className='col-md-4 text-center')
				], className='row align-items-center'),

				# Data row
				html.Div(children=[
					html.Div(children=[
						html.Div(id='output-old-calc', className='personal-bar')
					], className='col-md-4 text-center'),
					html.Div(children=[
						html.Div(id='output-agi-calc', className='personal-bar')
					], className='col-md-4 text-center'),
					html.Div(children=[
						html.Div(id='difference-agi-calc', className='personal-bar')
					], className='col-md-4 text-center')
				], className='row')

			# Close out the section of two new rows
			], className='col-md-6'),

			# Show a horizontal stacked bar illustrating how the tax is calculated
			html.Div(children=[
				dcc.Graph(id='graph-agi-calc')
			], className='col-md-4')

		# Close out the AGI example row
		], className='row align-items-center'),

		# Graph section is 2/3 of container
		html.Div(children=[
			html.Div(children=[

				# Revenue pie chart and total collected
				html.Div(children=[
					html.Div(children=[
						dcc.Graph(id='tax-revenue-bar')
					], className="col-md-6"),

					# Tax revenue graph is updated by the sliders
					html.Div(children=[
						dcc.Graph(id='tax-revenue-pie')
					], className='col-md-6')

				# Close out the AGI graph row
				], className='row')

			# Close out the column
			], className='col-md-8'),

			# Sliders in div
			html.Div(children=[
				html.Div(
					children=create_sliders(),
					id='all-sliders'
				)
			], className='col-md-4')
		], className='row', style={'padding-top': '1.25%'}),

		# Show the user how much total revenue is collected
		html.Div(children=[
			html.Div(children=[
				html.H5("Total Revenue with Customized Rates"),
				html.Div(id='total-collected')
			], className='col-md-4 text-center'),

			# Show the difference between the new amount and the old
			html.Div(children=[
				html.H5("Difference from 2019 Flat Tax Revenue"),
				html.Div(id='collected-difference')
			], className='col-md-4 text-center'),

			# Button for viewing results
			html.Div(children=[
				html.A(
					html.Button('View Results', id='results-btn', 
						className='btn btn-outline-dark'),
				href='/results/{}'.format(session_id))  # Redirect to route showing results
			], className='col-md-4 text-center')
		], className='row align-items-center',
			style={'padding-top': '7.5%', 'padding-bottom': '5%'}),

		# In markdown italics, tell the user where this information came from
		html.Div(children=[
			html.Div(children=[
				dcc.Markdown(dedent(credits))
			], className='col-md-12 text-center')
		], className='row'),

		# Hidden div for session id
		html.Div(session_id, id='session-id', style={'display': 'none'}),

	# Close out the container with 100% of the frame width
	], style={'width': '100%', 'padding-left': '2.5%', 'padding-right': '2.5%'})

# Serve the layout with different title
dash_app_input.layout = serve_layout
dash_app_input.title = 'IL Income Tax Customization'


'''
SUBMIT BUTTON CALLBACK
'''
# State includes slider values and session_id for kvs
@dash_app_input.callback(
	dash.dependencies.Output('session-id', 'children'),
	[dash.dependencies.Input('results-btn', 'n_clicks')],
	[dash.dependencies.State('slider-{}'.format(j), 'value') for j, b in enumerate(x)] +
	[dash.dependencies.State('session-id', 'children')] + 
	[dash.dependencies.State('input-agi-calc', 'value')]
)

# Send the data a final time and update the uuid for the session
def results_callback(*values):
	n = values[0]
	income = values[-1]
	session_id = values[-2]
	values = values[1:-2]  # Middle of values returned

	# Send data about graph change to kvs, only if button actually clicked
	if n:
		slider_pos = {k:v for k,v in zip(x, values)}
		kvs_data = {
			'session_id': session_id,
			'timestamp': datetime.now().isoformat(),
			'type': 'submit',
			'request_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
			'tax_rates': slider_pos,
			'income': income
		}
		send_kvs_data(kvs_data)

		# Return the new uuid
		return str(uuid.uuid4())

	# Otherwise, return the current uuid
	return session_id


'''
CALLBACK FOR SLIDER AND INPUT
'''
# Callback for changing value of specific slider
for i, band in enumerate(x):
	@dash_app_input.callback(
		dash.dependencies.Output('slider-section-{}'.format(i), 'children'),
		[dash.dependencies.Input('input-text-{}'.format(i), 'value')],
		[dash.dependencies.State('input-text-{}'.format(i), 'id'),
		dash.dependencies.State('slider-{}'.format(i), 'value')]
	)
	def slider_callback(input_value, state_id, slider_value):
		if round(input_value / 100.0, 4) != round(slider_value, 4):
			return dcc.Slider(
				id='slider-{}'.format(state_id.split('-')[-1]),
				min=0,
				max=1,
				marks={m / 100.0: '{}%'.format(m) for m in range(0, 101, 10)},
				value=round(input_value / 100.0, 4), # Percentage, so 4 decimal places
				step=0.0005
			)

		# If the values are the same, prevent a callback infinite loop
		else:
			raise dash.exceptions.PreventUpdate()

# Callback for changing text of specific input
for i, band in enumerate(x):
	@dash_app_input.callback(
		dash.dependencies.Output('input-section-{}'.format(i), 'children'),
		[dash.dependencies.Input('slider-{}'.format(i), 'value')],
		[dash.dependencies.State('slider-{}'.format(i), 'id'),
		dash.dependencies.State('input-text-{}'.format(i), 'value')]
	)
	def input_callback(slider_value, state_id, input_value):
		if round(input_value / 100.0, 4) != round(slider_value, 4):
			return dcc.Input(
				id='input-text-{}'.format(state_id.split('-')[-1]), 
				min=0,
				max=100,
				value=round(slider_value * 100.0, 2),  # 2 decimal places
				type='number'
			)
		
		# If the values are the same, prevent a callback infinite loop
		else:
			raise dash.exceptions.PreventUpdate()


'''
SLIDER CALLBACK FOR REVENUE BAR CHART
'''
# Callback for tax revenue graph 
values = ['value{}'.format(i) for i in range(len(x))]
@dash_app_input.callback(
	dash.dependencies.Output('tax-revenue-bar', 'figure'),
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)],
	[dash.dependencies.State('session-id', 'children')] +
	[dash.dependencies.State('input-agi-calc', 'value')]
)

# Create the graph and send the data to the kvs store function
def graph_callback(*values):
	income = values[-1]
	session_id = values[-2]
	values = values[:-2]

	# Make a copy of the dataframe and apply each rate
	rev_df = df.copy(deep=True)
	for i, band in enumerate(x):
		rev_df[band] = rev_df[band].apply(lambda x: x * values[i])
	
	# Iterate to get the y for the graph
	rev_data = []
	for c, band in enumerate(x):  
		y = [round(i, -7) for i in rev_df[band].tolist()]
		rev_data.append(
			go.Bar(
				x=[re.sub(',00[0|1]', 'k', j) for i, j in enumerate(x) if y[i]],
				y=[j for j in y if j],
				name=band,
				text=re.sub(',00[0|1]', 'k', band),
				hoverinfo='text',
				hoverlabel={
					'bgcolor': colors[c],
					'font': {'family': font}
				},
				marker={'color': colors[c]}
			)
		)

	# Send data about graph change to kvs
	slider_pos = {k:v for k,v in zip(x, values)}
	kvs_data = {
		'session_id': session_id,
		'timestamp': datetime.now().isoformat(),
		'request_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
		'tax_rates': slider_pos,
		'income': income
	}
	send_kvs_data(kvs_data)

	# Return the new tax revenue
	return go.Figure(
		data=rev_data,
		layout=go.Layout(
			barmode='stack',
			title='IL Tax Revenue<br>by Income Bracket',
			titlefont={'family': font},
			yaxis={
				'title':'Total Income Tax Revenue',
				'titlefont': {'family': font},
				'tickprefix': '$'
			},
			xaxis={
				'title':'Taxpayer Income Bracket',
				'titlefont': {'family': font}
			},
			showlegend=False
		)
	)


'''
CALLBACK FOR TOTAL REVENUE COLLECTED
'''
# Calculate the taxes collected
@dash_app_input.callback(
	dash.dependencies.Output('total-collected', 'children'),
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Apply each rate and sum
def collection_callback(*values):
	rev_df = df.copy(deep=True)
	for i, band in enumerate(x):
		rev_df[band] = rev_df[band].apply(lambda x: x * values[i])

	# Use the row indices for the actual data
	y = []
	for band in x:
		y.append(round(rev_df.loc[band].sum()))

	# Return the data
	return html.H5('${:,.0f}'.format(round(sum(y))))

# Calculate the difference for the taxes collected
@dash_app_input.callback(
	dash.dependencies.Output('collected-difference', 'children'),
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Get the difference between the total revenue collected
def collection_difference_callback(*values):
	rev_df = df.copy(deep=True)
	for i, band in enumerate(x):
		rev_df[band] = rev_df[band].apply(lambda x: x * values[i])

	# Use the row indices for the actual data
	new = 0
	for band in x:
		new += round(rev_df.loc[band].sum())

	# Get the difference by subtracting the old amount
	diff = new - 17158013217

	# Return the data formatted with dollar sign and indicator
	if diff > 0:
		return html.H5('+${:,.0f}'.format(abs(diff)), style={'color': green})
	elif diff == 0:
		return html.H5('${:,.0f}'.format(abs(diff)))
	else:
		return html.H5('-${:,.0f}'.format(abs(diff)), style={'color': red})


'''
SLIDER CALLBACK FOR REVENUE PIE 
'''
# Callback is similar to bar
@dash_app_input.callback(
	dash.dependencies.Output('tax-revenue-pie', 'figure'),
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Apply each rate to the copy of the dataframe 
def pie_callback(*values):
	rev_df = df.copy(deep=True)
	for i, band in enumerate(x):
		rev_df[band] = rev_df[band].apply(lambda x: x * values[i])

	# Use the row indices for the actual data
	y=[]
	for band in x:
		y.append(round(rev_df.loc[band].sum()))

	# Return the data as a dictionary for the figure
	return {
		'data': [go.Pie(
			labels=[re.sub(',00[0|1]', 'k', b) for b in x],
			text=['${:,.0f}'.format(v) for v in y],
			textinfo='label+percent',
			values=y,
			marker={'colors': colors},
			hoverinfo='text',
			hoverlabel={'font': {'family': font}}
		)],
		'layout': {
			'title': 'Percentage of IL Tax Revenue<br>by Income Bracket',
			'titlefont': {
				'family': font
			},
			'showlegend': False
		}
	}


'''
INPUT CALLBACK FOR EXAMPLE TAX
'''
# Calculate the total tax charged, given an AGI
def calculate_tax(agi, taxes):

	# Iterate across the income brackets
	tax = 0
	for i, b in enumerate(brackets):
		if b[0] < agi:

			# Calculate the tax
			amt = min(b[1], agi) - b[0]
			tax += amt * taxes[i]

	# Return the tax
	return tax

# Callback for div showing IL flat tax on this AGI
@dash_app_input.callback(
	dash.dependencies.Output('output-old-calc', 'children'),
	[dash.dependencies.Input('input-agi-calc', 'value')]
)

# Display the total tax for this AGI using IL flat tax
def agi_old_callback(*values):

	# Calculate the tax using the values
	old_tax = calculate_tax(values[0], [0.0495] * 5)

	# Return the data formatted with dollar sign
	return html.H4('${:,.0f}'.format(old_tax))

# Callback for div showing tax on this AGI
@dash_app_input.callback(
	dash.dependencies.Output('output-agi-calc', 'children'),
	[dash.dependencies.Input('input-agi-calc', 'value')] +
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Display the total tax for this AGI
def agi_calc_callback(*values):

	# Calculate the tax using the values
	new_tax = calculate_tax(values[0], values[1:])

	# Return the data formatted with dollar sign
	return html.H4('${:,.0f}'.format(new_tax))

# Callback showing the difference on the tax compared to flat tax
@dash_app_input.callback(
	dash.dependencies.Output('difference-agi-calc', 'children'),
	[dash.dependencies.Input('input-agi-calc', 'value')] +
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Subtract old tax from the new tax
def agi_diff_callback(*values):

	# Calculate the taxes using the values
	new_tax = calculate_tax(values[0], values[1:])
	old_tax = calculate_tax(values[0], [0.0495] * 5)
	diff = new_tax - old_tax

	# Return the data formatted with dollar sign and indicator
	if diff > 0:
		return html.H4('+${:,.0f}'.format(abs(diff)), style={'color': red})
	elif diff == 0:
		return html.H4('${:,.0f}'.format(abs(diff)))
	else:
		return html.H4('-${:,.0f}'.format(abs(diff)), style={'color': green})

# Callback for horizontal stacked bar showing tax illustration
@dash_app_input.callback(
	dash.dependencies.Output('graph-agi-calc', 'figure'),
	[dash.dependencies.Input('input-agi-calc', 'value')] +
	[dash.dependencies.Input('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Graph shows total income, colors for bands, amt of income in bands, and tax
def agi_graph_callback(*values):
	return example_bar_graphs(values)  # Same function for examples at top of page


'''
SLIDER DROPDOWN CALLBACK
'''
# Callback for dropdown menu for changing tax rates based on presets
@dash_app_input.callback(
	dash.dependencies.Output('all-sliders', 'children'),
	[dash.dependencies.Input('slider-dropdown', 'value')],
	[dash.dependencies.State('slider-{}'.format(j), 'value') for j, b in enumerate(x)]
)

# Check if the values are the same and update the sliders
def dropdown_callback(*values):

	# Get the choice and current slider values
	choice = values[0]
	new_values = [d for d in tax_dict if d['value'] == choice][0]['rates']
	current = list(values[1:])  # Must be list for comparison

	# If the values are different from the choice
	if current != new_values:

		# Return the new sliders using the new values
		return create_sliders(values=new_values, default=choice)

	# If the values are the same, prevent a callback infinite loop
	else:
		raise dash.exceptions.PreventUpdate()