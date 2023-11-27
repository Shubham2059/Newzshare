import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "xxxxxxxxxxxxxxxxxxxx"
NEWS_API_KEY = "xxxxxxxxxxxxxxxxxxxxx"
TWILIO_SID = "xxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxxxxxxxxxx"


parameter = {
    "apikey": STOCK_API_KEY,
    "function" : "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,

}


# Getting yesterday's closing stock price.
response = requests.get(STOCK_ENDPOINT, params = parameter)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)


# Getting the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)


# Finding the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(yesterday_closing_price)-float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"


# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

difference_percentage = round((difference/float(day_before_yesterday_closing_price))*100)
print(difference_percentage)


# Instead of printing ("Get News"), using the News API to get articles related to the COMPANY_NAME.

news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
}

news_response = requests.get(NEWS_ENDPOINT,params=news_params)
articles = news_response.json()["articles"]
print(articles)

# Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = articles[:3]
print(three_articles)


# Creating a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_percentage}%\nHeadline: {article['title']}, \nBrief: {article['description']}" for article in three_articles]



# Send each article as a separate message via Twilio.
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
                         body=article,
                         from_="123456789123",
                         to="+911234567891",
                     )




