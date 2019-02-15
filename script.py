# Imports
import requests
from datetime import datetime
from _variables import amc_data
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient, ASCENDING, DESCENDING

# Scheme Code;Scheme Name;ISIN Div Payout/ISIN Growth;ISIN Div Reinvestment;Net Asset Value;Repurchase Price;Sale Price;Date
# 101711;Aditya Birla Sun Life MIP II - Savings 5 Plan - Monthly Dividend - Regular Plan;INF209K01736;INF209K01DE3;11.2839;11.1711;11.2839;04-Jan-2010

# Constants
url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx'
start_date_str = '01-Jan-2006'
mongodb_host = 'localhost'
mongodb_port = 27017

# Exceptions
class DuplicateNAVEntry(Exception):
  pass
duplicate_nav_entry = DuplicateNAVEntry()

# To generate dates
start_date = datetime.strptime(start_date_str, '%d-%b-%Y')
today = datetime.today()

dates = []

x = start_date
while x < today:
  x = x + relativedelta(months=6)
  dates.append(x.strftime('%d-%b-%Y'))

# Connect to MongoDB
client = MongoClient(mongodb_host, mongodb_port)
db = client['amfi']
collection = db['nav_history']
collection.create_index([('scheme_code', ASCENDING), ('date', DESCENDING)])
cursor = collection.find({})

# Iterate through AMC List
for amc in amc_data:
  print('\n--------------------')
  print('Scraping', amc['name'])

  # Iterate through dates to get previous and current date
  for idx, date in enumerate(dates):
    if idx == 0: continue
    print('From', dates[idx - 1], 'to', dates[idx])

    params = {
      'mf': amc['code'],
      'frmdt': dates[idx - 1],
      'todt': dates[idx]
    }

    res = requests.get(url, params)
    data = res.text

    # If it does not contain 'Scheme Code' as the first entry, then data does not exist
    if not data.startswith('Scheme'):
      print('-- No data found for this time period!')
      continue

    data_lines = data.splitlines()
    data_lines = data_lines[1:]
    for line in data_lines:
      arr_points = []
      x = line.split(';')

      # Process the line only if it has relevant fields
      if len(x) == 8:
        try:
          for doc in cursor:
            if (doc['scheme_code'] == int(x[0]) and doc['timestamp'] == datetime.strptime(x[7], '%d-%b-%Y')):
              raise duplicate_nav_entry

          point = dict()
          point['amc_code'] = amc['code']
          point['amc_name'] = amc['name']
          point['scheme_code'] = int(x[0])
          point['scheme_name'] = x[1]
          point['isin'] = x[2]
          point['nav'] = float(x[4])
          point['timestamp'] = datetime.strptime(x[7], '%d-%b-%Y')

          collection.insert_one(point)
        except DuplicateNAVEntry:
          continue
        except ValueError:
          continue