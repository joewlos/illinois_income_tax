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
Dash apps dynamically generate HTML for each page, importing the primary Flask app as the server. Executing `app.py` initializes the Dash and Flask apps. Flask settings and routes are on `server.py`, and Dash routes are declared in `url_base_pathname`.

#### AMAZON DYNAMODB
The `models` folder includes functions for querying, inserting, and creating tables in Amazon DynamoDB. When locally hosted, the app relies on a config file that is not included in this GitHub repo. When deployed to Heroku, the settings are stored as environ variables.  

#### GEOLOCATION
Visitor IP addresses are examined but not stored. City and state data is retrieved from MaxMind's free GeoIP2 database, contained in `GeoLite2-City.mmdb`.