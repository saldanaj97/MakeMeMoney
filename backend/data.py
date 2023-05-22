import requests
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Global vars
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY") 
URL_PREFIX = "https://www.alphavantage.co/query" 

# Function that will build the url for API use
def buildUrl(function, symbol):
    return URL_PREFIX + "?function=" +function + '&symbol=' + symbol + "&apikey=" + ALPHA_VANTAGE_API_KEY

# Function that will act as a switch statement to determine which URL to build
def adjustedValueURLBuilder(timePeriod, symbol):
    url = "" 
    if timePeriod == 'daily':
        url = buildUrl(function='TIME_SERIES_DAILY_ADJUSTED', symbol=symbol)
    elif timePeriod == 'weekly':
        url = buildUrl(function='TIME_SERIES_WEEKLY_ADJUSTED', symbol=symbol)
    elif timePeriod == 'monthly':
        url = buildUrl(function='TIME_SERIES_MONTHLY_ADJUSTED', symbol=symbol)
    else: 
        url = buildUrl(function='TIME_SERIES_DAILY_ADJUSTED', symbol=symbol)
    return url    

# Function to return the raw (as-traded) daily open/high/low/close/volume values
def getAdjusted(timePeriod='daily', symbol='IBM'):
    url = adjustedValueURLBuilder(timePeriod, symbol)
    r = requests.get(url)
    data = r.json()
    print(data)

getAdjusted()
