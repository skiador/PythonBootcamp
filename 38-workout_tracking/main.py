import requests
import datetime
import os

APP_ID_NUTRIX = os.environ["APP_ID_NUTRIX"]
API_KEY_NUTRIX = os.environ["API_KEY_NUTRIX"]

URL_NUTRIX = "https://trackapi.nutritionix.com/v2/natural/exercise"
HEADERS_NUTRIX = {
    "x-app-id": APP_ID_NUTRIX,
    "x-app-key": API_KEY_NUTRIX
}


def get_new_exercise():
    prompt = input("What did you do? ")
    parameters = {
        "query": prompt,
        "gender": "male",
        "weight_kg": 64,
        "height_cm": 177,
        "age": 23
    }

    request = requests.post(url=URL_NUTRIX, json=parameters, headers=HEADERS_NUTRIX)
    return request.json()


def transform_data(raw_json):
    exercise = raw_json["exercises"][0]["name"]
    duration = raw_json["exercises"][0]["duration_min"]
    calories = raw_json["exercises"][0]["nf_calories"]

    formatted_data = {
        "workout": {
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.datetime.now().strftime("%X"),
            "exercise": exercise.title(),
            "duration": duration,
            "calories": calories
        }
    }
    return formatted_data


URL_SHEETS = os.environ["URL_SHEETS"]
TOKEN = os.environ["TOKEN"]
header = {
    "Authorization": f"Bearer {TOKEN}"
}


def add_data():
    raw_data = get_new_exercise()
    parameters = transform_data(raw_data)
    request = requests.post(url=URL_SHEETS, json=parameters, headers=header)
    print(request.text)
    print(request.raise_for_status())


add_data()
