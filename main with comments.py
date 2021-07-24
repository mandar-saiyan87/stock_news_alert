'''
Script sends SMS alert if your favorite stock went above or below 5%
and sends 3 latest news about stock
'''

import requests
import datetime as dt
from twilio.rest import Client

today_date = dt.datetime.today().date()
yesterday_date = today_date - dt.timedelta(days=1)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_KEY = 'YOUR_KEY'
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = 'YOUR_KEY'

parameters = {'function': 'TIME_SERIES_DAILY',
              'symbol': STOCK_NAME,
              'apikey': ALPHAVANTAGE_KEY,
              }

news_parameters = {'q': COMPANY_NAME,
                   'apikey': NEWSAPI_KEY
                   }

tesla_data = requests.get(STOCK_ENDPOINT, params=parameters)
tesla_daily_data = tesla_data.json()['Time Series (Daily)']
tesla_daily = [values for daily, values in tesla_daily_data.items()]
# print(tesla_daily)

# stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price
yesterday = float(tesla_daily[0]['4. close'])


# Get the day before yesterday's closing stock price
before_yesterday = float(tesla_daily[1]['4. close'])


# Find the positive difference between 1 and 2
difference = yesterday - before_yesterday
pos_diff = abs(difference)


# percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent = round((pos_diff / yesterday) * 100, 2)

# get the first 3 news pieces for the COMPANY_NAME.

if percent < 5 or percent > 5:
    new_get = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_articles = new_get.json()['articles'][0:3]


top3_news = [f"Headline: {article['title']}.\nDescription: {article['description']}.\nURL: {article['url']}"for article in news_articles]

#send a separate message with each article's title and description through SMS.
# list of the first 3 article's headline and description using list comprehension.
# Send article as a separate message via Twilio.

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


def send_ref(news):
    msgs = len(news)
    idx = 0
    while 0 < msgs:
        message = client.messages \
            .create(
            body=top3_news[idx],
            from_='+14804392476',
            to='+919167949688'
        )
        idx += 1
        msgs -= 1


account_sid = 'AC4c1bf70ae38877e3ba2f78806238ba8f'
auth_token = 'c7a8b6ff2e36affe073636d932c5e4c7'
client = Client(account_sid, auth_token)
if difference > 0:
    message = client.messages \
        .create(
        body=f"TSLA: 🔺{percent}%",
        from_='+14804392476',
        to='+919167949688'
    )
    send_ref(top3_news)
else:
    message = client.messages \
        .create(
        body=f"TSLA: 🔻{percent}%",
        from_='+14804392476',
        to='+919167949688'
    )
    send_ref(top3_news)
