# Illinois Income Tax Dash App
#### APP STRUCTURE
```
- app.py
- server.py
- dash_templates
    - tax_input.py
    - tax_results.py
- models
    - resource.py
    - create_tables.py
    - queries.py
    - inserts.py
- static
    - css
        - stylesheet.css
    - data
        - agi_data.csv
        - GeoLite2-City.mmdb
```
#### FLASK AND DASH

A Flask app functions as the server, while individual Dash apps provide the HTML for each page. Executing `app.py` initializes the Flask app, which each Dash app imports. Flask settings and routes are on `server.py`, and Dash routes are in their app files, declared in `url_base_pathname`.

#### AMAZON DYNAMODB
The `models` folder includes a script for querying, inserting, and creating tables in Amazon DynamoDB. When locally hosted, the app relies on a config file that is not included in this GitHub repo. When deployed to Heroku, the settings are stored as environ variables.  

#### GEOLOCATION
Visitor IP addresses are examined but not stored. City and state data is retrieved with MaxMind's free GeoIP2 database, contained in `GeoLite2-City.mmdb`.