import requests
import json


class Country:

    def __init__(self) -> None:
        self.url = "https://restcountries.eu/rest/v2/all"

    def get_all_countries(self):
        response = requests.get(self.url)
        result = [country['name'] for country in json.loads(response.text)]
        return result
