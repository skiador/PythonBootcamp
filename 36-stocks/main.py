import requests
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
PRICES_API_KEY = "K07BSOYFWEPTJNR0"
PRICES_ENDPOINT = "https://www.alphavantage.co/query?"

NEWS_API_KEY = "9946e64225824487bb08f4a0e9450d74"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"

ACCOUNT_SID = "test"
AUTH_TOKEN = "test"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters_prices = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": PRICES_API_KEY
}
connection_prices = requests.get(PRICES_ENDPOINT, params=parameters_prices)
print(connection_prices.raise_for_status())
prices_data = connection_prices.json()

yesterday_close = float(prices_data["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=1))]["4. close"])
two_days_ago_close = float(prices_data["Time Series (Daily)"][str(datetime.date.today() - datetime.timedelta(days=2))]["4. close"])
price_change = round(((two_days_ago_close - yesterday_close) / yesterday_close) * 100, 2)

if abs(price_change) >= 2:
    get_news = True
    if price_change > 0:
        status = "increased"
    elif price_change < 0:
        status = "decreased"
    message = f"{COMPANY_NAME}, {STOCK} has {status} by {price_change}!"


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

parameters_news = {
    "q": f"{COMPANY_NAME}",
    "apikey": NEWS_API_KEY,
    "sortBy": "popularity",
    "pageSize": 3,
    "page": 1,
    "language": "en"
}
connection_news = requests.get(NEWS_ENDPOINT, parameters_news)
news_data = connection_news.json()
news = {}
for i in range(3):
    news[news_data["articles"][i]["title"]] = news_data["articles"][i]["description"]




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
if get_news:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if status == "decreased":
        message_text = f"{STOCK}: 🔻{price_change}%"
        print(message_text)
    elif status == "increased":
        message_text = f"{STOCK}: 🔺{price_change}%"
        print(message_text)
    # message = client.messages.create(
    #     body=message_text,
    #     from_="phone_number",
    #     to="another_phone_number"
    # )
    for headline, body in news.items():
        message_text = f"Headline: {headline}\n Brief: {body}"
        # message = client.messages.create(
        #     body=message_text,
        #     from_="phone_number",
        #     to="another_phone_number"
        # )
        print(message_text)
        print("\n\n")









#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

