import json

import requests
import os
import pandas as pd
import datetime as dt
import notification_manager
import numpy as np

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

IATA_CODES_AND_FLIGHTS_API_KEY = os.environ["KIWI_API_KEY"]
IATA_CODES_URL = "https://api.tequila.kiwi.com/locations/query"
FLIGHTS_URL = "https://api.tequila.kiwi.com/v2/search"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
ORIGIN = "BCN"

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class DataManager:

    def __init__(self):
        self.iata_and_flights_header = {
            "apikey": IATA_CODES_AND_FLIGHTS_API_KEY
        }

        self.creds = None
        self.sheet = None
        self.columns = None

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def get_spreadsheet_data(self):
        self.authenticate()
        # Get spreadsheet data
        original_data = None
        try:
            service = build('sheets', 'v4', credentials=self.creds)

            # Call the Sheets API
            self.sheet = service.spreadsheets()
            result = self.sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range="Data").execute()
            values = result.get('values', [])
            data = []
            self.columns = []
            for index, row in enumerate(values):
                if index == 0:
                    self.columns = row
                else:
                    data.append(row)
            original_data = pd.DataFrame(data, columns=self.columns)
        except HttpError as err:
            print(err)

        return original_data

    def update_iata_codes(self, original_data: pd.DataFrame):

        print("Updating city codes...")
        for index, value in original_data.iterrows():
            if value["IATA Code"] == "":
                query = value["City"]
                params = {
                    "term": query
                }

                # Get Iata code
                iata_codes_response = requests.get(
                    url=IATA_CODES_URL,
                    params=params,
                    headers=self.iata_and_flights_header
                )
                iata_code_data = iata_codes_response.json()
                iata_code = iata_code_data["locations"][0]["code"]

                # Update Iata code on loaded spreadsheet data
                original_data.at[index, "IATA Code"] = iata_code

                # Upload new Iata codes to spreadsheet
                try:
                    self.sheet.values().update(
                        spreadsheetId=SPREADSHEET_ID,
                        range=f"Data!B{int(index) + 2}",
                        valueInputOption="USER_ENTERED",
                        body={
                            "values": [[iata_code]]
                        }
                    ).execute()
                except HttpError as err:
                    print(err)

            else:
                pass

        print("City codes updated successfully!")

    def iata_to_name(self, iata):
        with open("airlines.json", "r") as json_file:
            airline_data = json.load(json_file)
        iata_to_name = {entry["iata_code"]: entry["name"] for entry in airline_data}
        try:
            result = iata_to_name[f"{iata}"]
        except KeyError:
            result = iata
        return result

    def get_new_prices(self, original_data):

        # Initialize new data dataframe
        columns = ["IATA Code", "Outbound", "Inbound", "Price"]
        new_data = pd.DataFrame(columns=columns)
        # Set dates
        date_from = (dt.date.today() + dt.timedelta(days=5)).strftime("%d/%m/%Y")
        date_to = (dt.date.today() + dt.timedelta(days=185)).strftime("%d/%m/%Y")

        # Make request for each flight
        for index, row in original_data.iterrows():
            print(f"Checking lowest price to {row['City']}...")
            params = {
                "fly_from": ORIGIN,
                "fly_to": row["IATA Code"],
                "date_from": date_from,
                "date_to": date_to,
                "ret_from_diff_city": False,
                "ret_to_diff_city": False,
                "nights_in_dst_from": row["Minimum Nights"],
                "nights_in_dst_to": row["Maximum Nights"],
                "one_for_city": 1,
                "selected_cabins": "M",
                "partner_market": "es",
                "curr": "EUR"
            }
            flight_search_request = requests.get(
                url=FLIGHTS_URL,
                params=params,
                headers=self.iata_and_flights_header
            )

            # Save received data
            flight_data = flight_search_request.json()
            try:
                flight_price = flight_data["data"][0]["price"]
            except IndexError:
                print(f"No flights found for {row['City']}.")

                # Append the empty row to the DataFrame using concat
                nan_row = pd.DataFrame([np.nan])

                # Concatenate the NaN row to your existing DataFrame
                new_data = pd.concat([new_data, nan_row], ignore_index=True)
                print(new_data)
                continue

            # Check if there's more than 2 flights (meaning connections)
            # If there are connections, sort flights between outbound and inbound
            columns_connections = ["Origin", "Destination", "Date", "Airline"]
            flights_outbound = []
            flights_inbound = []
            for flight in flight_data["data"][0]["route"]:
                if flight["return"] == 0:
                    flight_outbound = (flight["local_departure"][0:10]
                                       + " "
                                       + flight["local_departure"][11:19])
                    airline = self.iata_to_name(flight["airline"])
                    departure_city = flight["cityFrom"]
                    arrival_city = flight["cityTo"]
                    data = [departure_city, arrival_city, flight_outbound, airline]
                    flights_outbound.append(data)
                else:
                    flight_inbound = (flight["local_departure"][0:10]
                                      + " "
                                      + flight["local_departure"][11:19])

                    airline = self.iata_to_name(flight["airline"])
                    departure_city = flight["cityFrom"]
                    arrival_city = flight["cityTo"]
                    data = [departure_city, arrival_city, flight_inbound, airline]
                    flights_inbound.append(data)

            flights_outbound = pd.DataFrame(flights_outbound, columns=columns_connections)
            flights_inbound = pd.DataFrame(flights_inbound, columns=columns_connections)

            new_data = pd.concat(
                [new_data,
                 pd.DataFrame([[row["IATA Code"], flights_outbound, flights_inbound, flight_price]],
                              columns=columns)],
                ignore_index=True)
        return new_data

    def update_prices(self, original_data, new_data):
        for index, row in original_data.iterrows():
            if new_data.loc[index].isna().all():
                continue
            else:
                try:
                    old_price = int(row["Lowest Price"])
                except ValueError:
                    old_price = 0
                new_price = new_data.at[index, "Price"]

                # Check if new price is lower
                if new_price < old_price or old_price == 0:
                    print(f"New lower price for {row['City']}. Updating...")

                    # Update price and dates if lower
                    try:
                        # Price
                        self.sheet.values().update(
                            spreadsheetId=SPREADSHEET_ID,
                            range=f"Data!C{int(index) + 2}:E{int(index) + 2}",
                            valueInputOption="USER_ENTERED",
                            body={
                                "values": [
                                    [f"{new_price}", f"{new_data.at[index, 'Outbound'].iloc[0,2]}",
                                     f"{new_data.at[index, 'Inbound'].iloc[0,2]}"]
                                ]
                            }
                        ).execute()

                    except HttpError as err:
                        print(err)

                else:
                    print(f"No new lowest prices for {row['City']}")
                    pass

    def check_desired_price(self, original_data, new_data):
        for index, row in original_data.iterrows():
            desired_price = int(row["Desired Price"])
            new_price = new_data.at[index, "Price"]
            if new_price <= desired_price:
                notification_manager.send_notification(new_data.iloc[index])
