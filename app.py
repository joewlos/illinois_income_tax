# -*- coding: utf-8 -*-
'''
IMPORT FLASK AND DASH APPS
'''
# Each dash file needs to imported
from server import app
from dash_templates.tax_input import dash_app_input
from dash_templates.tax_results import dash_app_results

'''
RUN APP
'''
# Run app in debug
if __name__ == '__main__':
    app.run(debug=True)
