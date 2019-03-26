# -*- coding: utf-8 -*-
'''
STYLES IMPORTED IN DASH APPS
'''
# Use Bootstrap, Google Fonts, and custom stylesheet for layout
external_stylesheets = [
	'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
	'https://fonts.googleapis.com/css?family=Rubik',
	'/stylesheet.css'
]

# These values are also in CSS
colors = [
	'#5B8E7D',
	'#8CB369',
	'#F4E285',
	'#F4A259',
	'#BC4B51'
]
green = '#5B8E7D'
red = '#BC4B51'
font = '"Rubik", Helvetica, sans-serif;'  # Imported in external_stylesheets

# Credits for creators and vendors
credits = '''
	*The data above are estimates, using individual income tax stratifications
	from the [Illinois Department of Revenue](https://www2.illinois.gov/rev/research/taxstats/IndIncomeStratifications/Pages/default.aspx)
	for 2016.
	[Eric Green](http://www.github.com/adriangreen) and [Joe Wlos](http://www.joewlos.com)
	produced the visualizations using the Python framework [Dash](https://plot.ly/products/dash/) by Plotly.
	[Amazon DynamoDB](https://aws.amazon.com/dynamodb/) is the NoSQL database service.
	[MaxMind](https://www.maxmind.com) provides GeoLite2 data for generalizing IP locations.
	No personally identifiable information is stored by this application.*
'''