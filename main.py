from typing import Dict
from pprint import pprint

import requests

SCRYFALL_URL = "https://api.scryfall.com"

def main():
    response = requests.get(SCRYFALL_URL)
    json_dict: Dict = response.json()
    print("Response from call:")
    pprint(json_dict)

if __name__ == "__main__":
    main()
