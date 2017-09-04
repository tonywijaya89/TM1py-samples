"""
Read FX data from FRED (Federal Reserve of St. Louis data) through pandas and push it to the fx cube

Run sample setup.py before running this script, to create the required cubes and dimensions!

Assumption: 
- pandas and pandas_datareader is installed

"""
import collections
from datetime import datetime
# type 'pip install pandas_datareader' into cmd if you don't have pandas_datareader installed
import pandas_datareader.data as web

from TM1py.Services import TM1Service

# load FX Rates for USD to JPY from FRED through pandas datareader
start = datetime(year=2017, month=1, day=1)
raw_data = web.get_data_fred("DEXJPUS", start)

# remove NaN
data = raw_data.dropna()

# create cellset and push it to FX Cube
cube = 'FX Rates'
cellset = collections.OrderedDict()
for tmstp, data in data.iterrows():
    date = tmstp.date()
    value = data.values[0]
    coordinates = ('USD', 'JPY', str(date), 'Spot')
    cellset[coordinates] = value

with TM1Service(address="", port=12354, user="admin", password="apple", ssl=True) as tm1:
    tm1.cubes.cells.write_values('TM1py FX Rates', cellset)

