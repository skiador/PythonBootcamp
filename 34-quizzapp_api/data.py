import requests


endpoint = "https://opentdb.com/api.php?"
parameters = {
    "amount": 10,
    "type": "boolean",
    "difficulty": "hard"
}

response = requests.get(endpoint, parameters)
response.raise_for_status()

question_data = response.json()["results"]
