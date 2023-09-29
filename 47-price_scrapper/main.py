import matplotlib.pyplot
import pandas as pd
import requests
import json
import datetime
import os
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

URL = "https://amzn.eu/d/iUwv4jV"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
}
MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SMTP = "smtp.gmail.com"
PRICE_THRESHOLD = 299


def send_email(price, product):
    email_connection = smtplib.SMTP(SMTP)
    email_connection.starttls()
    email_connection.login(user=MY_EMAIL, password=PASSWORD)
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL
    msg["Subject"] = f"Price alert for {product}"
    body = f"Item: {product}\nPrice: {price}e\nLink: {URL}"
    msg.attach(MIMEText(body, "plain"))

    with open("price_plot.png", "rb") as image_file:
        image = MIMEImage(image_file.read(), name="price_evolution")

    # Attach the image to the email
    msg.attach(image)
    email_connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=msg.as_string())

    email_connection.quit()


# Retrieve html
connection = requests.get(URL, headers=HEADERS)
connection.raise_for_status()
text = connection.text

if os.path.exists("prices.json") and os.path.getsize("prices.json") > 0:
    with open("prices.json", "r") as data:
        prices = json.load(data)
else:
    prices = {"date": [], "price": []}

# Search price info
soup = BeautifulSoup(text, "html.parser")
item_name = soup.find("span", id="productTitle").text.strip()
price_units = soup.find("span", class_="a-price-whole").text.strip(",")
price_cents = soup.find("span", class_="a-price-fraction").text
item_price = float(f"{price_units}.{price_cents}")
datetime_now = datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S")
prices["date"].append(datetime_now)
prices["price"].append(item_price)

# Update price database
with open("prices.json", "w") as file:
    json.dump(prices, file, indent=4)

with open("prices.json", "r") as data:
    prices = json.load(data)

dataframe = pd.DataFrame(prices)
dataframe["date"] = pd.to_datetime(dataframe["date"], dayfirst=True)
plot = dataframe.plot(x="date", y="price")
matplotlib.pyplot.savefig("price_plot.png")


# Check if price lower than preset value
if item_price <= PRICE_THRESHOLD:
    send_email(item_price, item_name)
