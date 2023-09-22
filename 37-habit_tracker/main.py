import requests
import datetime
import os

user_endpoint = "https://pixe.la/v1/users"
TOKEN = "aasdfasdfasdfasdfasdf"
USERNAME = "gerardpv"

params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(user_endpoint, json=params)
# print(response.text)

graph_endpoint = f"{user_endpoint}/{USERNAME}/graphs"
graph_params = {
    "id": "graph1",
    "name": "Reading Graph",
    "unit": "Pages",
    "type": "int",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# graph_response = requests.post(graph_endpoint, json=graph_params, headers=headers)
# print(graph_response.raise_for_status())


def add_pixel(quantity, year, month, day):
    pixel_endpoint = f"{user_endpoint}/{USERNAME}/graphs/graph1"
    date = datetime.date(year=year, month=month, day=day).strftime("%Y%m%d")
    pixel_params = {
        "date": date,
        "quantity": f"{quantity}"
    }

    pixel_request = requests.post(pixel_endpoint, json=pixel_params, headers=headers)
    print(pixel_request.text)


# add_pixel(56, 2023, 9, 21)


def delete_pixel(year, month, day):
    date = datetime.date(year=year, month=month, day=day).strftime("%Y%m%d")
    pixel_endpoint = f"{user_endpoint}/{USERNAME}/graphs/graph1/{date}"
    pixel_delete = requests.delete(url=pixel_endpoint, headers=headers)
    print(pixel_delete.raise_for_status())


# delete_pixel(2023, 9, 21)

def update_pixel(quantity, year, month, day):
    date = datetime.date(year=year, month=month, day=day).strftime("%Y%m%d")
    pixel_endpoint = f"{user_endpoint}/{USERNAME}/graphs/graph1/{date}"
    update_params = {
        "quantity": f"{quantity}"
    }
    update_request = requests.put(pixel_endpoint, json=update_params, headers=headers)
    print(update_request.raise_for_status())


# update_pixel(33, 2023, 9, 21)
