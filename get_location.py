### Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time

### mysql_functions has df_to_table to save to my local MySQL db
# from mysql_functions import df_to_table

### Ships to track
base_url = 'https://www.cruisemapper.com/'

ships = ['National-Geographic-Explorer-873',
         'National-Geographic-Orion-875',
         'National-Geographic-Sea-Bird-876',
         'ms-Koningsdam-1036',
         'Ruby-Princess-593',
         'Norwegian-Joy-1166',
         'ms-The-World-1119']

### Website rejects requests without user agents so header is used to act like browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

def read_page(ship):

    ### Get webpage and get relevant paragraph ###
  
    url = base_url + ship
  
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        html = BeautifulSoup(response.text, 'html.parser')

        return html.find('div', {'class': 'currentItineraryInfo'}).text.split('\n')[1].strip()

    else:

        print(f'Request failed with status code: {response.status_code}')
        return None

def parse_html(data):

    ### Parse specifics from paragraph ###
  
    vessel, location, latitude, longitude, destination, reported = re.findall(r'^(.*) current location is\s*at (.*) \(coordinates (.*) \/ (.*)\) cruising .*\s?en route to (.*)\. The AIS position was reported (.*) ago\.$', data)[0]
    
    ## Strip off trailing space and E or W since info is encoded in negative number and then variable can be float rather than string
    latitude = latitude[:-2]
    longitude = longitude[:-2]

    return vessel, location, latitude, longitude, destination, reported, datetime.now()

def parse_timestamp(reported, now):

    ### Calculate actual reporting time given info such as '... reported 11 minutes ago' ###
  
    num, min_or_hours = reported.split(' ')

    if min_or_hours.startswith('minute'):
        return now - timedelta(minutes=int(num))
    else:
        return now - timedelta(hours=int(num))

### Output time of query for logging
print (datetime.now())

for url in urls:

    data = read_page(url)

    try:

        vessel, location, latitude, longitude, destination, reported, now = parse_html(data)

        modified = parse_timestamp(reported, now)

        print (f"{vessel} reported {reported} ago en route to {destination}")

        data = {
            'vessel': vessel, 'location': location, 'latitude': latitude, 'longitude': longitude,
            'destination': destination, 'modified_gmt': modified
        }

        df = pd.DataFrame().from_records([data])

#        df_to_table(df, 'geography', 'cruiseship_locations', 'append')

    except Exception as e:

        print (f'ERROR: {e}')

        continue
