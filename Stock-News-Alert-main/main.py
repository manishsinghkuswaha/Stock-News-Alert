import requests
from twilio.rest import Client

STOCK = "TSLA"                                 # INSERT STOCK INTERESTED IN (TSLA for TESLA)
COMPANY_NAME = "TESLA"                         # INSERT THE COMPANY NAME

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = ""                            # INSERT STOCK API KEY
NEWS_API_KEY = ""                             # INSERT NEWS API KEY

account_sid = ""                              # INSERT TWILIO ACCOUNT SID
auth_token = ""                               # INSERT TWILIO AUTH TOKEN

TWILIO_NUMBER = ""                            # INSERT TWILIO GENERATED NUMBER
MOBILE_NUMBER = ""                            # INSERT PERSONAL MOBILE NUMBER

stock_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : STOCK_API_KEY,
}
news_parameters = {
    "q" : COMPANY_NAME,
    "apiKey" : NEWS_API_KEY
}
closing_values = []
stock_update = ""

response_stock = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response_stock.raise_for_status()
data_stock = response_stock.json()["Time Series (Daily)"]


for info in data_stock:
    closing_values.append(float(data_stock[info]["4. close"]))

difference = closing_values[0] - closing_values[1]
percent_diff = ((abs(difference)) / closing_values[0]) * 100


if percent_diff > 5:
    response_news = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    response_news.raise_for_status()
    news_articles = response_news.json()["articles"][:3]

    if difference > 0:
        stock_update = f"{STOCK}: 🔺{round(percent_diff, 2)}%"
    elif difference < 0:
        stock_update = f"{STOCK}: 🔻{round(percent_diff, 2)}%"

    client = Client(account_sid, auth_token)

    for news in news_articles:
        message = client.messages \
            .create(
            body=f'{stock_update} \nHeadline: {news["title"]} \nDescription: {news["description"]}',
            from_=TWILIO_NUMBER,
            to=MOBILE_NUMBER
        )

        print(message.status)

