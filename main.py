import requests
import datetime as dt
from twilio.rest import Client

# Alpha Vantage
STOCK = "AAPL"  # Stock Symbol
COMPANY_NAME = "Apple"  # Name of company
ALPHA_API = "_YOUR_ALPHA_VANTAGE_API_"  # your input goes here
ALPHA_END_POINT = "https://www.alphavantage.co/query"

# News API
NEWS_API = "_YOUR_NEWS_API_"  # your input goes here
NEWS_END_POINT = "http://newsapi.org/v2/top-headlines"

# Twilio
TWILIO_AUTH = "_YOUR_TWILIO_AUTH_KEY_"  # your input goes here
TWILIO_SID = "_YOUR_TWILIO_SID_"  # your input goes here
PHONE = "_YOUR_TWILIO_PHONE_NUMBER_"  # your input goes here

# Formatting Symbols
UP = "🔺"
DOWN = "🔻"

# Getting the date
date = dt.datetime.now()
year = date.year

# Date formatted for f-string keys to fetch from Alpha Vantage Dictionary
today = '{:02d}'.format(date.day)
month = '{:02d}'.format(date.month)
yesterday = '{:02d}'.format(int(today) - 1)
day_before_yesterday = '{:02d}'.format(int(today) - 2)

# Alpha Vantage API parameters
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": ALPHA_API,
}

news_parameters = {
    "apiKey": NEWS_API,
    "q": COMPANY_NAME,
    "category": "business",
    "pageSize": 3,
}

# Alpha Vantage API Request
alpha_response = requests.get(
    url=f"{ALPHA_END_POINT}", params=stock_parameters)
alpha_response.raise_for_status()
stock_data = alpha_response.json()["Time Series (Daily)"]

# NEWS API Request
news_response = requests.get(
    url=f"{NEWS_END_POINT}", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()["articles"]

# sets the variables to assign the price data to the key's in Alpha Vantage Data
yesterday_close = float(stock_data[f"{year}" + "-" + f"{month}" + "-" + f"{yesterday}"]["4. close"])
day_before_close = float(stock_data[f"{year}" + "-" + f"{month}" + "-" + f"{day_before_yesterday}"]["4. close"])

# formula for getting the percent change, formatted to second decimal place
percent_change = float("{:.2f}".format(((float(yesterday_close) - day_before_close) / day_before_close) * 100))

if percent_change >= 1 or percent_change <= -1:  # trigger conditions for text, alter the amount to personal preference
    if percent_change < 0:
        for item in news_data[0:1]:  # Set for one article
            client = Client(TWILIO_SID, TWILIO_AUTH)
            message = client.messages \
                .create(body=f"APPL: {DOWN}{percent_change}%\nHeadline: {item['title']}\nBrief: {item['description']}",
                        from_=PHONE, to="+15555554567")  # choose a verified number for the "to="
            print(message.status)
    elif percent_change > 0:
        for item in news_data[0:1]:  # Set for one article
            client = Client(TWILIO_SID, TWILIO_AUTH)
            message = client.messages \
                .create(body=f"APPL: {UP}{percent_change}%\nHeadline: {item['title']}\nBrief: {item['description']}",
                        from_=PHONE, to="+15555554567")  # choose a verified number for the "to="
            print(message.status)
